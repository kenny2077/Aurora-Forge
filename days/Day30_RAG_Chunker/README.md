# Day 30 — RAG Chunker with Overlap & Dedup

**Difficulty:** L4/L5. **Skill:** the ingestion primitive behind every retrieval system — window a
document with overlap and drop duplicates. Simple to state, easy to get the boundary/step math and
the dedup ordering subtly wrong.

---

## 🎫 RAG-22 — chunking wastes the vector store and loses cross-boundary context

**Component:** `chunker.py`

> We embed documents for retrieval, but the current splitter has no overlap (so facts spanning a
> boundary get lost) and re-embeds duplicate boilerplate (wasting the vector DB). Implement
> `chunk_text` to produce overlapping word-windows and drop exact duplicates, keeping the first.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day30_RAG_Chunker
```

## Workflow
1. **Work out the step math (no AI).** In `AI_LOG.md`: if windows are `size` words and overlap is
   `overlap`, how far does each window advance? What makes `overlap >= size` invalid? How do you dedup
   while keeping the first occurrence's order?
2. Generate windows by that step, join words, and dedup with an order-preserving set check.
3. Verify: overlap, non-overlap, short last window, dedup, text-shorter-than-size, empty, and the
   invalid-arg cases.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` states the step formula and the dedup ordering rule.
- [ ] `overlap >= size` and `size <= 0` both raise `ValueError`.

> Interview tell: "windows of `size`, advancing by `size − overlap`; dedup with a seen-set so the
> first occurrence wins and order is preserved; guard `overlap < size`." The step math + ordered
> dedup is the whole task.
