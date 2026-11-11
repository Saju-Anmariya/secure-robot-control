import os
import secrets
import time

import requests

from signing import load_secret, sign

BASE = os.environ.get("ROBOT_URL", "http://127.0.0.1:8001")
SECRET = load_secret()


def signed_headers(action: str) -> dict:
    ts = str(time.time())
    nonce = secrets.token_hex(16)
    return {"X-Timestamp": ts, "X-Nonce": nonce,
            "X-Signature": sign(SECRET, ts, nonce, action)}


def send_signed(action: str):
    return requests.post(f"{BASE}/command", json={"action": action},
                         headers=signed_headers(action), timeout=5)
