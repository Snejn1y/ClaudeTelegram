import pytest
from claude_telegram import keyboard


def test_encode_decode_option_roundtrip():
    data = keyboard.encode_option("3f", 2)
    assert data == "q:3f:o:2"
    parsed = keyboard.decode_callback(data)
    assert parsed == keyboard.Callback(request_id="3f", kind="option", index=2)


def test_encode_decode_other_roundtrip():
    data = keyboard.encode_other("3f")
    assert data == "q:3f:x"
    assert keyboard.decode_callback(data) == keyboard.Callback("3f", "other", None)


def test_decode_rejects_foreign_data():
    assert keyboard.decode_callback("garbage") is None


def test_build_keyboard_has_button_per_option_plus_other():
    kb = keyboard.build_keyboard("3f", ["Yes", "No", "Maybe"])
    rows = kb.inline_keyboard
    assert len(rows) == 4
    assert rows[0][0].text == "Yes"
    assert rows[0][0].callback_data == "q:3f:o:0"
    assert rows[3][0].callback_data == "q:3f:x"
