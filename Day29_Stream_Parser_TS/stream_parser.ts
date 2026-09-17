// Day 29 — streaming JSONL parser.
//
// LLM/backend responses arrive as a stream of newline-delimited JSON objects, but the transport
// hands you arbitrary CHUNKS — a JSON object can be split across two chunks, or several can arrive
// in one. Parse complete lines as they become available and buffer the incomplete tail until the
// rest arrives.
//
// Implement StreamParser to pass stream_parser.test.ts.
//
// Contract:
//   feed(chunk: string): unknown[]
//     - Append the chunk to an internal buffer.
//     - For every COMPLETE line (terminated by "\n") return its JSON.parse'd value, in order.
//     - Blank/whitespace-only lines are skipped.
//     - Keep any trailing partial line (no newline yet) buffered for the next feed().
//   flush(): unknown[]
//     - Parse and return whatever complete-but-unterminated value remains in the buffer (or [] if
//       the buffer is empty/whitespace), and clear the buffer. For end-of-stream without a final \n.

export class StreamParser {
  buffer = "";

  feed(chunk: string): unknown[] {
    throw new Error("not implemented: buffer, split on newlines, JSON.parse complete lines");
  }

  flush(): unknown[] {
    throw new Error("not implemented: parse the remaining buffered value, if any");
  }
}
