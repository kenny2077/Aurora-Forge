// Spec for Day 15. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { resolveUserFile } from "./safe_path.ts";

const BASE = "/srv/data";

test("a normal relative file resolves inside the base", () => {
  assert.equal(resolveUserFile(BASE, "notes.txt"), "/srv/data/notes.txt");
});

test("a nested relative file resolves inside the base", () => {
  assert.equal(resolveUserFile(BASE, "reports/q1.txt"), "/srv/data/reports/q1.txt");
});

test("normalization that stays inside the base is allowed", () => {
  assert.equal(resolveUserFile(BASE, "reports/../q1.txt"), "/srv/data/q1.txt");
});

test("a single ../ escape is rejected", () => {
  assert.throws(() => resolveUserFile(BASE, "../secret.txt"), /unsafe/);
});

test("a deep ../ escape is rejected", () => {
  assert.throws(() => resolveUserFile(BASE, "../../etc/passwd"), /unsafe/);
});

test("an absolute path is rejected", () => {
  assert.throws(() => resolveUserFile(BASE, "/etc/passwd"), /unsafe/);
});

test("a sneaky mid-path escape is rejected", () => {
  assert.throws(() => resolveUserFile(BASE, "a/../../etc/passwd"), /unsafe/);
});
