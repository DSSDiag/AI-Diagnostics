import streamlit as st
import pandas as pd
import os
from src.storage import create_request, get_request, get_all_requests, update_request_response

st.set_page_config(page_title="Automotive AI Diagnostics", layout="wide", page_icon="🚗")

st.title("🚗 Automotive Fault Diagnostics")

# Mock User Login for Expert
# In a real app, this would use a secure authentication system.
EXPERT_PASSWORD = "password123"

# Tabs for different user roles
tab1, tab2, tab3 = st.tabs(["Car Owner (Submit Issue)", "Expert Dashboard (For Mechanics)", "Check Diagnosis Status"])

# --- TAB 1: CAR OWNER ---
with tab1:
    st.header("Describe Your Car Issue")
    st.markdown("Get professional diagnostic advice from certified experts.")

    with st.form("diagnostic_request_form"):
        col1, col2 = st.columns(2)
        with col1:
            make = st.text_input("Car Make (e.g., Toyota)", placeholder="Toyota")
            model = st.text_input("Car Model (e.g., Camry)", placeholder="Camry")
            year = st.number_input("Year", min_value=1900, max_value=2025, step=1, value=2015)

        with col2:
            mileage = st.number_input("Mileage (km/miles)", min_value=0, step=1000)
            vin = st.text_input("VIN (Optional)", placeholder="17-digit VIN")
            engine_type = st.selectbox("Engine Type", ["Gasoline", "Diesel", "Hybrid", "Electric", "Other"])

        st.markdown("---")
        st.subheader("Symptoms & Details")
        symptoms = st.text_area("Describe the problem in detail", height=150, placeholder="Example: Car makes a rattling noise when accelerating above 40mph. Check engine light is on.")
        obd_codes = st.text_input("OBD-II Codes (if known)", placeholder="P0300, P0420")

        # File upload placeholder (Streamlit handles file uploads in memory)
        uploaded_files = st.file_uploader("Upload Photos/Videos/Audio of the issue", accept_multiple_files=True)

        # Payment Simulation
        st.markdown("### Payment")
        st.info("Consultation Fee: $20.00")

        submitted = st.form_submit_button("Pay & Submit Request")

        if submitted:
            if not make or not model or not symptoms:
                st.error("Please fill in at least Make, Model, and Symptoms.")
            else:
                # Simulate Payment Success
                with st.spinner("Processing Payment..."):
                    # Create request object
                    request_data = {
                        "make": make,
                        "model": model,
                        "year": year,
                        "mileage": mileage,
                        "vin": vin,
                        "engine_type": engine_type,
                        "symptoms": symptoms,
                        "obd_codes": obd_codes,
                    }

                    req_id = create_request(request_data, files=uploaded_files)
                    st.success(f"Payment Successful! Your request has been submitted.")
                    st.balloons()
                    st.markdown(f"**Your Request ID is:** `{req_id}`")
                    st.warning("Please save this ID to check your diagnosis status later.")

# --- TAB 2: EXPERT DASHBOARD ---
with tab2:
    st.header("Expert Dashboard")

    # Simple Authentication Check
    if 'expert_logged_in' not in st.session_state:
        st.session_state['expert_logged_in'] = False

    if not st.session_state['expert_logged_in']:
        password = st.text_input("Enter Expert Password", type="password")
        if st.button("Login"):
            if password == EXPERT_PASSWORD:
                st.session_state['expert_logged_in'] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
    else:
        st.success("Logged in as Expert")
        if st.button("Logout"):
            st.session_state['expert_logged_in'] = False
            st.rerun()

        st.markdown("---")
        st.subheader("Pending Requests")

        all_requests = get_all_requests()
        # Convert to DataFrame for easier display
        if all_requests:
            pending_requests = {k: v for k, v in all_requests.items() if v.get('status') == 'pending'}

            if not pending_requests:
                st.info("No pending requests.")
            else:
                for req_id, data in pending_requests.items():
                    with st.expander(f"{data['year']} {data['make']} {data['model']} - {req_id[:8]}..."):
                        st.write(f"**Request ID:** {req_id}")
                        st.write(f"**Submitted:** {data.get('timestamp')}")
                        st.write(f"**Mileage:** {data['mileage']}")
                        st.write(f"**Engine:** {data['engine_type']}")
                        st.write(f"**OBD Codes:** {data['obd_codes']}")
                        st.markdown(f"**Symptoms:**\n>{data['symptoms']}")

                        if data.get('has_files'):
                            st.write("📎 *User uploaded files:*")
                            for file_path in data.get('file_paths', []):
                                try:
                                    filename = os.path.basename(file_path)
                                    # Simple check for image extensions
                                    if any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                                        st.image(file_path, caption=filename, use_container_width=True)
                                    else:
                                        # For other files, provide a download button
                                        if os.path.exists(file_path):
                                            with open(file_path, "rb") as f:
                                                file_content = f.read()
                                                st.download_button(
                                                    label=f"Download {filename}",
                                                    data=file_content,
                                                    file_name=filename
                                                )
                                        else:
                                            st.warning(f"File not found: {filename}")
                                except Exception as e:
                                    st.error(f"Error loading file: {file_path} - {e}")

                        # Response Form
                        with st.form(key=f"response_form_{req_id}"):
                            diagnosis = st.text_area("Expert Diagnosis & Recommendation", height=200, placeholder="Enter your detailed diagnosis here...")
                            submit_diagnosis = st.form_submit_button("Send Diagnosis")

                            if submit_diagnosis:
                                if diagnosis:
                                    success = update_request_response(req_id, diagnosis)
                                    if success:
                                        st.success(f"Diagnosis sent for request {req_id}!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to update request.")
                                else:
                                    st.warning("Please enter a diagnosis.")
        else:
            st.info("No requests found.")

# --- TAB 3: CHECK STATUS ---
with tab3:
    st.header("Check Your Diagnosis Status")

    check_id = st.text_input("Enter your Request ID")

    if st.button("Check Status"):
        if check_id:
            req_data = get_request(check_id.strip())

            if req_data:
                st.subheader(f"Status: {req_data.get('status', 'Unknown').upper()}")

                st.markdown("### Vehicle Details")
                st.write(f"{req_data.get('year')} {req_data.get('make')} {req_data.get('model')}")

                if req_data.get('status') == 'completed':
                    st.markdown("---")
                    st.subheader("✅ Expert Diagnosis")
                    st.info(req_data.get('response'))
                    st.caption(f"Responded on: {req_data.get('response_timestamp')}")
                else:
                    st.info("Your request is currently being reviewed by an expert. Please check back later.")
            else:
                st.error("Request ID not found. Please check and try again.")
