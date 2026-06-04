from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv

Scope = Literal["user", "project", "local"]

DEFAULT_ENV_FILE = Path.home() / ".claude-telegram" / ".env"


@dataclass(frozen=True)
class Config:
    bot_token: str
    allowed_chat_id: Optional[int]
    answer_timeout: float


def load_config(env_file: Optional[Path] = DEFAULT_ENV_FILE) -> Config:
    if env_file is not None and Path(env_file).exists():
        load_dotenv(env_file)
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    chat_raw = os.environ.get("TELEGRAM_ALLOWED_CHAT_ID", "").strip()
    chat_id = int(chat_raw) if chat_raw else None
    timeout = float(os.environ.get("TELEGRAM_ANSWER_TIMEOUT", "0") or "0")
    return Config(bot_token=token, allowed_chat_id=chat_id, answer_timeout=timeout)


def flag_path(scope: Scope, home: Path, project_dir: Path) -> Path:
    if scope == "user":
        return home / ".claude-telegram" / "telegram-mode"
    return project_dir / ".claude" / "telegram-mode"


def is_mode_on(path: Path) -> bool:
    try:
        return path.read_text(encoding="utf-8").strip() == "on"
    except OSError:
        return False


def set_mode(path: Path, on: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("on" if on else "off", encoding="utf-8")
