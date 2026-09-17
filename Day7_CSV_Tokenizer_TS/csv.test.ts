// Spec for Day 7. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { parseCsvLine } from "./csv.ts";

test("plain comma-separated fields", () => {
  assert.deepEqual(parseCsvLine("a,b,c"), ["a", "b", "c"]);
});

test("empty fields are preserved", () => {
  assert.deepEqual(parseCsvLine("a,,c"), ["a", "", "c"]);
});

test("a trailing comma yields a trailing empty field", () => {
  assert.deepEqual(parseCsvLine("a,b,"), ["a", "b", ""]);
});

test("an empty line is a single empty field", () => {
  assert.deepEqual(parseCsvLine(""), [""]);
});

test("whitespace is significant (not trimmed)", () => {
  assert.deepEqual(parseCsvLine("a, b ,c"), ["a", " b ", "c"]);
});

test("quoted field containing a comma stays one field", () => {
  assert.deepEqual(parseCsvLine('"a,b",c'), ["a,b", "c"]);
});

test("surrounding quotes are stripped", () => {
  assert.deepEqual(parseCsvLine('"hello","world"'), ["hello", "world"]);
});

test("escaped double-quotes inside a quoted field", () => {
  assert.deepEqual(parseCsvLine('"she said ""hi""",x'), ['she said "hi"', "x"]);
});

test("quoted empty field", () => {
  assert.deepEqual(parseCsvLine('"",a'), ["", "a"]);
});

test("mixed quoted and unquoted with commas inside quotes", () => {
  assert.deepEqual(
    parseCsvLine('1,"Doe, John","New York, NY",done'),
    ["1", "Doe, John", "New York, NY", "done"],
  );
});
