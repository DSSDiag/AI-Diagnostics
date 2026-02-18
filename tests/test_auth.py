import pytest
import sys
import os

# Ensure src is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import hash_password, verify_password

def test_hash_password():
    """Test that hash_password returns a tuple of two hex strings."""
    password = "test_password"
    salt, hashed = hash_password(password)

    assert isinstance(salt, str)
    assert isinstance(hashed, str)
    assert len(salt) == 64  # 32 bytes hex encoded
    assert len(hashed) == 64 # 32 bytes hex encoded

def test_verify_password_success():
    """Test that verify_password returns True for correct password."""
    password = "correct_horse_battery_staple"
    salt, hashed = hash_password(password)

    assert verify_password(salt, hashed, password) is True

def test_verify_password_failure():
    """Test that verify_password returns False for incorrect password."""
    password = "my_secret_password"
    salt, hashed = hash_password(password)

    assert verify_password(salt, hashed, "wrong_password") is False

def test_verify_password_empty():
    """Test that verify_password handles empty strings correctly."""
    password = ""
    salt, hashed = hash_password(password)

    assert verify_password(salt, hashed, "") is True
    assert verify_password(salt, hashed, "not_empty") is False

def test_verify_password_invalid_hex():
    """Test that verify_password handles invalid hex strings gracefully."""
    assert verify_password("invalid_salt", "invalid_hash", "password") is False
