# Day 29 — Streaming JSONL Parser

**Difficulty:** L4/L5. **Skill:** correct buffering of a chunked byte/char stream — the thing that
bites everyone who parses streaming LLM responses. A value can straddle two chunks; several can
arrive in one. Get the buffering invariant right.

---

## 🎫 STREAM-31 — streamed responses drop or corrupt objects

**Component:** `stream_parser.ts`

> We read newline-delimited JSON from a streaming endpoint, but the transport delivers arbitrary
> chunks. Objects split across chunks get corrupted and multi-object chunks get half-parsed. Build a
> parser that emits each complete line as it arrives and buffers the partial tail. Implement
> `feed` and `flush`.

## How to run (Node 24 — native TS)
```bash
node --test
```

## Interactive mock
```bash
cd .. && python3 interview.py Day29_Stream_Parser_TS
```

## Workflow
1. **State the buffering invariant (no AI).** In `AI_LOG.md`: after each `feed`, what is guaranteed
   about the buffer's contents? (Hint: it holds exactly the unterminated tail.) What does `flush` do
   at end-of-stream?
2. Append the chunk, repeatedly split off everything up to each `\n`, parse non-empty lines, and keep
   the remainder buffered.
3. Verify: single line, multi-line chunk, split value, boundary-between-values, blank lines, flush.

## Success criteria
- [ ] `node --test` all green.
- [ ] `AI_LOG.md` states the post-`feed` buffer invariant.
- [ ] A value split across chunks is parsed exactly once, when completed.

> Interview tell: "buffer the tail, emit only newline-terminated lines, and expose a flush for the
> final line with no trailing newline." The chunk-boundary invariant is the whole problem.
