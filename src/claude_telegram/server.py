from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from aiogram import Bot
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from .bot import Question, QuestionOption, ask, build_dispatcher
from .config import load_config
from .registry import Registry

_config = load_config()
_registry = Registry()
_bot = Bot(token=_config.bot_token)


@asynccontextmanager
async def _lifespan(_server: FastMCP):
    dp = build_dispatcher(_config, _registry)
    task = asyncio.create_task(dp.start_polling(_bot, handle_signals=False))
    try:
        yield
    finally:
        task.cancel()
        await _bot.session.close()


mcp = FastMCP("claude-telegram", lifespan=_lifespan)


class OptionIn(BaseModel):
    label: str
    description: str = ""


class QuestionIn(BaseModel):
    header: str = Field(description="Short label, max ~12 chars")
    question: str
    options: list[OptionIn] = Field(min_length=1, max_length=4)


@mcp.tool()
async def ask_telegram(
    questions: Annotated[list[QuestionIn], Field(min_length=1, max_length=4)],
) -> dict:
    """Ask the user one or more multiple-choice questions via Telegram and wait for
    their answers. Use this instead of AskUserQuestion when Telegram mode is on.
    Returns each question's header mapped to the chosen option label (or free text)."""
    answers: dict[str, str] = {}
    for q in questions:
        domain_q = Question(
            header=q.header,
            question=q.question,
            options=[QuestionOption(o.label, o.description) for o in q.options],
        )
        answers[q.header] = await ask(_bot, _config, _registry, domain_q)
    return answers


def run() -> None:
    mcp.run()
