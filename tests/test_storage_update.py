import pytest
import src.storage
from src.storage import create_request, get_request, update_request_response

@pytest.fixture(autouse=True)
def mock_storage_path(tmp_path, monkeypatch):
    """Fixture to use a temporary file for storage during tests."""
    test_data_file = tmp_path / "test_diagnostics.json"
    monkeypatch.setattr(src.storage, "DATA_FILE", str(test_data_file))

def test_update_request_success():
    """Test updating a request with a valid ID."""
    # Create a request
    data = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "symptoms": "Engine light on",
    }
    request_id = create_request(data)

    # Update the request
    response_text = "Check the oxygen sensor."
    result = update_request_response(request_id, response_text)

    # Assertions
    assert result is True
    updated_request = get_request(request_id)
    assert updated_request['response'] == response_text
    assert updated_request['status'] == 'completed'

def test_update_request_invalid_id():
    """Test updating a request with an invalid ID."""
    # Attempt update with a non-existent ID
    invalid_id = "non-existent-id"
    response_text = "Should not be saved."
    result = update_request_response(invalid_id, response_text)

    # Assertions
    assert result is False
