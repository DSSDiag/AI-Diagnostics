import os
import pytest
from io import BytesIO
from src.storage import create_request, get_request

class MockUploadedFile:
    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.file = BytesIO(content)

    def read(self):
        return self.file.read()

@pytest.fixture
def setup_storage(tmp_path, monkeypatch):
    """Fixture to use a temporary directory for storage and uploads."""
    test_data_file = tmp_path / "test_diagnostics.json"
    test_upload_dir = tmp_path / "test_uploads"

    monkeypatch.setattr("src.storage.DATA_FILE", str(test_data_file))
    monkeypatch.setattr("src.storage.UPLOAD_DIR", str(test_upload_dir))

    return test_upload_dir

def test_create_request_with_files(setup_storage):
    """Test creating a request with file uploads."""
    files = [
        MockUploadedFile("image1.jpg", b"fake image content"),
        MockUploadedFile("video.mp4", b"fake video content")
    ]

    data = {
        "make": "Ford",
        "model": "F-150",
        "year": 2020,
        "symptoms": "Engine knocking"
    }

    request_id = create_request(data, files=files)

    # Verify request was created
    req = get_request(request_id)
    assert req is not None
    assert req['has_files'] is True
    assert len(req['file_paths']) == 2

    # Verify files exist on disk
    upload_dir = setup_storage
    req_dir = upload_dir / request_id
    assert req_dir.exists()

    file1_path = req_dir / "image1.jpg"
    file2_path = req_dir / "video.mp4"

    assert file1_path.exists()
    assert file2_path.exists()

    assert file1_path.read_bytes() == b"fake image content"
    assert file2_path.read_bytes() == b"fake video content"

def test_create_request_without_files(setup_storage):
    """Test creating a request without files."""
    data = {
        "make": "Tesla",
        "model": "Model 3",
        "year": 2022,
        "symptoms": "Screen frozen"
    }

    request_id = create_request(data)

    req = get_request(request_id)
    assert req['has_files'] is False
    assert req['file_paths'] == []

    upload_dir = setup_storage
    req_dir = upload_dir / request_id
    assert not req_dir.exists()
