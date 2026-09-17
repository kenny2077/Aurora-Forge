"""Hidden spec for Day 34. DO NOT read until spec_notes.md is filled in. DO NOT modify.

The behavioral rules are NOT written here — infer them from the cases. The full rules are in
SPEC_REVEAL.md, opened only at the reconciliation step.
"""
import pytest

from leaderboard import Leaderboard


def test_top_orders_by_score_desc():
    lb = Leaderboard()
    lb.add_score("alice", 10)
    lb.add_score("bob", 20)
    lb.add_score("carol", 15)
    assert lb.top(3) == ["bob", "carol", "alice"]


def test_add_score_updates_replace_not_accumulate():
    lb = Leaderboard()
    lb.add_score("alice", 10)
    lb.add_score("alice", 30)
    assert lb.top(1) == ["alice"]
    assert lb.rank("alice") == 1


def test_ties_broken_by_name_ascending():
    lb = Leaderboard()
    lb.add_score("bob", 10)
    lb.add_score("ann", 10)
    assert lb.top(2) == ["ann", "bob"]


def test_top_respects_n():
    lb = Leaderboard()
    for p, s in [("a", 1), ("b", 2), ("c", 3)]:
        lb.add_score(p, s)
    assert lb.top(1) == ["c"]


def test_top_larger_than_population_returns_all():
    lb = Leaderboard()
    lb.add_score("a", 1)
    lb.add_score("b", 2)
    assert lb.top(10) == ["b", "a"]


def test_top_on_empty():
    assert Leaderboard().top(5) == []


def test_rank_is_one_based_highest_first():
    lb = Leaderboard()
    lb.add_score("a", 10)
    lb.add_score("b", 20)
    lb.add_score("c", 15)
    assert lb.rank("b") == 1
    assert lb.rank("c") == 2
    assert lb.rank("a") == 3


def test_tied_players_share_a_rank():
    lb = Leaderboard()
    lb.add_score("a", 10)
    lb.add_score("b", 10)
    lb.add_score("c", 5)
    assert lb.rank("a") == 1
    assert lb.rank("b") == 1
    assert lb.rank("c") == 3      # standard competition ranking: next is 3, not 2


def test_rank_unknown_player_raises():
    with pytest.raises(KeyError):
        Leaderboard().rank("ghost")
