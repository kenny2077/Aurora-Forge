"""Hidden acceptance spec for slugify. DO NOT read until prompt.md is written. DO NOT modify.

These cases ARE the agreed spec after clarification. Your prompt.md should have predicted them.
"""
from solution import slugify


def test_basic_words():
    assert slugify("Hello World") == "hello-world"


def test_lowercases():
    assert slugify("MixedCASE") == "mixedcase"


def test_collapses_whitespace_and_separators():
    assert slugify("  Multiple   Spaces  ") == "multiple-spaces"


def test_strips_leading_and_trailing_separators():
    assert slugify("Trailing---dashes!!!") == "trailing-dashes"


def test_non_alphanumeric_becomes_single_hyphen():
    assert slugify("C++ & Python!") == "c-python"


def test_digits_are_kept():
    assert slugify("123 Numbers") == "123-numbers"


def test_already_a_slug_is_stable():
    assert slugify("already-a-slug") == "already-a-slug"


def test_non_ascii_letters_are_separators():
    # decision: only [a-z0-9] survive; accented/other letters act as separators
    assert slugify("Café del Mar") == "caf-del-mar"


def test_all_symbols_becomes_empty_string():
    assert slugify("!!!") == ""


def test_empty_input():
    assert slugify("") == ""
