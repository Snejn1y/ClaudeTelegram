from __future__ import annotations

import html
from dataclasses import dataclass

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from .config import Config
from .keyboard import build_keyboard, decode_callback
from .registry import Registry


@dataclass
class QuestionOption:
    label: str
    description: str = ""


@dataclass
class Question:
    header: str
    question: str
    options: list[QuestionOption]


def _render(question: Question) -> str:
    lines = [f"<b>{html.escape(question.header)}</b>", html.escape(question.question), ""]
    for i, opt in enumerate(question.options):
        desc = f" — {html.escape(opt.description)}" if opt.description else ""
        lines.append(f"<b>{i + 1}.</b> {html.escape(opt.label)}{desc}")
    return "\n".join(lines)


def build_dispatcher(config: Config, registry: Registry) -> Dispatcher:
    dp = Dispatcher()

    def _allowed(chat_id: int) -> bool:
        return config.allowed_chat_id is None or chat_id == config.allowed_chat_id

    @dp.message(Command("start"))
    async def on_start(message: Message) -> None:
        await message.answer(f"Your chat id: <code>{message.chat.id}</code>")

    @dp.callback_query(F.data.startswith("q:"))
    async def on_callback(cb: CallbackQuery) -> None:
        if not _allowed(cb.message.chat.id):
            await cb.answer("Not authorized")
            return
        parsed = decode_callback(cb.data or "")
        if parsed is None:
            await cb.answer()
            return
        if parsed.kind == "other":
            registry.mark_awaiting_text(cb.message.chat.id, parsed.request_id)
            await cb.message.answer("Надішли відповідь текстом:")
            await cb.answer()
            return
        resolved = registry.resolve(parsed.request_id, f"o:{parsed.index}")
        await cb.answer("✓" if resolved else "")

    @dp.message(F.text)
    async def on_text(message: Message) -> None:
        if not _allowed(message.chat.id):
            return
        rid = registry.pop_awaiting_text(message.chat.id)
        if rid is None:
            return
        registry.resolve(rid, f"t:{message.text}")

    return dp


async def ask(bot: Bot, config: Config, registry: Registry, question: Question) -> str:
    """Send one question, wait for the answer, return the chosen label or free text."""
    rid, fut = registry.new_request()
    labels = [o.label for o in question.options]
    await bot.send_message(
        chat_id=config.allowed_chat_id,
        text=_render(question),
        reply_markup=build_keyboard(rid, labels),
        parse_mode="HTML",
    )
    raw = await registry.wait(rid, fut, timeout=config.answer_timeout)
    if raw.startswith("o:"):
        return labels[int(raw[2:])]
    if raw.startswith("t:"):
        return raw[2:]
    return raw
