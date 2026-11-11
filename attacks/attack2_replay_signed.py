"""Attack 2 (signed version): the attacker captures a valid signed command
and replays it."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import requests
from client_secure import BASE, send_signed, signed_headers

action = "forward"
captured_headers = signed_headers(action)      # what an eavesdropper would see
captured_body = {"action": action}

r1 = requests.post(f"{BASE}/command", json=captured_body,
                   headers=captured_headers, timeout=5)
print("Operator sends signed 'forward' ->", r1.status_code)
time.sleep(0.5)
send_signed("stop")

print("Attacker replays the captured message...")
r2 = requests.post(f"{BASE}/command", json=captured_body,
                   headers=captured_headers, timeout=5)
print("Replay ->", r2.status_code, r2.json())
if r2.status_code == 200:
    print("RESULT: replayed message accepted.")
else:
    print("RESULT: replay blocked.")
