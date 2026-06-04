---
description: Toggle Telegram remote-answer mode for this session
---

The user ran `/telegram $ARGUMENTS`.

Run this to flip the mode flag (interpret no argument as "on", `off` as off):

```bash
claude-telegram mode $ARGUMENTS
```

If the flag was set to **on**:
- Telegram mode is now ACTIVE for this session.
- For every subsequent user-facing choice, call the `ask_telegram` MCP tool
  INSTEAD of the built-in `AskUserQuestion`. Pass the same questions/options you
  would have shown in the terminal.
- The user will answer from Telegram (buttons or free text); use the returned values.

If the flag was set to **off**:
- Telegram mode is now OFF. Resume using the normal `AskUserQuestion` tool.

Confirm the new state to the user in one short line.
