// Harness for Day 13. DO NOT MODIFY. Run with:  node --test
//
// It runs YOUR checkMedian (from assertions.ts) against the correct implementation and every
// mutant. You pass when your checks accept the correct one and catch (throw on) all mutants.
import { test } from "node:test";
import assert from "node:assert/strict";
import { correctMedian, mutants } from "./spec.ts";
import { checkMedian } from "./assertions.ts";

test("your checks ACCEPT the correct implementation", () => {
  assert.doesNotThrow(
    () => checkMedian(correctMedian),
    "your checks reject the correct median — they're wrong, not just weak",
  );
});

for (const m of mutants) {
  test(`your checks CATCH mutant: ${m.name}`, () => {
    assert.throws(
      () => checkMedian(m.impl),
      () => true,
      `mutant "${m.name}" survived — strengthen your checks with an input that exposes it`,
    );
  });
}
