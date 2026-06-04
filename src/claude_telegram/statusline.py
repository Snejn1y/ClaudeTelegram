from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from .config import is_mode_on

INDICATOR = " \U0001f4f1 Telegram ON"


def main() -> None:
    stdin_data = sys.stdin.read()
    base_cmd = os.environ.get("CLAUDE_TELEGRAM_BASE_STATUSLINE", "")
    base_output = ""
    if base_cmd:
        proc = subprocess.run(
            base_cmd, shell=True, input=stdin_data,
            capture_output=True, text=True,
        )
        base_output = proc.stdout.rstrip("\n")
    flag = Path(os.environ.get("CLAUDE_TELEGRAM_FLAG", "")) if os.environ.get(
        "CLAUDE_TELEGRAM_FLAG"
    ) else (Path.home() / ".claude-telegram" / "telegram-mode")
    suffix = INDICATOR if is_mode_on(flag) else ""
    sys.stdout.write(base_output + suffix + "\n")


if __name__ == "__main__":
    main()
