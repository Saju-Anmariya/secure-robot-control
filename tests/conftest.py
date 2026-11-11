import os

# Must be set before api_secure is imported (it loads the secret at import time).
os.environ.setdefault("ROBOT_SECRET", "t" * 64)

import pytest

import api_secure


@pytest.fixture(autouse=True)
def clean_state():
    api_secure.hits.clear()
    api_secure.seen_nonces.clear()
    yield
