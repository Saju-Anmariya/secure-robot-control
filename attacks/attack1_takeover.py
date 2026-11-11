"""Attack 1: no credentials. The attacker tries to steer the robot."""
import time
from common import state, send

print("Before:", state())
r = send("left")
print("Attacker sends 'left' with NO credentials ->", r.status_code)
time.sleep(1)
send("stop")
print("After: ", state())
if r.status_code == 200:
    print("RESULT: robot controlled by an unauthenticated stranger.")
else:
    print(f"RESULT: attack blocked (HTTP {r.status_code}).")
