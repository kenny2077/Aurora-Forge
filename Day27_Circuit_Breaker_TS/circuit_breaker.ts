// Day 27 — circuit breaker for a flaky LLM/HTTP client.
//
// After too many consecutive failures the breaker "opens" and rejects calls immediately for a
// cooldown, so we stop hammering a struggling backend. After the cooldown it goes "half-open" and
// lets ONE trial call through: success closes the breaker, failure re-opens it. Time is injected
// (ms) for deterministic tests.
//
// Bug report: a successful call does NOT reset the failure count, so the breaker trips on failures
// that were separated by successes and never really recovers. Fix `call`.
//
// Contract (see circuit_breaker.test.ts):
//   new CircuitBreaker(threshold, cooldownMs)
//   call(fn, now):
//     - If the breaker is open (now < openUntil): throw CircuitOpenError WITHOUT calling fn.
//     - Otherwise call fn():
//         * on success: reset the failure count to 0 (closed) and return the result.
//         * on failure: increment failures; if failures >= threshold, open until now + cooldownMs;
//           re-throw the original error.

export class CircuitOpenError extends Error {}

export class CircuitBreaker {
  threshold: number;
  cooldownMs: number;
  failures: number;
  openUntil: number;

  constructor(threshold: number, cooldownMs: number) {
    this.threshold = threshold;
    this.cooldownMs = cooldownMs;
    this.failures = 0;
    this.openUntil = 0;
  }

  call<T>(fn: () => T, now: number): T {
    if (now < this.openUntil) {
      throw new CircuitOpenError("circuit is open");
    }
    try {
      const result = fn();
      return result;
    } catch (err) {
      this.failures++;
      if (this.failures >= this.threshold) {
        this.openUntil = now + this.cooldownMs;
      }
      throw err;
    }
  }
}
