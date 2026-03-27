import os
import pytest
import src.storage
from src.storage import (
    create_tutorial_request,
    get_tutorial_request,
    get_all_tutorial_requests,
    update_tutorial_request_response,
)

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

def test_get_all_tutorial_requests_empty():
    """Test retrieving all tutorial requests when none exist."""
    reqs = get_all_tutorial_requests()
    assert reqs == {}

def test_get_all_tutorial_requests_multiple():
    """Test retrieving all tutorial requests when multiple exist."""
    data1 = {"topic": "Topic 1", "details": "Details 1"}
    data2 = {"topic": "Topic 2", "details": "Details 2"}

    id1 = create_tutorial_request(data1)
    id2 = create_tutorial_request(data2)

    reqs = get_all_tutorial_requests()
    assert len(reqs) == 2
    assert id1 in reqs
    assert id2 in reqs
    assert reqs[id1]["topic"] == "Topic 1"
    assert reqs[id2]["topic"] == "Topic 2"

def test_update_tutorial_request_response_success():
    """Test successfully updating a tutorial request response."""
    data = {"topic": "Brakes", "details": "How to change pads."}
    request_id = create_tutorial_request(data)

    response_text = "https://example.com/brakes-tutorial"
    success = update_tutorial_request_response(request_id, response_text)

    assert success is True
    req = get_tutorial_request(request_id)
    assert req["status"] == "completed"
    assert req["response"] == response_text
    assert "response_timestamp" in req

def test_update_tutorial_request_response_not_found():
    """Test updating a non-existent tutorial request response."""
    success = update_tutorial_request_response("non_existent_id", "some response")
    assert success is False
