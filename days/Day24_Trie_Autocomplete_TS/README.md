# Day 24 — Trie Autocomplete

**Difficulty:** L4/L5. **Skill:** implement prefix search over a trie — traverse to a prefix node,
then collect completions in order under a limit. Autocomplete/typeahead is a very common systems +
algorithms interview blend.

---

## 🎫 SEARCH-77 — search box needs prefix suggestions

**Component:** `trie.ts` — `insert` is done; `suggest` is not.

> Given a prefix, return up to `limit` inserted words that start with it, in ascending lexicographic
> order. The prefix itself counts if it's a word; an empty prefix matches everything; no match
> returns `[]`. Implement `suggest`.

## How to run (Node 24 — native TS)
```bash
node --test
```

## Interactive mock
```bash
cd .. && python3 interview.py Day24_Trie_Autocomplete_TS
```

## Workflow
1. **Break it into two phases (no AI).** In `AI_LOG.md`: phase one, walk from the root down the
   prefix (what if a character is missing?); phase two, collect words under that node. What traversal
   yields them in lexicographic order, and how do you stop at `limit`?
2. Reconstruct each word (prefix + the path you descended) and emit a node *before* its children so a
   word that is a prefix of another comes first.
3. Verify: prefix match, limit, prefix-is-a-word, no-match, empty prefix, dedup, limit 0.

## Success criteria
- [ ] `node --test` all green.
- [ ] `AI_LOG.md` explains why visiting sorted children (emitting on the way down) yields lexicographic order.
- [ ] `suggest` stops as soon as it has `limit` results (doesn't collect everything then slice).

> Interview tell: "descend to the prefix node, then DFS visiting children in sorted order and
> emitting a node before its subtree — that produces sorted completions, and I bail at the limit."
> The order-and-limit reasoning is the signal.
