# ClaudeTelegram

Answer Claude Code's multiple-choice prompts from a Telegram bot — keep the agent
working while you're away from the keyboard.

When Telegram mode is on, Claude Code routes its choices (the `AskUserQuestion`-style
1–4 option prompts) to your Telegram bot. You tap a button — or type a free-text
answer — from your phone, and the agent continues with your selection.

## Install

```bash
pipx install claude-telegram
claude-telegram setup        # prompts for scope (user/project/local) + bot token
```

`setup` registers the MCP server with Claude Code (`claude mcp add` at the chosen
scope), installs the `/telegram` slash command, and writes config to
`~/.claude-telegram/.env`.

If `claude mcp add` can't run automatically, `setup` prints the exact command to run
manually.

### Statusline indicator (optional)

To show `📱 Telegram ON` in the Claude Code statusline while the mode is active, wrap
your existing `statusLine.command` in `settings.json` with the bundled wrapper, e.g.
(replace `BASE` with your current command):

```jsonc
"statusLine": {
  "type": "command",
  "command": "CLAUDE_TELEGRAM_BASE_STATUSLINE='BASE' python -m claude_telegram.statusline"
}
```

The wrapper runs your original statusline as-is and appends the indicator only when the
mode flag is on (so claude-hud or any other statusline keeps working untouched).

## Use

1. In a Claude Code session, run `/telegram` to turn on remote mode (`/telegram off`
   to turn it off).
2. When Claude needs a choice, it arrives in Telegram with buttons. Tap one, or tap
   **✏️ Інше** to type a free-text answer. The agent continues with your answer.

Send `/start` to the bot at any time to get your chat id (put it in
`~/.claude-telegram/.env` as `TELEGRAM_ALLOWED_CHAT_ID` so the bot only listens to you).

## Configuration

`~/.claude-telegram/.env`:

| Variable | Meaning |
|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather |
| `TELEGRAM_ALLOWED_CHAT_ID` | Your chat id; the bot ignores everyone else |
| `TELEGRAM_ANSWER_TIMEOUT` | Seconds to wait for an answer (`0` = wait forever) |

## Limitations

- One active session at a time — Telegram allows only a single long-polling consumer
  per bot token.

## Development

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"
.venv/Scripts/python -m pytest -v
```
