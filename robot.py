import math
from dataclasses import dataclass, field

ARENA_SIZE = 10.0
MAX_SPEED = 2.0       # units per second
TURN_RATE = 90.0      # degrees per second

VALID_COMMANDS = {"forward", "backward", "left", "right", "stop"}


@dataclass
class Robot:
    x: float = 5.0
    y: float = 5.0
    heading: float = 0.0   # degrees, 0 = east
    speed: float = 0.0
    turn: float = 0.0      # +1 = left, -1 = right, 0 = straight
    trail: list = field(default_factory=list)

    def command(self, action: str) -> None:
        if action not in VALID_COMMANDS:
            raise ValueError(f"unknown command: {action}")
        if action == "forward":
            self.speed = MAX_SPEED
        elif action == "backward":
            self.speed = -MAX_SPEED
        elif action == "left":
            self.turn = 1.0
        elif action == "right":
            self.turn = -1.0
        elif action == "stop":
            self.speed = 0.0
            self.turn = 0.0

    def step(self, dt: float = 0.1) -> None:
        self.heading = (self.heading + self.turn * TURN_RATE * dt) % 360
        rad = math.radians(self.heading)
        self.x += self.speed * math.cos(rad) * dt
        self.y += self.speed * math.sin(rad) * dt
        self.x = min(max(self.x, 0.0), ARENA_SIZE)
        self.y = min(max(self.y, 0.0), ARENA_SIZE)
        self.trail.append((self.x, self.y))

    def state(self) -> dict:
        return {
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "heading": round(self.heading, 1),
            "speed": self.speed,
        }
