import os
import pytest
import src.storage
from src.storage import create_request, get_request

@pytest.fixture(autouse=True)
def mock_storage_path(tmp_path, monkeypatch):
    """Fixture to use a temporary file for storage during tests."""
    test_data_file = tmp_path / "test_diagnostics.json"
    monkeypatch.setattr(src.storage, "DATA_FILE", str(test_data_file))

def test_create_request_minimal_data():
    """Test create_request with an empty dictionary."""
    minimal_data = {}
    request_id = create_request(minimal_data)

    assert isinstance(request_id, str)
    assert len(request_id) > 0

    stored_request = get_request(request_id)
    assert stored_request is not None
    assert stored_request['request_id'] == request_id
    assert 'timestamp' in stored_request
    assert stored_request['status'] == 'pending'
    assert stored_request['response'] is None

def test_create_request_retains_original_data():
    """Test that create_request retains existing fields while adding mandatory ones."""
    data = {"make": "Honda", "model": "Civic"}
    request_id = create_request(data)

    stored_request = get_request(request_id)
    assert stored_request['make'] == "Honda"
    assert stored_request['model'] == "Civic"
    assert 'request_id' in stored_request
    assert 'timestamp' in stored_request
