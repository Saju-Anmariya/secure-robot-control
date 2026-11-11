"""Robot control API, version 2: SECURED (signed requests, replay protection,
rate limiting, security logging)."""
import asyncio
import hmac
import logging
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

from robot import Robot
from signing import load_secret, sign

SECRET = load_secret()
MAX_AGE = 30          # seconds a signed request stays valid
RATE_LIMIT = 20       # commands allowed ...
RATE_WINDOW = 10      # ... per this many seconds, per IP

logging.basicConfig(filename="security.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("robot.security")

robot = Robot()
seen_nonces: dict[str, float] = {}
hits: dict[str, deque] = defaultdict(deque)


def rate_limited(ip: str) -> bool:
    now = time.time()
    q = hits[ip]
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return True
    q.append(now)
    return False


def nonce_used(nonce: str) -> bool:
    now = time.time()
    for n in [n for n, exp in seen_nonces.items() if exp < now]:
        del seen_nonces[n]
    if nonce in seen_nonces:
        return True
    seen_nonces[nonce] = now + MAX_AGE * 2
    return False


def reject(status: int, reason: str, ip: str):
    log.warning("REJECTED ip=%s status=%s reason=%s", ip, status, reason)
    raise HTTPException(status_code=status, detail=reason)


async def simulation_loop():
    while True:
        robot.step(0.1)
        await asyncio.sleep(0.1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(simulation_loop())
    yield
    task.cancel()


app = FastAPI(title="Robot Control API (SECURE v2)", lifespan=lifespan)


class Command(BaseModel):
    action: str


@app.get("/state")
def get_state():
    # Read-only telemetry, left open on purpose (see README: known limitation).
    return robot.state()


@app.post("/command")
def send_command(cmd: Command, request: Request,
                 x_timestamp: str | None = Header(default=None),
                 x_nonce: str | None = Header(default=None),
                 x_signature: str | None = Header(default=None)):
    ip = request.client.host

    if rate_limited(ip):
        reject(429, "too many requests", ip)

    if not (x_timestamp and x_nonce and x_signature):
        reject(401, "authentication required", ip)
    if len(x_nonce) > 64:
        reject(401, "invalid nonce", ip)

    try:
        ts = float(x_timestamp)
    except ValueError:
        reject(401, "invalid timestamp", ip)
    if abs(time.time() - ts) > MAX_AGE:
        reject(401, "request expired", ip)

    expected = sign(SECRET, x_timestamp, x_nonce, cmd.action)
    if not hmac.compare_digest(expected, x_signature):
        reject(401, "bad signature", ip)

    # Only validly signed nonces are stored, so attackers cannot fill the store.
    if nonce_used(x_nonce):
        reject(401, "replay detected", ip)

    try:
        robot.command(cmd.action)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    log.info("ACCEPTED ip=%s action=%s", ip, cmd.action)
    return {"ok": True, "state": robot.state()}
