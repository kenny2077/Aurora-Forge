"""Behavior spec for config.parse_config. DO NOT MODIFY.

Make every test pass by fixing config.py.
"""
from config import parse_config


def test_basic_key_value():
    cfg = parse_config("[server]\nhost = localhost\n")
    assert cfg["server"]["host"] == "localhost"


def test_whitespace_is_trimmed():
    # surrounding spaces around key and value must be stripped
    cfg = parse_config("[server]\n   host   =    localhost   \n")
    assert cfg["server"]["host"] == "localhost"


def test_full_line_comments_skipped_even_when_indented():
    text = "[server]\n    # this is an indented comment\nhost = localhost\n"
    cfg = parse_config(text)
    assert cfg["server"]["host"] == "localhost"
    assert "# this is an indented comment" not in cfg["server"]


def test_inline_comment_stripped_from_value():
    cfg = parse_config("[server]\nport = 8080      # the http port\n")
    assert cfg["server"]["port"] == 8080


def test_int_float_and_negative_coercion():
    text = "[math]\na = 42\nb = 3.5\nc = -7\n"
    cfg = parse_config(text)
    assert cfg["math"]["a"] == 42 and isinstance(cfg["math"]["a"], int)
    assert cfg["math"]["b"] == 3.5 and isinstance(cfg["math"]["b"], float)
    assert cfg["math"]["c"] == -7


def test_bool_coercion_true_and_false():
    cfg = parse_config("[flags]\nx = true\ny = false\n")
    assert cfg["flags"]["x"] is True
    assert cfg["flags"]["y"] is False


def test_repeated_key_last_value_wins():
    cfg = parse_config("[server]\nport = 8080\nport = 9090\n")
    assert cfg["server"]["port"] == 9090


def test_repeated_section_merges():
    text = "[server]\nhost = localhost\n[server]\nport = 8080\n"
    cfg = parse_config(text)
    assert cfg["server"]["host"] == "localhost"
    assert cfg["server"]["port"] == 8080


def test_section_header_with_inline_comment():
    text = "[server]   # main server block\nhost = localhost\n"
    cfg = parse_config(text)
    assert "server" in cfg
    assert cfg["server"]["host"] == "localhost"


def test_keys_before_any_section_go_to_default():
    cfg = parse_config("name = toplevel\n[server]\nhost = localhost\n")
    assert cfg["DEFAULT"]["name"] == "toplevel"
    assert cfg["server"]["host"] == "localhost"


def test_value_containing_equals_sign():
    # only the first '=' separates key from value
    cfg = parse_config("[db]\nurl = postgres://u:p@host/db?x=1\n")
    assert cfg["db"]["url"] == "postgres://u:p@host/db?x=1"


def test_semver_like_value_stays_a_string():
    # a real coercion edge: "1.0.0" is not an int OR a float — it must stay a str,
    # so a naive `float(value)` fix would regress here
    cfg = parse_config("[app]\nversion = 1.0.0\n")
    assert cfg["app"]["version"] == "1.0.0"
