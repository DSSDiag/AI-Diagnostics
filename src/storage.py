import json
import os
import uuid
import time
from datetime import datetime

DATA_FILE = "diagnostics_data.json"
LOCK_FILE = "diagnostics_data.json.lock"

class FileLock:
    """A simple file lock using os.open with O_EXCL for atomicity."""
    def __init__(self, lock_file, timeout=10):
        self.lock_file = lock_file
        self.timeout = timeout
        self.fd = None

    def __enter__(self):
        start_time = time.monotonic()
        while True:
            try:
                self.fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                return self
            except FileExistsError:
                if time.monotonic() - start_time > self.timeout:
                    raise TimeoutError(f"Could not acquire lock on {self.lock_file} within {self.timeout} seconds")
                time.sleep(0.05)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd:
            os.close(self.fd)
            try:
                os.remove(self.lock_file)
            except OSError:
                pass

def _load_data():
    """Loads all data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_data(data):
    """Saves data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def create_request(data):
    """
    Creates a new diagnostic request.

    Args:
        data (dict): Dictionary containing car details and symptoms.

    Returns:
        str: The unique request ID.
    """
    with FileLock(LOCK_FILE):
        requests = _load_data()
        request_id = str(uuid.uuid4())

        data['request_id'] = request_id
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['status'] = 'pending'
        data['response'] = None

        requests[request_id] = data
        _save_data(requests)
        return request_id

def get_request(request_id):
    """Retrieves a specific request by ID."""
    requests = _load_data()
    return requests.get(request_id)

def get_all_requests():
    """Retrieves all requests."""
    return _load_data()

def update_request_response(request_id, response_text):
    """
    Updates a request with the expert's diagnosis.

    Args:
        request_id (str): The ID of the request to update.
        response_text (str): The diagnosis/solution.

    Returns:
        bool: True if successful, False if request not found.
    """
    with FileLock(LOCK_FILE):
        requests = _load_data()
        if request_id in requests:
            requests[request_id]['response'] = response_text
            requests[request_id]['status'] = 'completed'
            requests[request_id]['response_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _save_data(requests)
            return True
        return False
