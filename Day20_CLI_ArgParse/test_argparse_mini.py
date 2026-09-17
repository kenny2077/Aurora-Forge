"""Spec for the mini arg parser. DO NOT MODIFY."""
import pytest

from argparse_mini import parse


def test_defaults():
    r = parse([])
    assert r == {"verbose": False, "output": None, "retries": 3, "positional": []}


def test_verbose_flag():
    assert parse(["--verbose"])["verbose"] is True


def test_output_space_form():
    assert parse(["--output", "out.txt"])["output"] == "out.txt"


def test_output_equals_form():
    assert parse(["--output=out.txt"])["output"] == "out.txt"


def test_retries_is_int_space_form():
    r = parse(["--retries", "5"])
    assert r["retries"] == 5
    assert isinstance(r["retries"], int)


def test_retries_is_int_equals_form():
    assert parse(["--retries=7"])["retries"] == 7


def test_positional_args():
    assert parse(["build", "target"])["positional"] == ["build", "target"]


def test_mixed_flags_and_positionals():
    r = parse(["build", "--verbose", "--output=log.txt", "target"])
    assert r["verbose"] is True
    assert r["output"] == "log.txt"
    assert r["positional"] == ["build", "target"]


def test_unknown_option_raises():
    with pytest.raises(ValueError):
        parse(["--nope"])


def test_double_dash_terminator():
    r = parse(["--", "--verbose", "file.txt"])
    assert r["verbose"] is False                       # after --, options are literal
    assert r["positional"] == ["--verbose", "file.txt"]


def test_output_empty_equals_value():
    # "--output=" is an explicit empty value, not a positional
    assert parse(["--output="])["output"] == ""


def test_non_integer_retries_raises():
    with pytest.raises(ValueError):
        parse(["--retries", "abc"])
