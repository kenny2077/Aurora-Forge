# API contract — `GET /users/{id}` response

The frontend and our mobile clients depend on this **exact** JSON shape. The serializer must match
it byte-for-byte in structure. (This is the source of truth — the tests encode it.)

```jsonc
{
  "id": 42,                              // int
  "displayName": "Ada Lovelace",         // string  (from User.name)
  "email": "ada@example.com",            // string
  "nickname": null,                      // string OR null — ALWAYS present, never omitted
  "createdAt": "2024-01-15T09:30:00Z",   // ISO-8601 UTC, 'T' separator, trailing 'Z'
  "roles": ["admin", "editor"],          // array of role NAMES (strings), sorted ascending
  "address": {                            // object OR null
    "city": "London",
    "zip": "EC1A"
  }
}
```

Rules that keep biting us:
- Keys are **camelCase** (`displayName`, `createdAt`), not snake_case.
- `nickname` and `address` are **nullable but always present** — emit `null`, don't drop the key.
- `createdAt` uses `...T...Z`, not Python's default `str(datetime)` (which gives `2024-01-15 09:30:00`).
- `roles` is a **sorted list of strings**, not Role objects.
- Nested `address` is itself serialized to `{city, zip}`, not passed through as an object.
