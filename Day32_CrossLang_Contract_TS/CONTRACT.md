# Contract — `POST /users` (Python server ⇄ TypeScript client)

The Python backend deserializes this request body with a strict schema. The TypeScript client must
produce **exactly** this shape, or the server rejects it. (The tests encode it.)

```jsonc
{
  "user_id": 42,                       // int  — from client User.id
  "full_name": "Ada Lovelace",         // str  — from client User.name
  "email_verified": true,              // bool — from client User.emailVerified
  "created_at": "2024-01-15T09:30:00.000Z",  // ISO-8601 UTC — from User.createdAtMs (epoch ms)
  "tags": ["admin", "beta"],           // string[], sorted ascending
  "referrer": null                     // str OR null — ALWAYS present (User.referrer ?? null)
}
```

Rules that keep breaking the client:
- Keys are **snake_case** (`user_id`, `full_name`, `email_verified`, `created_at`) — the Python
  server does not accept camelCase.
- `created_at` is an **ISO string**, not the raw epoch-milliseconds number the client holds.
- `tags` must be **sorted**.
- `referrer` is **nullable but always present** — emit `null`, never drop the key.
