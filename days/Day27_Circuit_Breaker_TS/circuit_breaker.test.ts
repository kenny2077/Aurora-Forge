// Spec for the circuit breaker. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { CircuitBreaker, CircuitOpenError } from "./circuit_breaker.ts";

const ok = () => "ok";
function boom(): never {
  throw new Error("boom");
}

test("passes through while closed", () => {
  const cb = new CircuitBreaker(3, 100);
  assert.equal(cb.call(ok, 0), "ok");
});

test("opens after threshold consecutive failures and stops calling fn", () => {
  const cb = new CircuitBreaker(3, 100);
  for (let i = 0; i < 3; i++) assert.throws(() => cb.call(boom, 0), /boom/);
  let called = false;
  const spy = () => {
    called = true;
    return "x";
  };
  assert.throws(() => cb.call(spy, 0), (e) => e instanceof CircuitOpenError);
  assert.equal(called, false, "fn must not be called while the breaker is open");
});

test("a success resets the failure count", () => {
  const cb = new CircuitBreaker(3, 100);
  assert.throws(() => cb.call(boom, 0)); // 1
  assert.throws(() => cb.call(boom, 0)); // 2
  assert.equal(cb.call(ok, 0), "ok"); //   reset -> 0
  assert.throws(() => cb.call(boom, 0)); // 1
  assert.throws(() => cb.call(boom, 0)); // 2  (still below threshold 3)
  assert.equal(cb.call(ok, 0), "ok"); //   still closed
});

test("half-open after cooldown allows a trial call", () => {
  const cb = new CircuitBreaker(1, 100);
  assert.throws(() => cb.call(boom, 0)); //                  opens until 100
  assert.throws(() => cb.call(ok, 50), (e) => e instanceof CircuitOpenError); // still open
  assert.equal(cb.call(ok, 100), "ok"); //                   half-open trial succeeds
});

test("half-open failure re-opens the breaker", () => {
  const cb = new CircuitBreaker(1, 100);
  assert.throws(() => cb.call(boom, 0)); //     open until 100
  assert.throws(() => cb.call(boom, 100), /boom/); // trial fails -> reopen until 200
  assert.throws(() => cb.call(ok, 150), (e) => e instanceof CircuitOpenError);
});

test("after recovery it takes a full threshold of failures to open again", () => {
  const cb = new CircuitBreaker(2, 100);
  assert.throws(() => cb.call(boom, 0)); // 1
  assert.throws(() => cb.call(boom, 0)); // 2 -> open until 100
  assert.equal(cb.call(ok, 100), "ok"); //  half-open success -> closed & reset
  assert.throws(() => cb.call(boom, 100)); // 1 (must NOT open yet)
  let called = false;
  assert.throws(() =>
    cb.call(() => {
      called = true;
      throw new Error("boom");
    }, 100),
  ); // 2 -> opens, but fn WAS reached because breaker was closed
  assert.equal(called, true, "breaker should have been closed after the reset");
});
