import os
import pytest
import src.storage
from src.storage import create_request, get_request, update_request_response, get_all_requests

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
