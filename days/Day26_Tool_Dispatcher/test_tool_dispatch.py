"""Spec for the tool dispatcher. DO NOT MODIFY."""
import pytest

from tool_dispatch import dispatch, ToolError


def registry():
    return {
        "add": {"handler": lambda a, b: a + b, "params": ["a", "b"]},
        "greet": {"handler": lambda name: f"hello {name}", "params": ["name"]},
        "now": {"handler": lambda: "noon", "params": []},
    }


def test_valid_call_returns_result():
    assert dispatch(registry(), {"tool": "add", "args": {"a": 1, "b": 2}}) == 3


def test_zero_arg_tool():
    assert dispatch(registry(), {"tool": "now", "args": {}}) == "noon"


def test_unknown_tool_raises_toolerror():
    with pytest.raises(ToolError):
        dispatch(registry(), {"tool": "nope", "args": {}})


def test_missing_required_arg_raises_toolerror():
    with pytest.raises(ToolError):
        dispatch(registry(), {"tool": "add", "args": {"a": 1}})


def test_unexpected_arg_raises_toolerror():
    with pytest.raises(ToolError):
        dispatch(registry(), {"tool": "greet", "args": {"name": "x", "extra": 1}})


def test_missing_error_is_toolerror_not_typeerror():
    # a raw handler TypeError would leak implementation details; it must be ToolError
    try:
        dispatch(registry(), {"tool": "add", "args": {}})
    except ToolError:
        pass
    except TypeError:
        pytest.fail("missing args leaked a TypeError instead of raising ToolError")


def test_valid_greet():
    assert dispatch(registry(), {"tool": "greet", "args": {"name": "kenny"}}) == "hello kenny"
