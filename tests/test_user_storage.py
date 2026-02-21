import os
import pytest
import src.storage
from src.storage import (
    create_user, get_user, get_all_users, verify_user,
    update_user_status, delete_user, get_user_requests, create_request,
)


@pytest.fixture(autouse=True)
def mock_storage_paths(tmp_path, monkeypatch):
    """Use temporary files for both diagnostics and users during tests."""
    monkeypatch.setattr(src.storage, "DATA_FILE", str(tmp_path / "test_diagnostics.json"))
    monkeypatch.setattr(src.storage, "USERS_FILE", str(tmp_path / "test_users.json"))


# ---------------------------------------------------------------------------
# create_user / get_user
# ---------------------------------------------------------------------------

def test_create_user_success():
    ok, msg = create_user("test@example.com", "Password1", "Alice Smith", "1990-01-15", "Mechanic")
    assert ok is True
    user = get_user("test@example.com")
    assert user is not None
    assert user["name"] == "Alice Smith"
    assert user["email"] == "test@example.com"
    assert user["status"] == "active"
    assert "password_hash" in user
    assert "salt" in user


def test_create_user_duplicate_email():
    create_user("dup@example.com", "Password1", "Bob", "1985-06-01", "Driver")
    ok, msg = create_user("DUP@EXAMPLE.COM", "Password1", "Bob Again", "1985-06-01", "Driver")
    assert ok is False
    assert "already exists" in msg


def test_get_user_case_insensitive():
    create_user("Case@Example.COM", "Password1", "Carol", "1995-03-20", "Engineer")
    user = get_user("case@example.com")
    assert user is not None
    assert user["name"] == "Carol"


def test_get_user_not_found():
    assert get_user("nobody@example.com") is None


def test_get_all_users():
    create_user("a@example.com", "Password1", "A", "1990-01-01", "Occ")
    create_user("b@example.com", "Password2", "B", "1991-01-01", "Occ")
    users = get_all_users()
    assert len(users) == 2


# ---------------------------------------------------------------------------
# verify_user
# ---------------------------------------------------------------------------

def test_verify_user_correct_password():
    create_user("login@example.com", "MyPass99", "Dave", "1988-07-10", "Tech")
    ok, msg = verify_user("login@example.com", "MyPass99")
    assert ok is True


def test_verify_user_wrong_password():
    create_user("wrong@example.com", "Correct1", "Eve", "1992-04-05", "Dev")
    ok, msg = verify_user("wrong@example.com", "wrongpass")
    assert ok is False
    assert "Incorrect password" in msg


def test_verify_user_not_found():
    ok, msg = verify_user("ghost@example.com", "anything")
    assert ok is False
    assert "No account found" in msg


def test_verify_user_paused_account():
    create_user("paused@example.com", "Pause123", "Frank", "1980-12-31", "Manager")
    update_user_status("paused@example.com", "paused")
    ok, msg = verify_user("paused@example.com", "Pause123")
    assert ok is False
    assert "suspended" in msg


# ---------------------------------------------------------------------------
# update_user_status / delete_user
# ---------------------------------------------------------------------------

def test_update_user_status():
    create_user("status@example.com", "Status1!", "Grace", "1993-09-09", "Artist")
    assert update_user_status("status@example.com", "paused") is True
    user = get_user("status@example.com")
    assert user["status"] == "paused"
    assert update_user_status("status@example.com", "active") is True
    assert get_user("status@example.com")["status"] == "active"


def test_update_user_status_not_found():
    assert update_user_status("nobody@example.com", "paused") is False


def test_delete_user():
    create_user("del@example.com", "Delete99", "Hank", "1975-02-28", "Pilot")
    assert delete_user("del@example.com") is True
    assert get_user("del@example.com") is None


def test_delete_user_not_found():
    assert delete_user("nobody@example.com") is False


# ---------------------------------------------------------------------------
# get_user_requests
# ---------------------------------------------------------------------------

def test_get_user_requests():
    create_request({"make": "Toyota", "model": "Camry", "user_email": "owner@example.com"})
    create_request({"make": "Honda", "model": "Civic", "user_email": "owner@example.com"})
    create_request({"make": "Ford", "model": "Ranger", "user_email": "other@example.com"})
    reqs = get_user_requests("owner@example.com")
    assert len(reqs) == 2


def test_get_user_requests_empty():
    reqs = get_user_requests("nobody@example.com")
    assert reqs == {}
