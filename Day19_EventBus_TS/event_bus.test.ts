// Spec for the event bus. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { EventBus } from "./event_bus.ts";

test("on/emit delivers the payload to a handler", () => {
  const bus = new EventBus();
  const seen: unknown[] = [];
  bus.on("ping", (p) => seen.push(p));
  bus.emit("ping", 42);
  assert.deepEqual(seen, [42]);
});

test("all handlers for an event are called", () => {
  const bus = new EventBus();
  let a = 0, b = 0;
  bus.on("x", () => a++);
  bus.on("x", () => b++);
  bus.emit("x", null);
  assert.equal(a, 1);
  assert.equal(b, 1);
});

test("the returned unsubscribe removes the handler", () => {
  const bus = new EventBus();
  let n = 0;
  const off = bus.on("x", () => n++);
  bus.emit("x", null);
  off();
  bus.emit("x", null);
  assert.equal(n, 1);
});

test("emitting to an event with no handlers is a no-op", () => {
  const bus = new EventBus();
  assert.doesNotThrow(() => bus.emit("nobody", 1));
});

test("a handler that unsubscribes another still lets it run in the current emit", () => {
  const bus = new EventBus();
  const calls: string[] = [];
  let offB = () => {};
  bus.on("x", () => {
    calls.push("a");
    offB(); // unsubscribe B mid-emit
  });
  offB = bus.on("x", () => calls.push("b"));
  bus.emit("x", null);
  assert.deepEqual(calls, ["a", "b"]); // B still runs THIS emit (snapshot semantics)
  calls.length = 0;
  bus.emit("x", null);
  assert.deepEqual(calls, ["a"]); // B is gone next time
});

test("once fires exactly once", () => {
  const bus = new EventBus();
  let n = 0;
  bus.once("x", () => n++);
  bus.emit("x", null);
  bus.emit("x", null);
  bus.emit("x", null);
  assert.equal(n, 1);
});

test("once can be cancelled before it fires", () => {
  const bus = new EventBus();
  let n = 0;
  const off = bus.once("x", () => n++);
  off();
  bus.emit("x", null);
  assert.equal(n, 0);
});
