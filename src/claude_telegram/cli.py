from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from importlib.resources import files
from pathlib import Path

from .config import DEFAULT_ENV_FILE, flag_path, set_mode


def _command_template_text() -> str:
    return (
        files("claude_telegram")
        .joinpath("commands", "telegram.md")
        .read_text(encoding="utf-8")
    )


def _cmd_serve(_args: argparse.Namespace) -> int:
    from .server import run
    run()
    return 0


def _cmd_mode(args: argparse.Namespace) -> int:
    on = args.state != "off"
    path = flag_path(args.scope, home=Path.home(), project_dir=Path.cwd())
    set_mode(path, on)
    print(f"Telegram mode {'ON' if on else 'OFF'} ({path})")
    return 0


def _cmd_setup(args: argparse.Namespace) -> int:
    scope = args.scope or input("Scope [user/project/local] (default user): ").strip() or "user"

    DEFAULT_ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DEFAULT_ENV_FILE.exists():
        token = input("Bot token from @BotFather: ").strip()
        chat = input("Allowed chat id (blank to fill later via /start): ").strip()
        DEFAULT_ENV_FILE.write_text(
            f"TELEGRAM_BOT_TOKEN={token}\n"
            f"TELEGRAM_ALLOWED_CHAT_ID={chat}\n"
            f"TELEGRAM_ANSWER_TIMEOUT=0\n",
            encoding="utf-8",
        )
        print(f"Wrote {DEFAULT_ENV_FILE}")

    exe = shutil.which("claude-telegram") or "claude-telegram"
    try:
        subprocess.run(
            ["claude", "mcp", "add", "--scope", scope, "claude-telegram", exe, "serve"],
            check=True,
        )
        print(f"Registered MCP server (scope={scope})")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"!! Could not auto-register MCP server: {e}")
        print(f"   Run manually: claude mcp add --scope {scope} claude-telegram {exe} serve")

    cmd_dir = (
        Path.home() / ".claude" / "commands" if scope == "user"
        else Path.cwd() / ".claude" / "commands"
    )
    cmd_dir.mkdir(parents=True, exist_ok=True)
    (cmd_dir / "telegram.md").write_text(_command_template_text(), encoding="utf-8")
    print(f"Installed /telegram command to {cmd_dir}")

    print(
        "\nStatusline: to show the indicator, set your statusLine command to wrap the\n"
        "existing one. Example for settings.json (replace BASE with your current\n"
        "statusLine.command):\n"
        '  "command": "CLAUDE_TELEGRAM_BASE_STATUSLINE=\'BASE\' '
        'python -m claude_telegram.statusline"\n'
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="claude-telegram")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_serve = sub.add_parser("serve", help="run the MCP server")
    p_serve.set_defaults(func=_cmd_serve)

    p_mode = sub.add_parser("mode", help="toggle telegram mode flag")
    p_mode.add_argument("state", nargs="?", default="on", choices=["on", "off"])
    p_mode.add_argument("--scope", default="user", choices=["user", "project", "local"])
    p_mode.set_defaults(func=_cmd_mode)

    p_setup = sub.add_parser("setup", help="install + register everything")
    p_setup.add_argument("--scope", default=None, choices=["user", "project", "local"])
    p_setup.set_defaults(func=_cmd_setup)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
