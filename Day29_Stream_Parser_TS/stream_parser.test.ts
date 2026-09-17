// Spec for the streaming JSONL parser. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { StreamParser } from "./stream_parser.ts";

test("a single complete line parses", () => {
  const p = new StreamParser();
  assert.deepEqual(p.feed('{"a":1}\n'), [{ a: 1 }]);
});

test("multiple lines in one chunk", () => {
  const p = new StreamParser();
  assert.deepEqual(p.feed('{"x":1}\n{"y":2}\n'), [{ x: 1 }, { y: 2 }]);
});

test("a value split across two chunks", () => {
  const p = new StreamParser();
  assert.deepEqual(p.feed('{"a"'), []);
  assert.deepEqual(p.feed(":1}\n"), [{ a: 1 }]);
});

test("a chunk boundary between two values", () => {
  const p = new StreamParser();
  assert.deepEqual(p.feed('{"a":1}\n{"b"'), [{ a: 1 }]);
  assert.deepEqual(p.feed(':2}\n'), [{ b: 2 }]);
});

test("blank lines are skipped", () => {
  const p = new StreamParser();
  assert.deepEqual(p.feed('{"a":1}\n\n{"b":2}\n'), [{ a: 1 }, { b: 2 }]);
});

test("flush returns a final line that had no trailing newline", () => {
  const p = new StreamParser();
  assert.deepEqual(p.feed('{"c":3}'), []);
  assert.deepEqual(p.flush(), [{ c: 3 }]);
});

test("flush on an empty buffer returns nothing", () => {
  const p = new StreamParser();
  p.feed('{"a":1}\n');
  assert.deepEqual(p.flush(), []);
});

test("handles arrays and scalars as line values", () => {
  const p = new StreamParser();
  assert.deepEqual(p.feed("[1,2,3]\n42\n"), [[1, 2, 3], 42]);
});
