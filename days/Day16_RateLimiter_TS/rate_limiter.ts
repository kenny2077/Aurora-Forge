// Day 16 — token-bucket rate limiter.
//
// Protects an API: each caller gets a bucket of `capacity` tokens that refills at `refillPerSec`.
// Each request costs tokens; if the bucket can't cover the cost, the request is rejected.
// Time is INJECTED (seconds) so behavior is deterministic and testable.
//
// Two bugs are in here (a QA found them): tokens can exceed capacity after an idle period, and an
// exact-cost request is wrongly rejected. Fix them to satisfy rate_limiter.test.ts.
//
// Contract:
//   - new RateLimiter(capacity, refillPerSec, now=0) starts FULL (capacity tokens).
//   - tryAcquire(now, cost=1) refills based on elapsed time since the last call (capped at
//     capacity), then consumes `cost` tokens and returns true, or returns false without consuming
//     any tokens if there aren't enough. An exact-cost request (tokens == cost) succeeds.

export class RateLimiter {
  capacity: number;
  refillPerSec: number;
  tokens: number;
  last: number;

  constructor(capacity: number, refillPerSec: number, now: number = 0) {
    this.capacity = capacity;
    this.refillPerSec = refillPerSec;
    this.tokens = capacity;
    this.last = now;
  }

  tryAcquire(now: number, cost: number = 1): boolean {
    const elapsed = now - this.last;
    this.last = now;
    this.tokens = this.tokens + elapsed * this.refillPerSec;
    if (this.tokens > cost) {
      this.tokens -= cost;
      return true;
    }
    return false;
  }
}
