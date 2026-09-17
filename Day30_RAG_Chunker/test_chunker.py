"""Spec for the RAG chunker. DO NOT MODIFY."""
import pytest

from chunker import chunk_text


def test_overlapping_windows():
    text = "w1 w2 w3 w4 w5 w6 w7 w8 w9 w10"
    # size 4, overlap 1 -> step 3 -> starts 0,3,6,9
    assert chunk_text(text, 4, 1) == [
        "w1 w2 w3 w4",
        "w4 w5 w6 w7",
        "w7 w8 w9 w10",
        "w10",
    ]


def test_non_overlapping():
    assert chunk_text("a b c d e", 2, 0) == ["a b", "c d", "e"]


def test_last_window_may_be_shorter():
    assert chunk_text("a b c", 2, 0) == ["a b", "c"]


def test_dedup_keeps_first_occurrence():
    # "x x x x", size 2, overlap 1 -> "x x","x x"(dup),"x x"(dup),"x" -> dedup
    assert chunk_text("x x x x", 2, 1) == ["x x", "x"]


def test_text_shorter_than_size_is_one_chunk():
    assert chunk_text("a b", 5, 1) == ["a b"]


def test_empty_text():
    assert chunk_text("", 3, 1) == []


def test_whitespace_is_collapsed():
    assert chunk_text("  a   b  c ", 2, 0) == ["a b", "c"]


def test_overlap_equal_to_size_raises():
    with pytest.raises(ValueError):
        chunk_text("a b c", 2, 2)


def test_size_not_positive_raises():
    with pytest.raises(ValueError):
        chunk_text("a b c", 0, 0)
