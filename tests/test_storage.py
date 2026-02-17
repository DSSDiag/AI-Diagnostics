from src.storage import create_request, get_request, update_request_response, get_all_requests
import os

# Clean up any existing data file
if os.path.exists("diagnostics_data.json"):
    os.remove("diagnostics_data.json")

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
print(f"Created request: {request_id}")

# 2. Verify Data Saved
req = get_request(request_id)
assert req['make'] == "Toyota"
assert req['status'] == "pending"
print("Request verified.")

# 3. Simulate Expert Response
success = update_request_response(request_id, "Check the air intake system.")
assert success is True
print("Response updated.")

# 4. Verify Response
req_updated = get_request(request_id)
assert req_updated['status'] == "completed"
assert req_updated['response'] == "Check the air intake system."
print("Response verified.")

# 5. Check All Requests
all_reqs = get_all_requests()
assert len(all_reqs) == 1
print("All requests verification successful.")
