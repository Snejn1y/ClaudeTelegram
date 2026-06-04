from claude_telegram.bot import decode_answer


def test_decode_answer_option_returns_label():
    assert decode_answer("o:1", ["A", "B", "C"]) == "B"


def test_decode_answer_free_text():
    assert decode_answer("t:hello world", ["A"]) == "hello world"


def test_decode_answer_out_of_range_index_falls_back_to_raw():
    assert decode_answer("o:99", ["A", "B"]) == "o:99"


def test_decode_answer_unknown_prefix_returns_raw():
    assert decode_answer("weird", ["A"]) == "weird"
