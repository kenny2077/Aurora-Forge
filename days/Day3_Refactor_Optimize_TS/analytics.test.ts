// Spec for Day 3. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { parseEndpoint, endpointCounts, topEndpoints } from "./analytics.ts";

test("parseEndpoint extracts the path", () => {
  assert.equal(parseEndpoint("GET /api/users 200 12ms"), "/api/users");
  assert.equal(parseEndpoint("POST /login 302 4ms"), "/login");
});

test("parseEndpoint returns null on malformed lines", () => {
  assert.equal(parseEndpoint("garbage"), null);
  assert.equal(parseEndpoint("   "), null);
});

test("endpointCounts tallies hits and skips malformed lines", () => {
  const c = endpointCounts([
    "GET /a 200 1ms",
    "GET /a 200 1ms",
    "junk",
    "GET /b 500 9ms",
  ]);
  assert.equal(c.get("/a"), 2);
  assert.equal(c.get("/b"), 1);
  assert.equal(c.size, 2);
});

test("topEndpoints ordered by hit count descending", () => {
  const lines = ["GET /hot 200 1ms", "GET /hot 200 1ms", "GET /hot 200 1ms", "GET /cold 200 1ms"];
  assert.deepEqual(topEndpoints(lines, 2), ["/hot", "/cold"]);
});

test("ties are broken alphabetically", () => {
  // /c, /a, /b each hit once, inserted in that order -> must come out /a, /b, /c
  const lines = ["GET /c 200 1ms", "GET /a 200 1ms", "GET /b 200 1ms"];
  assert.deepEqual(topEndpoints(lines, 3), ["/a", "/b", "/c"]);
});

test("hit count takes priority over alphabetical", () => {
  const lines = ["GET /z 200 1ms", "GET /z 200 1ms", "GET /z 200 1ms", "GET /a 200 1ms"];
  assert.deepEqual(topEndpoints(lines, 2), ["/z", "/a"]);
});

test("n larger than the number of endpoints returns all, sorted", () => {
  const lines = ["GET /b 200 1ms", "GET /a 200 1ms"];
  assert.deepEqual(topEndpoints(lines, 10), ["/a", "/b"]);
});

test("performance: 60k log lines well under budget", () => {
  const lines: string[] = [];
  for (let i = 0; i < 60000; i++) {
    lines.push(`GET /ep${i % 500} 200 5ms`); // 500 distinct endpoints, evenly hit
  }
  for (let i = 0; i < 300; i++) {
    lines.push("GET /api/health 200 1ms"); // clearly the hottest endpoint
  }

  const start = performance.now();
  const top = topEndpoints(lines, 5);
  const elapsed = performance.now() - start;

  assert.equal(top.length, 5);
  assert.equal(top[0], "/api/health"); // perf test doubles as a correctness check
  // O(n^2) takes ~10+ seconds here; a single-pass Map solution is a few ms.
  assert.ok(
    elapsed < 1000,
    `topEndpoints took ${elapsed.toFixed(0)}ms — still O(n^2)? Budget is 1000ms.`,
  );
});
