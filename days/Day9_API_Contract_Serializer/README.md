# Day 9 — API Contract Serializer

**Difficulty:** L3 (new-grad / early-career). **Skill:** make code conform to an external contract exactly — the unglamorous,
extremely common reality of backend work. Reading a spec and matching it precisely is a real
big-tech signal (breaking a published API shape is an incident).

---

## 🎫 Ticket API-902 — mobile clients choke on the user payload

**Component:** `serializers.py` (with `models.py`; contract in `SCHEMA.md`).

> The mobile team reports broken `GET /users/{id}` responses: keys are snake_case instead of
> camelCase, `nickname` disappears when it's null (their parser expects the key present), timestamps
> come back as `2024-01-15 09:30:00` instead of `2024-01-15T09:30:00Z`, and `roles` arrive as
> objects instead of a sorted list of names. Make `serialize_user` match `SCHEMA.md` exactly.

## How to run

```bash
python3 -m pytest -q
```

## Interactive mock

```bash
cd .. && python3 interview.py Day9_API_Contract_Serializer
```

## Workflow
1. **Read `SCHEMA.md` first (no AI)** and diff it against the current `serialize_user` output in your
   head. List every discrepancy in `AI_LOG.md` before editing — this is exactly the "read the
   contract, then the code" habit interviewers watch for.
2. Fix each discrepancy: casing, null-but-present, datetime format, nested serialization, sorted
   role names.
3. Verify with the exact-match tests. `assert out == {...}` is unforgiving — that's the point.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` lists all discrepancies you found between code and `SCHEMA.md`.
- [ ] Output matches the contract byte-for-byte in structure.

> Interview tell: "let me pull up the contract and enumerate the diffs before touching code." A
> checklist against the spec beats guessing field by field.
