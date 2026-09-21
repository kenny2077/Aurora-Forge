"""Spec for the dependency resolver. DO NOT MODIFY."""
import pytest

from resolver import resolve, CycleError


def test_empty_graph():
    assert resolve({}) == []


def test_linear_chain():
    # a depends on b depends on c  ->  c, b, a
    assert resolve({"a": ["b"], "b": ["c"], "c": []}) == ["c", "b", "a"]


def test_diamond_is_deterministic():
    graph = {"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []}
    assert resolve(graph) == ["a", "b", "c", "d"]


def test_alphabetical_tiebreak_when_multiple_ready():
    assert resolve({"b": [], "a": [], "c": []}) == ["a", "b", "c"]


def test_dependency_that_is_not_a_key_is_a_root():
    # 'b' is never a key -> treat it as a task with no deps
    assert resolve({"a": ["b"]}) == ["b", "a"]


def test_cycle_raises():
    with pytest.raises(CycleError):
        resolve({"a": ["b"], "b": ["a"]})


def test_self_dependency_raises():
    with pytest.raises(CycleError):
        resolve({"a": ["a"]})


def test_duplicate_dependency_is_tolerated():
    assert resolve({"a": ["b", "b"], "b": []}) == ["b", "a"]


def test_order_respects_all_dependencies():
    graph = {
        "app": ["db", "cache", "auth"],
        "auth": ["db"],
        "cache": [],
        "db": [],
        "web": ["app", "cache"],
    }
    order = resolve(graph)
    pos = {name: i for i, name in enumerate(order)}
    assert set(order) == {"app", "auth", "cache", "db", "web"}
    for node, deps in graph.items():
        for d in deps:
            assert pos[d] < pos[node], f"{d} must come before {node}"
