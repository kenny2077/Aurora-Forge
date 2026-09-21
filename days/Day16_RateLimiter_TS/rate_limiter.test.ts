// Spec for the token-bucket rate limiter. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { RateLimiter } from "./rate_limiter.ts";

test("starts full and allows up to capacity", () => {
  const rl = new RateLimiter(2, 1, 0);
  assert.equal(rl.tryAcquire(0), true);
  assert.equal(rl.tryAcquire(0), true);
  assert.equal(rl.tryAcquire(0), false); // bucket empty
});

test("refills over time", () => {
  const rl = new RateLimiter(2, 1, 0);
  rl.tryAcquire(0);
  rl.tryAcquire(0); // now empty
  assert.equal(rl.tryAcquire(0), false);
  assert.equal(rl.tryAcquire(1), true); // 1 token refilled after 1s
  assert.equal(rl.tryAcquire(1), false);
});

test("refill is capped at capacity (no burst after long idle)", () => {
  const rl = new RateLimiter(2, 1, 0);
  rl.tryAcquire(0);
  rl.tryAcquire(0); // empty
  // 100s later: at 1 token/s that's 100 tokens, but capacity is 2
  assert.equal(rl.tryAcquire(100), true);
  assert.equal(rl.tryAcquire(100), true);
  assert.equal(rl.tryAcquire(100), false); // only 2, not 100
});

test("an exact-cost request succeeds", () => {
  const rl = new RateLimiter(3, 1, 0);
  assert.equal(rl.tryAcquire(0, 3), true); // exactly 3 tokens for cost 3
  assert.equal(rl.tryAcquire(0, 1), false);
});

test("cost greater than one", () => {
  const rl = new RateLimiter(5, 1, 0);
  assert.equal(rl.tryAcquire(0, 3), true); // 5 -> 2
  assert.equal(rl.tryAcquire(0, 3), false); // only 2 left
  assert.equal(rl.tryAcquire(0, 2), true); // 2 -> 0
});

test("fractional refill accumulates", () => {
  const rl = new RateLimiter(10, 2, 0);
  for (let i = 0; i < 10; i++) rl.tryAcquire(0); // drain to 0
  assert.equal(rl.tryAcquire(0.5), true); // 0.5s * 2/s = 1 token
  assert.equal(rl.tryAcquire(0.5), false); // no more time passed
});
