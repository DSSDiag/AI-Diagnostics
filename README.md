# Automotive AI Diagnostics Platform

A web-based platform connecting car owners with expert mechanics for remote vehicle diagnostics.

## Overview

This application allows car owners to submit detailed reports of their vehicle issues (symptoms, OBD codes, media) and receive professional diagnostic advice from verified experts.

## Key Features

### For Car Owners
- **Easy Submission**: User-friendly form to input vehicle details (Make, Model, Year, Mileage).
- **Detailed Reporting**: Describe symptoms and upload relevant photos or videos.
- **OBD-II Integration**: Input engine codes for more accurate diagnosis.
- **Status Tracking**: Track the status of your request and view the expert's response using a unique Request ID.

### For Experts (Mechanics)
- **Dashboard**: View a list of pending diagnostic requests.
- **Review Tools**: Analyze vehicle data and symptoms.
- **Response System**: Provide detailed diagnostic reports and recommendations directly to the customer.

## Technology Stack

- **Frontend/Backend**: Streamlit (Python)
- **Data Storage**: JSON (Local file storage for demo purposes)

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. **Car Owner Flow**:
   - Go to the **"Car Owner"** tab.
   - Fill in the vehicle details and symptoms.
   - Click **"Pay & Submit Request"**.
   - **Save your Request ID** to check the status later.

3. **Expert Flow**:
   - Go to the **"Expert Dashboard"** tab.
   - Login with the password: `password123`.
   - Select a pending request to review.
   - Type your diagnosis and click **"Send Diagnosis"**.

4. **Check Status**:
   - Go to the **"Check Diagnosis Status"** tab.
   - Enter your Request ID to see the expert's response.

## Project Structure

- `app.py`: Main application entry point.
- `src/storage.py`: Handles data persistence (saving/loading requests).
- `requirements.txt`: Python dependencies.
