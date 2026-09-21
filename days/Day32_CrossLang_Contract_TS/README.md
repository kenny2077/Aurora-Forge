# Day 32 — Cross-Language Contract (TS client ⇄ Python server)

**Difficulty:** L4/L5. **Skill:** make a client conform *exactly* to a contract owned by a service in
another language. Cross-language schema drift is a real source of production incidents, and matching
a spec precisely is a strong signal.

---

## 🎫 API-720 — Python server rejects the mobile client's payload

**Component:** `client.ts` (contract in `CONTRACT.md`).

> The TS client's `POST /users` body has drifted from the Python server's strict schema: camelCase
> keys, the raw epoch-ms timestamp instead of ISO, unsorted `tags`, and a dropped `referrer` when
> null. Make `buildRequestBody` match `CONTRACT.md` exactly.

## How to run (Node 24 — native TS)
```bash
node --test
```

## Interactive mock
```bash
cd .. && python3 interview.py Day32_CrossLang_Contract_TS
```

## Workflow
1. **Diff the client against the contract (no AI).** In `AI_LOG.md`, list every discrepancy between
   the current output and `CONTRACT.md` before editing — casing, timestamp format, sorting,
   null-but-present, and (subtly) not mutating the caller's array.
2. Build the body to match the contract exactly.
3. Verify with the exact-match tests.

## Success criteria
- [ ] `node --test` all green.
- [ ] `AI_LOG.md` enumerates the discrepancies.
- [ ] Output matches `CONTRACT.md` byte-for-byte in structure; caller's `tags` isn't mutated.

> Interview tell: "pull up the contract, enumerate the diffs, and convert at the boundary — snake_case
> keys, ISO timestamp, sorted copy of tags, null-but-present." Treating the other service's schema as
> law is the integration signal.
