# Simulation Instructions

This document describes how to simulate the diagnostics repository.

## Prerequisites

Ensure you have Python installed.

## Steps to Simulate

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Verify Backend Logic:**
    Run the `tests/test_storage.py` script to verify the core functionality of the application (request creation, expert response, status check).
    ```bash
    PYTHONPATH=. python3 tests/test_storage.py
    ```

3.  **Start Application:**
    Start the Streamlit application on port 3000 to allow live preview.
    ```bash
    streamlit run app.py --server.port 3000 --server.address 0.0.0.0
    ```

4.  **Verify Access:**
    Use `curl` to verify the application is running.
    ```bash
    curl -I http://0.0.0.0:3000
    ```

## Notes

- The application uses `diagnostics_data.json` for data persistence. This file is generated automatically when the application runs.
- Make sure to set `PYTHONPATH=.` when running tests from the root directory to resolve imports correctly.
