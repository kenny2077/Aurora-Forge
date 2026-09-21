# Day 23 — Dependency Resolver (Topological Sort)

**Difficulty:** L5. **Skill:** model a real problem as a graph, produce a topological order with a
deterministic tie-break, and detect cycles. Dependency/build ordering is a hard-tier interview
classic that shows real modeling ability.

---

## 🎫 BUILD-500 — task runner needs a correct, stable run order

**Component:** `resolver.py`

> The build runner must run each task after all its dependencies, pick a **stable** order (so CI logs
> diff cleanly — alphabetical among ready tasks), and **fail loudly** when the dependency graph has a
> cycle instead of hanging or running a partial build. Implement `resolve`.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day23_Dependency_Resolver
```

## Workflow
1. **Model it (no AI).** In `AI_LOG.md`: which nodes are "ready" to run first? How do you make the
   choice deterministic when several are ready? How do you know a cycle exists rather than just
   incomplete work? Note that a dependency named but never a key is a root task.
2. Choose an approach (Kahn's algorithm with a min-heap gives both the order and the cycle check).
3. Verify: chains, the diamond, tie-breaks, non-key deps, and both cycle forms.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` describes your readiness rule, the deterministic tie-break, and the cycle test.
- [ ] Output is stable (same input → same order every run).

> Interview tell: "Kahn's algorithm — start from in-degree-zero nodes, and if I finish with fewer
> nodes than the graph has, there's a cycle. A min-heap of ready nodes makes the order deterministic."
> Naming the cycle-detection-via-incomplete-order is the L5 signal.
