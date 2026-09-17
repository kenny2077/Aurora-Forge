# Day 15 — Security: Path Traversal

**Difficulty:** L4. **Skill:** spot and close an injection-class vulnerability, and prove it with
tests. Security-mindedness is increasingly probed in big-tech loops — and it's squarely your
PromptGuard territory (catching unsafe input before it does damage).

---

## 🎫 SEC-208 — file endpoint is vulnerable to path traversal

**Component:** `safe_path.ts` — resolves `GET /files?path=<user input>` against a fixed base dir.

> Pen test finding: `?path=../../etc/passwd` and `?path=/etc/passwd` both escape the intended
> directory and serve arbitrary files. `resolveUserFile` just `path.join`s the base and user input.
> Make it return the resolved path only when it stays **inside** `baseDir`, and otherwise throw
> `Error("unsafe path")`.

## How to run (Node 24 — native TS)
```bash
node --test
```
The three safe cases already pass; the four attack cases fail until you add the containment check.

## Interactive mock
```bash
cd .. && python3 interview.py Day15_Security_Path_Traversal_TS
```

## Workflow
1. **Think like an attacker (no AI).** In `AI_LOG.md`, list the escape vectors: `../`, absolute
   paths, and mid-path `a/../../` tricks. Note why `path.join` alone is insufficient.
2. Resolve both the base and the candidate to absolute paths, then verify the candidate is the base
   or lives under `base + separator`. (Guard against the prefix trick: `/srv/data-evil` must not
   count as inside `/srv/data`.)
3. Verify all attack cases throw and all legitimate cases resolve correctly.

## Success criteria
- [ ] `node --test` all green (safe cases resolve, attacks throw).
- [ ] `AI_LOG.md` lists the escape vectors and why join alone fails.
- [ ] Legitimate normalization (`reports/../q1.txt`) still works.

> Interview tell: "resolve to absolute, then assert it's contained under the base with a separator
> boundary — a bare `startsWith(base)` is itself a bug because of sibling-prefix directories."
> Catching the prefix subtlety is the senior security signal.
