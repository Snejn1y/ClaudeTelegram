from __future__ import annotations

import asyncio
import uuid
from typing import Optional


class Registry:
    """Tracks pending ask_telegram requests and their answers."""

    def __init__(self) -> None:
        self._futures: dict[str, asyncio.Future] = {}
        self._awaiting_text: dict[int, str] = {}

    def new_request(self) -> tuple[str, asyncio.Future]:
        rid = uuid.uuid4().hex[:6]
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        self._futures[rid] = fut
        return rid, fut

    def resolve(self, request_id: str, value: str) -> bool:
        fut = self._futures.pop(request_id, None)
        if fut is None or fut.done():
            return False
        fut.set_result(value)
        return True

    def mark_awaiting_text(self, chat_id: int, request_id: str) -> None:
        self._awaiting_text[chat_id] = request_id

    def pop_awaiting_text(self, chat_id: int) -> Optional[str]:
        return self._awaiting_text.pop(chat_id, None)

    async def wait(self, request_id: str, fut: asyncio.Future, timeout: float) -> str:
        try:
            if timeout and timeout > 0:
                return await asyncio.wait_for(fut, timeout=timeout)
            return await fut
        except asyncio.TimeoutError:
            self._futures.pop(request_id, None)
            raise
