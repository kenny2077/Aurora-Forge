"""Spec for the token-budget trimmer. DO NOT MODIFY.

count_tokens is word count, so budgets are easy to reason about.
"""
from trimmer import trim_to_budget


def words(s):
    return len(s.split())


def msg(role, content):
    return {"role": role, "content": content}


SYS = msg("system", "s1 s2")           # 2 tokens
M1 = msg("user", "a a a")              # 3
M2 = msg("assistant", "b b")           # 2
M3 = msg("user", "c")                  # 1


def test_all_fit_keeps_everything():
    out = trim_to_budget([SYS, M1, M2, M3], 100, words)
    assert out == [SYS, M1, M2, M3]


def test_drops_oldest_keeps_recent_and_system():
    # budget 5: system(2) + M2(2) + M3(1) = 5; M1(3) would overflow -> dropped (oldest)
    out = trim_to_budget([SYS, M1, M2, M3], 5, words)
    assert out == [SYS, M2, M3]


def test_system_is_always_kept():
    out = trim_to_budget([SYS, M1, M2, M3], 2, words)  # only room for system
    assert out == [SYS]


def test_system_alone_over_budget_returns_just_system():
    big_sys = msg("system", "s1 s2 s3")  # 3 tokens, budget 2
    out = trim_to_budget([big_sys, M1], 2, words)
    assert out == [big_sys]


def test_order_is_preserved():
    out = trim_to_budget([SYS, M1, M2, M3], 6, words)  # sys2 + M3 1 + M2 2 = 5; +M1 3 = 8 > 6
    assert out == [SYS, M2, M3]
    assert [m["role"] for m in out] == ["system", "assistant", "user"]


def test_no_system_message():
    out = trim_to_budget([M1, M2, M3], 3, words)  # keep recent suffix within 3: M3(1)+M2(2)=3
    assert out == [M2, M3]


def test_empty():
    assert trim_to_budget([], 10, words) == []
