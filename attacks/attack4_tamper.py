"""Attack 4: the attacker captures a signed 'stop' and changes it to 'forward'."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import requests
from client_secure import BASE, signed_headers

headers = signed_headers("stop")               # valid signature for 'stop'
r = requests.post(f"{BASE}/command", json={"action": "forward"},
                  headers=headers, timeout=5)
print("Tampered command (stop -> forward) ->", r.status_code, r.json())
if r.status_code == 200:
    print("RESULT: tampered message accepted.")
else:
    print("RESULT: tampering blocked.")
