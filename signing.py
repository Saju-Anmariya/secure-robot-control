import hashlib
import hmac
import os
from pathlib import Path


def load_secret() -> bytes:
    value = os.environ.get("ROBOT_SECRET")
    if not value:
        path = Path(__file__).parent / ".robot_secret"
        if path.exists():
            value = path.read_text().strip()
    if not value or len(value) < 32:
        raise SystemExit("No secret found. Create .robot_secret first.")
    return value.encode()


def sign(secret: bytes, timestamp: str, nonce: str, action: str) -> str:
    message = f"{timestamp}.{nonce}.{action}".encode()
    return hmac.new(secret, message, hashlib.sha256).hexdigest()
