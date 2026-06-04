from pathlib import Path
import pytest
from claude_telegram.config import Config, load_config, flag_path


def test_load_config_reads_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok123")
    monkeypatch.setenv("TELEGRAM_ALLOWED_CHAT_ID", "555")
    monkeypatch.setenv("TELEGRAM_ANSWER_TIMEOUT", "30")
    cfg = load_config(env_file=None)
    assert cfg.bot_token == "tok123"
    assert cfg.allowed_chat_id == 555
    assert cfg.answer_timeout == 30.0


def test_load_config_missing_token_raises(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
        load_config(env_file=None)


def test_flag_path_user_scope(tmp_path):
    p = flag_path("user", home=tmp_path, project_dir=tmp_path / "proj")
    assert p == tmp_path / ".claude-telegram" / "telegram-mode"


def test_flag_path_project_scope(tmp_path):
    proj = tmp_path / "proj"
    p = flag_path("project", home=tmp_path, project_dir=proj)
    assert p == proj / ".claude" / "telegram-mode"


def test_load_config_blank_chat_id_is_none(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "tok")
    monkeypatch.setenv("TELEGRAM_ALLOWED_CHAT_ID", "")
    cfg = load_config(env_file=None)
    assert cfg.allowed_chat_id is None


def test_is_mode_on_and_set_mode_roundtrip(tmp_path):
    from claude_telegram.config import is_mode_on, set_mode
    p = tmp_path / "sub" / "telegram-mode"
    assert is_mode_on(p) is False  # missing file
    set_mode(p, True)
    assert is_mode_on(p) is True
    set_mode(p, False)
    assert is_mode_on(p) is False
