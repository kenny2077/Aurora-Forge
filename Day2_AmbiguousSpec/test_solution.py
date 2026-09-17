"""Hidden spec for Day 2. DO NOT read until spec_notes.md is filled in. DO NOT modify.

The behavioral rules are NOT written here on purpose — infer them from the cases, the way
you'd infer an interviewer's intent from their reactions. The full rule list lives in
SPEC_REVEAL.md, which you open only at the reconciliation step.
"""
import pytest
from solution import wrap_lines, line_count


def test_single_line_exact_fit():
    assert line_count("hello world", 11) == 1


def test_wraps_when_too_wide():
    assert line_count("hello world", 10) == 2


def test_greedy_packing():
    assert line_count("the quick brown fox", 9) == 2


def test_wrap_lines_returns_the_wrapped_strings():
    assert wrap_lines("the quick brown fox", 9) == ["the quick", "brown fox"]


def test_single_word():
    assert line_count("hello", 5) == 1


def test_overlong_word_gets_its_own_line():
    assert line_count("supercalifragilistic", 5) == 1


def test_overlong_word_in_the_middle():
    assert line_count("hi supercalifrag hi", 5) == 3


def test_everything_on_one_line_when_wide():
    assert line_count("a bb ccc", 100) == 1


def test_empty_text_is_zero_lines():
    assert line_count("", 5) == 0
    assert wrap_lines("", 5) == []


def test_whitespace_only_text_is_zero_lines():
    assert line_count("      ", 5) == 0


def test_collapses_extra_whitespace():
    assert line_count("  hello    world  ", 11) == 1


def test_existing_newline_forces_a_hard_break():
    # a '\n' already in the input is a hard line break the printer must honor
    assert line_count("a\nb", 80) == 2
    assert wrap_lines("a\nb", 80) == ["a", "b"]


def test_newline_break_combines_with_wrapping():
    # first segment fits on one line, newline forces a second segment
    assert wrap_lines("hello world\nfoo", 11) == ["hello world", "foo"]
    assert line_count("hello world\nfoo", 11) == 2


def test_zero_width_raises():
    with pytest.raises(ValueError):
        line_count("hello", 0)


def test_negative_width_raises():
    with pytest.raises(ValueError):
        wrap_lines("hello", -3)
