# Automotive AI Diagnostics

A Streamlit-based web application for automotive diagnostics and expert consultation.

## Features

- **User Authentication:** Secure signup and login for members.
- **Issue Submission:** Members can describe car issues, including make, model, year, and structured symptoms.
- **File Uploads:** Members can upload photos, videos, or audio of the issue.
- **Expert Dashboard:** Experts can review pending requests and provide structured diagnoses.
- **Admin Panel:** Administrators can view metrics, manage members (pause, delete), and oversee requests.
- **Custom Tutorials:** Members can request specific guides tailored to their vehicles.

## Setup & Execution

### Prerequisites

- Python 3.9+
- The required dependencies in `requirements.txt`

### Installation

1. Clone the repository.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
streamlit run app.py
```

### Environment Variables

You can configure the following environment variables:

- `EXPERT_PASSWORD`: The password required for the Expert Dashboard (default: "password123"). If unset, access is disabled.
- `ADMIN_PASSWORD`: The password required for the Admin Panel (default: "admin456"). If unset, access is disabled.
- `DIAGNOSTICS_DATA_FILE`: Path to the JSON file for storing diagnostic requests (default: "diagnostics_data.json").
- `DIAGNOSTICS_USERS_FILE`: Path to the JSON file for storing user data (default: "users_data.json").
- `DIAGNOSTICS_TUTORIALS_FILE`: Path to the JSON file for storing tutorial requests (default: "tutorials_data.json").
- `DIAGNOSTICS_UPLOAD_DIR`: Directory where uploaded files are saved (default: "uploads").

## Testing

Tests are written using `pytest`. Run tests from the project root:

```bash
PYTHONPATH=. pytest tests/
```

