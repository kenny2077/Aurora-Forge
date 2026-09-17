"""Serialize domain models to the API contract in SCHEMA.md.

The mobile team is seeing broken user payloads: wrong key casing, a missing `nickname` key when
it's null, timestamps in the wrong format, and roles coming back as objects. Fix serialize_user so
its output matches SCHEMA.md exactly (the tests encode it).
"""


def serialize_user(user) -> dict:
    data = {
        "id": user.id,
        "display_name": user.name,
        "email": user.email,
        "created_at": str(user.created_at),
        "roles": [r for r in user.roles],
    }
    if user.nickname is not None:
        data["nickname"] = user.nickname
    if user.address is not None:
        data["address"] = user.address
    return data
