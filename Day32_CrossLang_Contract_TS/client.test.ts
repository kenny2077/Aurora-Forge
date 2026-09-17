// Contract tests — must match CONTRACT.md exactly. DO NOT MODIFY. Run with:  node --test
import { test } from "node:test";
import assert from "node:assert/strict";
import { buildRequestBody, type User } from "./client.ts";

function user(overrides: Partial<User> = {}): User {
  return {
    id: 42,
    name: "Ada Lovelace",
    emailVerified: true,
    createdAtMs: Date.UTC(2024, 0, 15, 9, 30, 0), // 2024-01-15T09:30:00.000Z
    tags: ["beta", "admin"],
    referrer: null,
    ...overrides,
  };
}

test("full body matches the contract", () => {
  assert.deepEqual(buildRequestBody(user({ referrer: "twitter" })), {
    user_id: 42,
    full_name: "Ada Lovelace",
    email_verified: true,
    created_at: "2024-01-15T09:30:00.000Z",
    tags: ["admin", "beta"],
    referrer: "twitter",
  });
});

test("keys are snake_case", () => {
  assert.deepEqual(
    Object.keys(buildRequestBody(user())).sort(),
    ["created_at", "email_verified", "full_name", "referrer", "tags", "user_id"],
  );
});

test("created_at is an ISO string, not epoch ms", () => {
  assert.equal(buildRequestBody(user()).created_at, "2024-01-15T09:30:00.000Z");
});

test("tags are sorted", () => {
  assert.deepEqual(buildRequestBody(user({ tags: ["z", "a", "m"] })).tags, ["a", "m", "z"]);
});

test("null referrer is present, not dropped", () => {
  const body = buildRequestBody(user({ referrer: null }));
  assert.ok("referrer" in body);
  assert.equal(body.referrer, null);
});

test("does not mutate the caller's tags array", () => {
  const u = user({ tags: ["z", "a"] });
  buildRequestBody(u);
  assert.deepEqual(u.tags, ["z", "a"]);
});
