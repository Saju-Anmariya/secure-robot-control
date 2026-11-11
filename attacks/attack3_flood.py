"""Attack 3: flooding with commands."""
import time
from common import send

N = 300
start = time.time()
codes = [send("stop").status_code for _ in range(N)]
elapsed = time.time() - start
summary = {c: codes.count(c) for c in sorted(set(codes))}
print(f"Sent {N} commands in {elapsed:.2f}s ({N / elapsed:.0f} req/s)")
print("Status codes:", summary)
if 429 in codes:
    print(f"RESULT: rate limiting kicked in; {codes.count(429)} requests blocked.")
else:
    print("RESULT: server accepted everything, no rate limiting.")
