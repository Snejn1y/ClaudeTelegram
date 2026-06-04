import asyncio
import pytest
from claude_telegram.registry import Registry


async def test_new_request_returns_unique_ids():
    reg = Registry()
    rid1, _ = reg.new_request()
    rid2, _ = reg.new_request()
    assert rid1 != rid2


async def test_resolve_sets_future_result():
    reg = Registry()
    rid, fut = reg.new_request()
    assert reg.resolve(rid, "Yes") is True
    assert await fut == "Yes"


async def test_resolve_unknown_id_returns_false():
    reg = Registry()
    assert reg.resolve("nope", "x") is False


async def test_resolve_twice_returns_false_second_time():
    reg = Registry()
    rid, _ = reg.new_request()
    assert reg.resolve(rid, "a") is True
    assert reg.resolve(rid, "b") is False


async def test_awaiting_text_roundtrip():
    reg = Registry()
    reg.mark_awaiting_text(chat_id=555, request_id="ab")
    assert reg.pop_awaiting_text(555) == "ab"
    assert reg.pop_awaiting_text(555) is None


async def test_wait_times_out_and_cleans_up():
    reg = Registry()
    rid, fut = reg.new_request()
    with pytest.raises(asyncio.TimeoutError):
        await reg.wait(rid, fut, timeout=0.01)
    assert reg.resolve(rid, "late") is False
