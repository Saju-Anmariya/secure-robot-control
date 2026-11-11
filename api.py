"""Robot control API, version 1: deliberately INSECURE (no authentication)."""
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from robot import Robot

robot = Robot()


async def simulation_loop():
    while True:
        robot.step(0.1)
        await asyncio.sleep(0.1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(simulation_loop())
    yield
    task.cancel()


app = FastAPI(title="Robot Control API (INSECURE v1)", lifespan=lifespan)


class Command(BaseModel):
    action: str


@app.get("/state")
def get_state():
    return robot.state()


@app.post("/command")
def send_command(cmd: Command):
    try:
        robot.command(cmd.action)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True, "state": robot.state()}
