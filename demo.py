import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from robot import Robot, ARENA_SIZE

robot = Robot()

def run(action, seconds):
    robot.command(action)
    for _ in range(int(round(seconds / 0.1))):
        robot.step(0.1)

for _ in range(4):          # four sides of a square
    run("forward", 2)       # drive 4 units
    run("stop", 0.1)
    run("left", 1)          # turn 90 degrees on the spot
    run("stop", 0.1)

xs, ys = zip(*robot.trail)
plt.figure(figsize=(6, 6))
plt.plot(xs, ys, "-", label="path")
plt.plot(xs[0], ys[0], "go", label="start")
plt.plot(xs[-1], ys[-1], "ro", label="end")
plt.xlim(0, ARENA_SIZE)
plt.ylim(0, ARENA_SIZE)
plt.gca().set_aspect("equal")
plt.title("Simulated robot path")
plt.legend()
plt.savefig("robot_demo.png", dpi=120)
print("final state:", robot.state())
