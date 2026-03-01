import os
import pytest
import src.storage
from src.storage import create_request, get_request, update_request_response, get_all_requests, update_request_files

@pytest.fixture(autouse=True)
def mock_storage_path(tmp_path, monkeypatch):
    """Fixture to use a temporary file for storage during tests."""
    test_data_file = tmp_path / "test_diagnostics.json"
    monkeypatch.setattr(src.storage, "DATA_FILE", str(test_data_file))

def test_full_workflow():
    # 1. Simulate User Submission
    data = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2015,
        "mileage": 50000,
        "vin": "12345",
        "engine_type": "Gasoline",
        "symptoms": "Strange noise",
        "obd_codes": "P0101",
        "has_files": False
    }

    request_id = create_request(data)
    assert request_id is not None

    # 2. Verify Data Saved
    req = get_request(request_id)
    assert req['make'] == "Toyota"
    assert req['status'] == "pending"

    # 3. Simulate Expert Response
    success = update_request_response(request_id, "Check the air intake system.")
    assert success is True

    # 4. Verify Response
    req_updated = get_request(request_id)
    assert req_updated['status'] == "completed"
    assert req_updated['response'] == "Check the air intake system."

    # 5. Check All Requests
    all_reqs = get_all_requests()
    assert len(all_reqs) == 1

def test_update_request_files_success():
    """Test successful update of a request with files."""
    data = {
        "make": "Ford",
        "model": "Mustang",
        "has_files": False
    }
    request_id = create_request(data)

    filenames = ["image1.png", "video.mp4"]
    success = update_request_files(request_id, filenames)
    assert success is True

    req_updated = get_request(request_id)
    assert req_updated['has_files'] is True
    assert req_updated['files'] == filenames

def test_update_request_files_not_found():
    """Test update_request_files fails when request ID is not found."""
    # Act
    success = update_request_files("non_existent_id", ["file.jpg"])

    # Assert
    assert success is False
