// Spec for the trie autocomplete. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { Trie } from "./trie.ts";

function seeded(): Trie {
  const t = new Trie();
  for (const w of ["apple", "app", "apply", "apt", "bat"]) t.insert(w);
  return t;
}

test("suggests all words for a prefix, lexicographically", () => {
  assert.deepEqual(seeded().suggest("ap", 10), ["app", "apple", "apply", "apt"]);
});

test("respects the limit", () => {
  assert.deepEqual(seeded().suggest("ap", 2), ["app", "apple"]);
});

test("the prefix itself is included when it is a word", () => {
  assert.deepEqual(seeded().suggest("app", 10), ["app", "apple", "apply"]);
});

test("no matches returns empty", () => {
  assert.deepEqual(seeded().suggest("z", 5), []);
});

test("empty prefix matches every word, sorted", () => {
  assert.deepEqual(seeded().suggest("", 10), ["app", "apple", "apply", "apt", "bat"]);
});

test("a full word with no extensions returns just itself", () => {
  assert.deepEqual(seeded().suggest("bat", 10), ["bat"]);
});

test("inserting the same word twice does not duplicate it", () => {
  const t = new Trie();
  t.insert("dog");
  t.insert("dog");
  assert.deepEqual(t.suggest("d", 10), ["dog"]);
});

test("limit of zero returns nothing", () => {
  assert.deepEqual(seeded().suggest("ap", 0), []);
});
