import pytest
import src.storage
from src.storage import (
    create_tutorial_request,
    get_tutorial_request,
    update_tutorial_request_response,
    get_all_tutorial_requests
)

@pytest.fixture(autouse=True)
def mock_tutorials_storage(tmp_path, monkeypatch):
    """Fixture to use a temporary file for tutorial storage during tests."""
    test_tutorials_file = tmp_path / "test_tutorials.json"
    monkeypatch.setattr(src.storage, "TUTORIALS_FILE", str(test_tutorials_file))

def test_create_tutorial_request():
    data = {
        "user_email": "test@example.com",
        "topic": "Oil Change",
        "description": "How to change oil in a 2010 Prius?"
    }
    request_id = create_tutorial_request(data)
    assert isinstance(request_id, str)

    req = get_tutorial_request(request_id)
    assert req is not None
    assert req['user_email'] == "test@example.com"
    assert req['topic'] == "Oil Change"
    assert req['status'] == "pending"
    assert req['response'] is None
    assert 'timestamp' in req

def test_update_tutorial_request_response_success():
    data = {
        "user_email": "test@example.com",
        "topic": "Brake Pads"
    }
    request_id = create_tutorial_request(data)

    response_text = "https://example.com/tutorial/brake-pads"
    success = update_tutorial_request_response(request_id, response_text)

    assert success is True

    req = get_tutorial_request(request_id)
    assert req['status'] == "completed"
    assert req['response'] == response_text
    assert 'response_timestamp' in req

def test_update_tutorial_request_response_failure():
    success = update_tutorial_request_response("non-existent-id", "Some response")
    assert success is False

def test_get_all_tutorial_requests():
    create_tutorial_request({"topic": "Topic 1"})
    create_tutorial_request({"topic": "Topic 2"})

    all_reqs = get_all_tutorial_requests()
    assert len(all_reqs) == 2
