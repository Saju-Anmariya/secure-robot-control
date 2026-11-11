import pytest

from robot import ARENA_SIZE, Robot


def test_forward_moves_east():
    r = Robot()
    r.command("forward")
    for _ in range(10):
        r.step(0.1)
    assert r.x > 5.0
    assert r.y == pytest.approx(5.0)


def test_stop_halts_robot():
    r = Robot()
    r.command("forward")
    r.step(0.1)
    r.command("stop")
    x = r.x
    r.step(0.1)
    assert r.x == x


def test_robot_stays_in_arena():
    r = Robot()
    r.command("forward")
    for _ in range(1000):
        r.step(0.1)
    assert 0 <= r.x <= ARENA_SIZE
    assert 0 <= r.y <= ARENA_SIZE


def test_unknown_command_rejected():
    with pytest.raises(ValueError):
        Robot().command("self_destruct")
