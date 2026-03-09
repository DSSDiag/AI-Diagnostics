import os
import pytest
import src.storage
from src.storage import create_tutorial_request, get_tutorial_request

@pytest.fixture(autouse=True)
def mock_storage_path(tmp_path, monkeypatch):
    """Fixture to use a temporary file for storage during tests."""
    test_tutorials_file = tmp_path / "test_tutorials.json"
    monkeypatch.setattr(src.storage, "TUTORIALS_FILE", str(test_tutorials_file))

def test_get_tutorial_request_success():
    """Test retrieving an existing tutorial request."""
    data = {
        "topic": "Oil Change",
        "details": "Need a guide on changing oil."
    }
    request_id = create_tutorial_request(data)

    req = get_tutorial_request(request_id)
    assert req is not None
    assert req["topic"] == "Oil Change"
    assert req["request_id"] == request_id
    assert req["status"] == "pending"

def test_get_tutorial_request_not_found():
    """Test retrieving a tutorial request that doesn't exist."""
    data = {
        "topic": "Tire Replacement",
        "details": "How to change a flat tire."
    }
    create_tutorial_request(data)

    req = get_tutorial_request("invalid_id")
    assert req is None

def test_get_tutorial_request_empty_file():
    """Test retrieving a tutorial request when no requests exist yet."""
    # Since no request has been created, the file should not exist,
    # and _load_tutorials() will return {}
    req = get_tutorial_request("any_id")
    assert req is None
