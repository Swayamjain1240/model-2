from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_is_not_plaintext_and_verifies():
    encoded = hash_password("correct-horse-battery")

    assert encoded != "correct-horse-battery"
    assert verify_password("correct-horse-battery", encoded)
    assert not verify_password("wrong-password", encoded)


def test_access_token_round_trip_and_invalid_token():
    token = create_access_token("user-123")

    assert decode_access_token(token) == "user-123"
    assert decode_access_token("not-a-token") is None
