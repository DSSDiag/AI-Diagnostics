import pytest
import src.storage
from src.storage import get_request

@pytest.fixture(autouse=True)
def mock_storage_path(tmp_path, monkeypatch):
    """Fixture to use a temporary file for storage during tests."""
    test_data_file = tmp_path / "test_diagnostics.json"
    monkeypatch.setattr(src.storage, "DATA_FILE", str(test_data_file))

def test_get_request_non_existent():
    """Test get_request with a non-existent ID."""
    request = get_request("non-existent-id")
    assert request is None
