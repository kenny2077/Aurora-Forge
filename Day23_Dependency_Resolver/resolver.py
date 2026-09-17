"""Dependency resolver — topological order with cycle detection.

The build system needs to run tasks so that every task runs after all of its dependencies. Given a
graph mapping each task to the list of tasks it depends on, produce a valid run order — or raise
CycleError if the dependencies are impossible to satisfy.

Implement `resolve` to pass test_resolver.py.

Contract:
    resolve(graph: dict[str, list[str]]) -> list[str]
    - Every task appears AFTER all of its dependencies in the returned list.
    - The node set is every key PLUS every task named as a dependency (a dep that isn't a key is a
      task with no dependencies of its own).
    - Deterministic tie-break: whenever more than one task is ready to run, choose the
      alphabetically smallest first.
    - Raise CycleError if the graph contains a cycle (including a self-dependency).
"""


class CycleError(Exception):
    pass


def resolve(graph):
    raise NotImplementedError("Implement topological sort with deterministic ordering.")
