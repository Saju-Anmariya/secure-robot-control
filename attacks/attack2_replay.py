"""Attack 2: replay. The attacker records a legitimate command and re-sends it."""
import time
from common import state, send

# Step 1: the operator sends a legitimate command; the attacker captures it.
captured = {"action": "forward"}
print("Operator sends:", captured)
send(captured["action"])
time.sleep(0.5)
send("stop")
print("State after operator:", state())

# Step 2: later, the attacker replays the exact same message.
time.sleep(1)
print("Attacker replays the captured command...")
send(captured["action"])
time.sleep(0.5)
send("stop")
print("State after replay:   ", state())
print("RESULT: replayed message was accepted again.")
