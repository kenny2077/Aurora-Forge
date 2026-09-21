"""Contract tests for serialize_user. DO NOT MODIFY. Encodes SCHEMA.md exactly."""
from datetime import datetime

from models import User, Role, Address
from serializers import serialize_user


def make_user(**overrides):
    base = dict(
        id=42,
        name="Ada Lovelace",
        email="ada@example.com",
        created_at=datetime(2024, 1, 15, 9, 30, 0),
        roles=[Role("editor"), Role("admin")],
        nickname=None,
        address=Address(city="London", zip="EC1A"),
    )
    base.update(overrides)
    return User(**base)


def test_full_payload_matches_contract():
    out = serialize_user(make_user(nickname="ada"))
    assert out == {
        "id": 42,
        "displayName": "Ada Lovelace",
        "email": "ada@example.com",
        "nickname": "ada",
        "createdAt": "2024-01-15T09:30:00Z",
        "roles": ["admin", "editor"],           # sorted names
        "address": {"city": "London", "zip": "EC1A"},
    }


def test_keys_are_camelcase():
    out = serialize_user(make_user())
    assert set(out.keys()) == {
        "id", "displayName", "email", "nickname", "createdAt", "roles", "address"
    }


def test_null_nickname_is_present_not_omitted():
    out = serialize_user(make_user(nickname=None))
    assert "nickname" in out
    assert out["nickname"] is None


def test_null_address_is_present_and_null():
    out = serialize_user(make_user(address=None))
    assert "address" in out
    assert out["address"] is None


def test_created_at_is_iso_utc_with_z():
    out = serialize_user(make_user())
    assert out["createdAt"] == "2024-01-15T09:30:00Z"


def test_roles_are_sorted_strings():
    out = serialize_user(make_user(roles=[Role("zeta"), Role("alpha"), Role("mu")]))
    assert out["roles"] == ["alpha", "mu", "zeta"]


def test_nested_address_is_serialized_not_passed_through():
    out = serialize_user(make_user(address=Address(city="Paris", zip="75001")))
    assert out["address"] == {"city": "Paris", "zip": "75001"}
