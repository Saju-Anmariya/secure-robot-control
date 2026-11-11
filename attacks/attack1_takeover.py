"""Attack 1: no authentication. The attacker has no credentials at all."""
import time
from common import state, send

print("Before:", state())
r = send("stop")
print("Attacker sends 'left' with NO credentials ->", r.status_code)
send("left")
time.sleep(1)
send("stop")
print("After: ", state())
print("RESULT: robot controlled by an unauthenticated stranger.")
