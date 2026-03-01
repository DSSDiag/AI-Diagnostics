import os
import pytest
import uuid
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

def test_update_request_files_non_existent():
    # Attempt to update files for a request ID that doesn't exist
    random_uuid = str(uuid.uuid4())
    success = update_request_files(random_uuid, ["file1.jpg", "file2.png"])
    assert success is False

def test_update_request_files_success():
    # Create a request
    data = {"make": "Ford", "model": "Focus", "has_files": False}
    request_id = create_request(data)

    # Update files
    filenames = ["img1.jpg", "doc.pdf"]
    success = update_request_files(request_id, filenames)
    assert success is True

    # Verify updates
    req = get_request(request_id)
    assert req['has_files'] is True
    assert req['files'] == filenames
