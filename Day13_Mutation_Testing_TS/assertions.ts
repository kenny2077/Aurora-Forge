// Day 13 — YOU FILL THIS IN.
//
// Write checks that call `median` on inputs YOU choose and assert correct behavior.
// Requirements enforced by check.test.ts:
//   - checkMedian(correctMedian) must NOT throw.
//   - checkMedian(mutant) MUST throw for every mutant in spec.ts.
//
// The starter check below is far too weak — most mutants slip through it. Strengthen it until
// `node --test` is all green (every mutant "caught").
import assert from "node:assert/strict";
import type { Median } from "./spec.ts";

export function checkMedian(median: Median): void {
  assert.equal(median([1, 2, 3]), 2);
  // TODO: add inputs that distinguish the correct median from each way it can be wrong:
  //   - an UNSORTED input (catches "does-not-sort")
  //   - a SKEWED even-length input where mean != median (catches "returns-mean", "even-upper")
  //   - the EMPTY input (catches "empty-returns-zero")
}
