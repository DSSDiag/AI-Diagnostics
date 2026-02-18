import json
import os
import uuid
from datetime import datetime

DATA_FILE = "diagnostics_data.json"
UPLOAD_DIR = "uploads"

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

def _save_file(file_obj, request_id):
    """
    Saves an uploaded file to the local storage.

    Args:
        file_obj: The file object (from Streamlit uploader or similar).
        request_id (str): The ID of the request.

    Returns:
        str: The relative path to the saved file.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Create a directory for this request to avoid name collisions
    request_dir = os.path.join(UPLOAD_DIR, request_id)
    if not os.path.exists(request_dir):
        os.makedirs(request_dir)

    # Sanitize filename to prevent path traversal
    filename = os.path.basename(file_obj.name)
    file_path = os.path.join(request_dir, filename)

    with open(file_path, "wb") as f:
        f.write(file_obj.read())

    return file_path

def create_request(data, files=None):
    """
    Creates a new diagnostic request.

    Args:
        data (dict): Dictionary containing car details and symptoms.
        files (list, optional): List of file objects to upload.

    Returns:
        str: The unique request ID.
    """
    requests = _load_data()
    request_id = str(uuid.uuid4())

    data['request_id'] = request_id
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['status'] = 'pending'
    data['response'] = None

    # Handle file uploads
    file_paths = []
    if files:
        for file_obj in files:
            try:
                path = _save_file(file_obj, request_id)
                file_paths.append(path)
            except Exception as e:
                print(f"Error saving file {file_obj.name}: {e}")

    data['file_paths'] = file_paths
    data['has_files'] = bool(file_paths)

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
    requests = _load_data()
    if request_id in requests:
        requests[request_id]['response'] = response_text
        requests[request_id]['status'] = 'completed'
        requests[request_id]['response_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _save_data(requests)
        return True
    return False
