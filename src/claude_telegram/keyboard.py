from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

OTHER_LABEL = "✏️ Інше"


@dataclass(frozen=True)
class Callback:
    request_id: str
    kind: Literal["option", "other"]
    index: Optional[int]


def encode_option(request_id: str, index: int) -> str:
    return f"q:{request_id}:o:{index}"


def encode_other(request_id: str) -> str:
    return f"q:{request_id}:x"


def decode_callback(data: str) -> Optional[Callback]:
    parts = data.split(":")
    if len(parts) < 3 or parts[0] != "q":
        return None
    rid = parts[1]
    if parts[2] == "o" and len(parts) == 4 and parts[3].isdigit():
        return Callback(rid, "option", int(parts[3]))
    if parts[2] == "x":
        return Callback(rid, "other", None)
    return None


def build_keyboard(request_id: str, option_labels: list[str]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=label, callback_data=encode_option(request_id, i))]
        for i, label in enumerate(option_labels)
    ]
    rows.append(
        [InlineKeyboardButton(text=OTHER_LABEL, callback_data=encode_other(request_id))]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)
