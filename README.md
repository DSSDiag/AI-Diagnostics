# Automotive AI Diagnostics Platform

A web-based platform connecting car owners with expert mechanics for remote vehicle diagnostics.

## Overview

This application allows car owners to submit detailed reports of their vehicle issues (symptoms, OBD codes, media) and receive professional diagnostic advice from verified experts. An admin area provides monitoring and management of all diagnostic requests.

## Key Features

### For Car Owners
- **Easy Submission**: User-friendly form to input vehicle details (Make, Model, Year, Mileage, VIN, Engine Type, Transmission, Fuel Type, Last Service Date).
- **Structured Symptom Reporting**: Select from categorised symptom checklists covering:
  - ⚡ Power symptoms (loss of power, surges, hesitation, etc.)
  - 👋 Tactile symptoms (vibration, pulling, shaking, jerking, etc.)
  - 🔊 Audible symptoms (rattling, knocking, grinding, squealing, etc.)
  - ⛽ Fuel/Consumption symptoms (increased consumption, difficulty starting, stalling, etc.)
  - 👁️ Visual symptoms (smoke, warning lights, fluid leaks, corrosion, etc.)
  - 🌡️ Temperature symptoms (overheating, A/C issues, heater issues, etc.)
- **Additional Details**: Free-text field for extra context beyond the checklists.
- **OBD-II Integration**: Input engine codes for more accurate diagnosis.
- **Media Upload**: Attach photos, videos, or audio recordings of the issue.
- **Payment Simulation**: $20.00 consultation fee checkout step.
- **Status Tracking**: Track the status of your request and view the expert's response using a unique Request ID.

### For Experts (Mechanics)
- **Dashboard**: View a list of pending diagnostic requests.
- **Review Tools**: Analyze full vehicle data, structured symptoms, OBD codes, and service history.
- **Response System**: Provide detailed diagnostic reports and recommendations directly to the customer.

### For Administrators
- **Admin Area**: Password-protected dashboard for webapp monitoring and management.
- **Key Metrics**: At-a-glance totals for all, pending, and completed requests.
- **Activity Feed**: Timeline of the 10 most recent requests.
- **Request Management**: Filterable and sortable list of all requests with full detail view.

## Technology Stack

- **Frontend/Backend**: Streamlit (100% Python)
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
   - Go to the **"Car Owner (Submit Issue)"** tab.
   - Fill in the vehicle details (Make, Model, Year, Mileage, and optional fields).
   - Select at least one option in **each** of the six symptom categories (required).
   - Click **"Pay & Submit Request"**.
   - **Save your Request ID** to check the status later.

3. **Expert Flow**:
   - Go to the **"Expert Dashboard (For Mechanics)"** tab.
   - Login with the password: `password123`.
   - Select a pending request to review.
   - Type your diagnosis and click **"Send Diagnosis"**.

4. **Check Status**:
   - Go to the **"Check Diagnosis Status"** tab.
   - Enter your Request ID to see the expert's response.

5. **Admin Flow**:
   - Go to the **"Admin Area"** tab.
   - Login with the password: `admin456`.
   - View key metrics, recent activity, and full request details.

## Project Structure

- `app.py`: Main application entry point.
- `src/storage.py`: Handles data persistence (saving/loading requests).
- `src/validation.py`: Validates all form inputs before a request is created.
- `requirements.txt`: Python dependencies.
