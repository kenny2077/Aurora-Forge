// Spec for minimum meeting rooms. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { minMeetingRooms } from "./meeting_rooms.ts";

test("no meetings need no rooms", () => {
  assert.equal(minMeetingRooms([]), 0);
});

test("a single meeting needs one room", () => {
  assert.equal(minMeetingRooms([[1, 5]]), 1);
});

test("touching meetings share a room (end is exclusive)", () => {
  assert.equal(minMeetingRooms([[1, 2], [2, 3], [3, 4]]), 1);
});

test("classic overlapping example needs two rooms", () => {
  assert.equal(minMeetingRooms([[0, 30], [5, 10], [15, 20]]), 2);
});

test("all meetings overlapping need one room each", () => {
  assert.equal(minMeetingRooms([[1, 10], [2, 10], [3, 10]]), 3);
});

test("partial overlaps", () => {
  // [1,5] overlaps [2,3] and [4,6]; [2,3] and [4,6] do not overlap each other -> 2
  assert.equal(minMeetingRooms([[1, 5], [2, 3], [4, 6]]), 2);
});

test("a meeting starting exactly when another ends reuses the room", () => {
  assert.equal(minMeetingRooms([[1, 10], [10, 20]]), 1);
});
