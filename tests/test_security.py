import secrets
import time

from fastapi.testclient import TestClient

import api_secure
from signing import sign

client = TestClient(api_secure.app)


def signed(action, ts=None, secret=None):
    ts = str(ts if ts is not None else time.time())
    nonce = secrets.token_hex(16)
    sig = sign(secret or api_secure.SECRET, ts, nonce, action)
    return {"X-Timestamp": ts, "X-Nonce": nonce, "X-Signature": sig}


def post(action, headers=None):
    return client.post("/command", json={"action": action}, headers=headers)


def test_valid_signed_command_accepted():
    r = post("forward", signed("forward"))
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_unauthenticated_command_rejected():
    r = post("forward")
    assert r.status_code == 401
    assert r.json()["detail"] == "authentication required"


def test_wrong_secret_rejected():
    r = post("forward", signed("forward", secret=b"x" * 64))
    assert r.status_code == 401
    assert r.json()["detail"] == "bad signature"


def test_tampered_action_rejected():
    headers = signed("stop")               # signature is valid for 'stop'
    r = post("forward", headers)           # attacker swaps the action
    assert r.status_code == 401
    assert r.json()["detail"] == "bad signature"


def test_replayed_message_rejected():
    headers = signed("forward")
    assert post("forward", headers).status_code == 200
    r = post("forward", headers)           # exact same message again
    assert r.status_code == 401
    assert r.json()["detail"] == "replay detected"


def test_expired_message_rejected():
    old = time.time() - 120
    r = post("forward", signed("forward", ts=old))
    assert r.status_code == 401
    assert r.json()["detail"] == "request expired"


def test_invalid_action_rejected_even_when_signed():
    r = post("self_destruct", signed("self_destruct"))
    assert r.status_code == 400


def test_flooding_is_rate_limited():
    codes = [post("stop").status_code for _ in range(60)]
    assert 429 in codes
    assert codes.count(429) > 30
