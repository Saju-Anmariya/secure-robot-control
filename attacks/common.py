import requests

BASE = "http://127.0.0.1:8000"


def state():
    return requests.get(f"{BASE}/state", timeout=5).json()


def send(action, headers=None):
    return requests.post(f"{BASE}/command", json={"action": action},
                         headers=headers, timeout=5)
