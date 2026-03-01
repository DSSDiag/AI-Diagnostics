import hashlib
import json
import os
import uuid
from datetime import datetime

DATA_FILE = os.getenv("DIAGNOSTICS_DATA_FILE", "diagnostics_data.json")
USERS_FILE = os.getenv("DIAGNOSTICS_USERS_FILE", "users_data.json")

# In-memory caches for diagnostic data
_DATA_CACHE = None
_DATA_MTIME = None
_CACHED_DATA_FILE = None

# In-memory caches for user data
_USERS_CACHE = None
_USERS_MTIME = None
_CACHED_USERS_FILE = None

def _load_data():
    """Loads all data from the JSON file with caching."""
    global _DATA_CACHE, _DATA_MTIME, _CACHED_DATA_FILE

    # Invalidate cache if filename has changed
    if DATA_FILE != _CACHED_DATA_FILE:
        _DATA_CACHE = None
        _DATA_MTIME = None
        _CACHED_DATA_FILE = DATA_FILE

    if not os.path.exists(DATA_FILE):
        _DATA_CACHE = {}
        _DATA_MTIME = None
        return _DATA_CACHE

    try:
        current_mtime = os.path.getmtime(DATA_FILE)
        if _DATA_CACHE is not None and _DATA_MTIME == current_mtime:
            return _DATA_CACHE

        with open(DATA_FILE, 'r') as f:
            _DATA_CACHE = json.load(f)
            _DATA_MTIME = current_mtime
            return _DATA_CACHE
    except (json.JSONDecodeError, OSError):
        return {}

def _save_data(data):
    """Saves data to the JSON file and updates the cache."""
    global _DATA_CACHE, _DATA_MTIME, _CACHED_DATA_FILE
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    # Update cache
    _DATA_CACHE = data
    _DATA_MTIME = os.path.getmtime(DATA_FILE)
    _CACHED_DATA_FILE = DATA_FILE

def create_request(data):
    """
    Creates a new diagnostic request.

    Args:
        data (dict): Dictionary containing car details and symptoms.

    Returns:
        str: The unique request ID.
    """
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
    requests = _load_data()
    if request_id in requests:
        requests[request_id]['response'] = response_text
        requests[request_id]['status'] = 'completed'
        requests[request_id]['response_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _save_data(requests)
        return True
    return False

def update_request_files(request_id, filenames):
    """
    Updates a request with uploaded file names.

    Args:
        request_id (str): The ID of the request to update.
        filenames (list): List of filenames uploaded.

    Returns:
        bool: True if successful, False if request not found.
    """
    requests = _load_data()
    if request_id in requests:
        requests[request_id]['has_files'] = True
        requests[request_id]['files'] = filenames
        _save_data(requests)
        return True
    return False


# ---------------------------------------------------------------------------
# User management
# ---------------------------------------------------------------------------

def _load_users():
    """Loads all users from the JSON file with caching."""
    global _USERS_CACHE, _USERS_MTIME, _CACHED_USERS_FILE

    # Invalidate cache if filename has changed
    if USERS_FILE != _CACHED_USERS_FILE:
        _USERS_CACHE = None
        _USERS_MTIME = None
        _CACHED_USERS_FILE = USERS_FILE

    if not os.path.exists(USERS_FILE):
        _USERS_CACHE = {}
        _USERS_MTIME = None
        return _USERS_CACHE

    try:
        current_mtime = os.path.getmtime(USERS_FILE)
        if _USERS_CACHE is not None and _USERS_MTIME == current_mtime:
            return _USERS_CACHE

        with open(USERS_FILE, 'r') as f:
            _USERS_CACHE = json.load(f)
            _USERS_MTIME = current_mtime
            return _USERS_CACHE
    except (json.JSONDecodeError, OSError):
        return {}


def _save_users(data):
    """Saves users data to the JSON file and updates the cache."""
    global _USERS_CACHE, _USERS_MTIME, _CACHED_USERS_FILE
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    # Update cache
    _USERS_CACHE = data
    _USERS_MTIME = os.path.getmtime(USERS_FILE)
    _CACHED_USERS_FILE = USERS_FILE


def _hash_password(password, salt=None):
    """Returns (hex_hash, hex_salt) using PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = os.urandom(16).hex()
    dk = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt.encode('utf-8'), 600000
    )
    return dk.hex(), salt


def create_user(email, password, name, dob, occupation):
    """
    Creates a new member account.

    Returns:
        tuple(bool, str): (success, message)
    """
    users = _load_users()
    email_key = email.lower().strip()
    if email_key in users:
        return False, "An account with this email already exists."
    pw_hash, salt = _hash_password(password)
    users[email_key] = {
        "email": email_key,
        "name": name.strip(),
        "dob": str(dob),
        "occupation": occupation.strip(),
        "password_hash": pw_hash,
        "salt": salt,
        "status": "active",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    _save_users(users)
    return True, "Account created successfully."


def get_user(email):
    """Retrieves a user record by email (case-insensitive)."""
    users = _load_users()
    return users.get(email.lower().strip())


def get_all_users():
    """Retrieves all user records."""
    return _load_users()


def verify_user(email, password):
    """
    Verifies login credentials.

    Returns:
        tuple(bool, str): (success, message)
    """
    user = get_user(email)
    if not user:
        return False, "No account found with this email address."
    if user.get('status') == 'paused':
        return False, "Your account has been suspended. Please contact support."
    pw_hash, _ = _hash_password(password, user['salt'])
    if pw_hash == user['password_hash']:
        return True, "Login successful."
    return False, "Incorrect password."


def update_user_status(email, status):
    """
    Sets the status of a user account ('active' or 'paused').

    Returns:
        bool: True if successful, False if user not found.
    """
    users = _load_users()
    email_key = email.lower().strip()
    if email_key in users:
        users[email_key]['status'] = status
        _save_users(users)
        return True
    return False


def delete_user(email):
    """
    Permanently removes a user account.

    Returns:
        bool: True if successful, False if user not found.
    """
    users = _load_users()
    email_key = email.lower().strip()
    if email_key in users:
        del users[email_key]
        _save_users(users)
        return True
    return False


def get_user_requests(email):
    """Returns all diagnostic requests submitted by a specific user."""
    all_reqs = _load_data()
    email_key = email.lower().strip()
    return {
        k: v for k, v in all_reqs.items()
        if v.get('user_email', '').lower() == email_key
    }
