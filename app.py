import streamlit as st
from src.storage import create_request, get_request, get_all_requests, update_request_response
from src.validation import validate_input

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

    # Australian Market Vehicle Data
    AUSTRALIAN_MAKES = [
        "Select Make", "Abarth", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "BYD", "Chery", 
        "Chevrolet", "Chrysler", "Citroen", "Cupra", "Dacia", "Daewoo", "Daihatsu", "Dodge", "Ferrari", 
        "Fiat", "Ford", "Genesis", "GWM", "Holden", "Honda", "Hyundai", "Infiniti", "Isuzu", "Jaguar", 
        "Jeep", "Kia", "Lamborghini", "Land Rover", "LDV", "Lexus", "Mahindra", "Maserati", "Mazda", 
        "McLaren", "Mercedes-Benz", "MG", "Mini", "Mitsubishi", "Nissan", "Opel", "Peugeot", "Porsche", 
        "RAM", "Renault", "Rolls-Royce", "Skoda", "SsangYong", "Subaru", "Suzuki", "Tesla", "Toyota", 
        "Volkswagen", "Volvo", "Other"
    ]
    
    # Popular models by make (simplified for Australian market)
    MODELS_BY_MAKE = {
        "Toyota": ["Select Model", "Camry", "Corolla", "RAV4", "Hilux", "Land Cruiser", "Prado", "Kluger", "C-HR", "Yaris", "HiAce", "Fortuner", "86", "Supra", "Other"],
        "Holden": ["Select Model", "Commodore", "Cruze", "Astra", "Colorado", "Captiva", "Trax", "Barina", "Other"],
        "Ford": ["Select Model", "Ranger", "Mustang", "Focus", "Fiesta", "Everest", "Escape", "Mondeo", "Territory", "Other"],
        "Mazda": ["Select Model", "Mazda3", "Mazda6", "CX-3", "CX-5", "CX-9", "CX-30", "CX-60", "BT-50", "MX-5", "2", "Other"],
        "Hyundai": ["Select Model", "i30", "Tucson", "Santa Fe", "Kona", "Elantra", "Venue", "Palisade", "Staria", "Other"],
        "Mitsubishi": ["Select Model", "Outlander", "ASX", "Pajero", "Triton", "Eclipse Cross", "Lancer", "Mirage", "Other"],
        "Nissan": ["Select Model", "X-Trail", "Navara", "Patrol", "Qashqai", "Pathfinder", "Juke", "Leaf", "Altima", "Other"],
        "Subaru": ["Select Model", "Outback", "Forester", "XV", "Impreza", "WRX", "Liberty", "Levorg", "BRZ", "Other"],
        "Volkswagen": ["Select Model", "Golf", "Polo", "Tiguan", "Amarok", "Passat", "Transporter", "T-Cross", "Touareg", "Other"],
        "Honda": ["Select Model", "Civic", "Accord", "CR-V", "HR-V", "Jazz", "City", "Odyssey", "Other"],
        "Kia": ["Select Model", "Sportage", "Seltos", "Cerato", "Sorento", "Carnival", "Picanto", "Stinger", "Niro", "EV6", "Other"],
        "BMW": ["Select Model", "3 Series", "5 Series", "X3", "X5", "1 Series", "2 Series", "4 Series", "7 Series", "X1", "X7", "Other"],
        "Mercedes-Benz": ["Select Model", "C-Class", "E-Class", "GLC", "GLE", "A-Class", "CLA", "GLA", "S-Class", "GLB", "Other"],
        "Audi": ["Select Model", "A3", "A4", "Q3", "Q5", "Q7", "A5", "A6", "Q2", "e-tron", "Other"],
        "Tesla": ["Select Model", "Model 3", "Model Y", "Model S", "Model X", "Other"],
        "Lexus": ["Select Model", "NX", "RX", "UX", "ES", "IS", "LX", "LS", "Other"],
        "Isuzu": ["Select Model", "D-Max", "MU-X", "Other"],
        "Jeep": ["Select Model", "Grand Cherokee", "Wrangler", "Cherokee", "Compass", "Gladiator", "Other"],
        "Land Rover": ["Select Model", "Range Rover", "Range Rover Sport", "Discovery", "Defender", "Evoque", "Discovery Sport", "Other"],
        "Peugeot": ["Select Model", "308", "3008", "5008", "2008", "208", "Expert", "Other"],
        "Renault": ["Select Model", "Koleos", "Megane", "Captur", "Kangoo", "Master", "Other"],
        "Skoda": ["Select Model", "Octavia", "Kodiaq", "Karoq", "Superb", "Fabia", "Scala", "Other"],
        "MG": ["Select Model", "MG3", "ZS", "HS", "5", "6", "Other"],
        "GWM": ["Select Model", "Ute", "Haval H6", "Haval Jolion", "Other"],
        "LDV": ["Select Model", "T60", "D90", "Deliver 9", "G10", "Other"],
        "BYD": ["Select Model", "Atto 3", "Dolphin", "Seal", "Other"],
    }
    
    YEARS = ["Select Year"] + [str(year) for year in range(2025, 1979, -1)]
    
    with st.form("diagnostic_request_form"):
        st.subheader("📋 Vehicle Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            make = st.selectbox("Car Make", AUSTRALIAN_MAKES, index=0)
            
            # Dynamic model dropdown based on selected make
            if make in MODELS_BY_MAKE:
                model_options = MODELS_BY_MAKE[make]
            else:
                model_options = ["Select Model", "Other"]
            model = st.selectbox("Car Model", model_options, index=0)
            
            year_str = st.selectbox("Year", YEARS, index=0)
            year = int(year_str) if year_str != "Select Year" else 0

        with col2:
            mileage = st.number_input("Mileage (km/miles)", min_value=0, step=1000)
            vin = st.text_input("VIN (Optional)", placeholder="17-digit VIN")
            engine_type = st.selectbox("Engine Type", ["Gasoline", "Diesel", "Hybrid", "Electric", "Other"])

        with col3:
            transmission_type = st.selectbox("Transmission", ["Automatic", "Manual", "CVT", "Semi-Automatic", "Unknown"])
            fuel_type = st.selectbox("Fuel Type", ["Regular", "Premium", "Diesel", "Electric", "Hybrid", "Other"])
            last_service_date = st.text_input("Last Service Date (Optional)", placeholder="YYYY-MM-DD or e.g., 3 months ago")

        st.markdown("---")
        st.subheader("🔍 Symptom Categories")
        st.markdown("**Select at least one option in each category:**")
        
        # Power Symptoms
        st.markdown("**⚡ Power Symptoms**")
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            power_loss = st.checkbox("Loss of power")
            power_intermittent = st.checkbox("Intermittent power loss")
        with col_p2:
            power_surge = st.checkbox("Power surges")
            power_more = st.checkbox("Increased power (unusual)")
        with col_p3:
            power_hesitation = st.checkbox("Hesitation/lag")
            power_no_change = st.checkbox("No change")
        
        # Tactile Symptoms
        st.markdown("**👋 Tactile Symptoms**")
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            tactile_vibration = st.checkbox("Vibration")
            tactile_rough = st.checkbox("Rough engine performance")
        with col_t2:
            tactile_pulling = st.checkbox("Pulling to one side")
            tactile_shaking = st.checkbox("Shaking/trembling")
        with col_t3:
            tactile_jerking = st.checkbox("Jerking motion")
            tactile_hunting = st.checkbox("Hunting")
            tactile_stiff = st.checkbox("Stiff steering/pedals")
            tactile_no_change = st.checkbox("No change", key="tactile_no_change")
        
        # Audible Symptoms
        st.markdown("**🔊 Audible Symptoms**")
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            audible_rattling = st.checkbox("Rattling")
            audible_knocking = st.checkbox("Knocking")
        with col_a2:
            audible_grinding = st.checkbox("Grinding")
            audible_squealing = st.checkbox("Squealing/squeaking")
        with col_a3:
            audible_humming = st.checkbox("Humming/buzzing")
            audible_clicking = st.checkbox("Clicking")
            audible_no_change = st.checkbox("No change", key="audible_no_change")
        
        # Fuel Consumption Symptoms
        st.markdown("**⛽ Fuel/Consumption Symptoms**")
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            fuel_increased = st.checkbox("Increased fuel consumption")
            fuel_smell = st.checkbox("Fuel smell")
        with col_f2:
            fuel_decreased_mileage = st.checkbox("Decreased mileage/efficiency")
            fuel_leak = st.checkbox("Fuel leak")
        with col_f3:
            fuel_difficulty_starting = st.checkbox("Difficulty starting")
            fuel_stalling = st.checkbox("Engine stalling")
            fuel_no_change = st.checkbox("No change", key="fuel_no_change")
        
        # Visual Symptoms
        st.markdown("**👁️ Visual Symptoms**")
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            visual_smoke_white = st.checkbox("White smoke")
            visual_smoke_black = st.checkbox("Black smoke")
        with col_v2:
            visual_smoke_blue = st.checkbox("Blue smoke")
            visual_warning_lights = st.checkbox("Warning lights on")
        with col_v3:
            visual_fluid_leak = st.checkbox("Fluid leaks")
            visual_corrosion = st.checkbox("Corrosion/rust")
            visual_no_change = st.checkbox("No change", key="visual_no_change")
        
        # Temperature Symptoms
        st.markdown("**🌡️ Temperature Symptoms**")
        col_temp1, col_temp2, col_temp3 = st.columns(3)
        with col_temp1:
            temp_overheating = st.checkbox("Engine overheating")
            temp_running_hot = st.checkbox("Running hotter than normal")
        with col_temp2:
            temp_running_cold = st.checkbox("Running colder than normal")
            temp_ac_issues = st.checkbox("A/C not working properly")
        with col_temp3:
            temp_heater_issues = st.checkbox("Heater not working properly")
            temp_no_change = st.checkbox("No change", key="temp_no_change")
        
        st.markdown("---")
        st.subheader("📝 Additional Details")
        additional_symptoms = st.text_area("Describe any additional symptoms or context", height=150, placeholder="Example: The rattling noise only happens when accelerating above 40mph. The check engine light came on yesterday.")
        obd_codes = st.text_input("OBD-II Codes (if known)", placeholder="P0300, P0420")

        # File upload placeholder (Streamlit handles file uploads in memory)
        uploaded_files = st.file_uploader("Upload Photos/Videos/Audio of the issue", accept_multiple_files=True)

        # Payment Simulation
        st.markdown("### Payment")
        st.info("Consultation Fee: $20.00")

        submitted = st.form_submit_button("Pay & Submit Request")

        if submitted:
            # Collect all symptoms into structured data
            symptoms_data = {
                "power": {
                    "loss_of_power": power_loss,
                    "intermittent_power_loss": power_intermittent,
                    "power_surges": power_surge,
                    "increased_power": power_more,
                    "hesitation_lag": power_hesitation,
                    "no_change": power_no_change
                },
                "tactile": {
                    "vibration": tactile_vibration,
                    "rough_engine": tactile_rough,
                    "pulling_to_side": tactile_pulling,
                    "shaking": tactile_shaking,
                    "jerking": tactile_jerking,
                    "hunting": tactile_hunting,
                    "stiff_controls": tactile_stiff,
                    "no_change": tactile_no_change
                },
                "audible": {
                    "rattling": audible_rattling,
                    "knocking": audible_knocking,
                    "grinding": audible_grinding,
                    "squealing": audible_squealing,
                    "humming": audible_humming,
                    "clicking": audible_clicking,
                    "no_change": audible_no_change
                },
                "fuel": {
                    "increased_consumption": fuel_increased,
                    "fuel_smell": fuel_smell,
                    "decreased_mileage": fuel_decreased_mileage,
                    "fuel_leak": fuel_leak,
                    "difficulty_starting": fuel_difficulty_starting,
                    "stalling": fuel_stalling,
                    "no_change": fuel_no_change
                },
                "visual": {
                    "white_smoke": visual_smoke_white,
                    "black_smoke": visual_smoke_black,
                    "blue_smoke": visual_smoke_blue,
                    "warning_lights": visual_warning_lights,
                    "fluid_leak": visual_fluid_leak,
                    "corrosion": visual_corrosion,
                    "no_change": visual_no_change
                },
                "temperature": {
                    "overheating": temp_overheating,
                    "running_hot": temp_running_hot,
                    "running_cold": temp_running_cold,
                    "ac_issues": temp_ac_issues,
                    "heater_issues": temp_heater_issues,
                    "no_change": temp_no_change
                },
                "additional_details": additional_symptoms
            }
            
            errors = validate_input(make, model, year, mileage, vin, engine_type, transmission_type, 
                                   fuel_type, last_service_date, symptoms_data, obd_codes)

            if errors:
                for error in errors:
                    st.error(error)
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
                        "transmission_type": transmission_type,
                        "fuel_type": fuel_type,
                        "last_service_date": last_service_date,
                        "symptoms": symptoms_data,
                        "obd_codes": obd_codes,
                        # For a real app, you'd save file paths here after uploading to S3/Cloud storage
                        "has_files": True if uploaded_files else False
                    }

                    req_id = create_request(request_data)
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
        if all_requests:
            pending_requests = {k: v for k, v in all_requests.items() if v.get('status') == 'pending'}

            if not pending_requests:
                st.info("No pending requests.")
            else:
                for req_id, data in pending_requests.items():
                    with st.expander(f"{data['year']} {data['make']} {data['model']} - {req_id[:8]}..."):
                        st.write(f"**Request ID:** {req_id}")
                        st.write(f"**Submitted:** {data.get('timestamp')}")
                        
                        # Vehicle Details
                        st.markdown("### 🚗 Vehicle Details")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Make/Model:** {data['make']} {data['model']}")
                            st.write(f"**Year:** {data['year']}")
                            st.write(f"**Mileage:** {data['mileage']}")
                        with col2:
                            st.write(f"**Engine:** {data['engine_type']}")
                            st.write(f"**Transmission:** {data.get('transmission_type', 'N/A')}")
                            st.write(f"**Fuel Type:** {data.get('fuel_type', 'N/A')}")
                        if data.get('last_service_date'):
                            st.write(f"**Last Service:** {data['last_service_date']}")
                        if data.get('obd_codes'):
                            st.write(f"**OBD Codes:** {data['obd_codes']}")
                        
                        # Display Symptoms
                        st.markdown("### 🔍 Reported Symptoms")
                        symptoms = data.get('symptoms', {})
                        
                        # Handle both old format (string) and new format (dict)
                        if isinstance(symptoms, str):
                            st.markdown(f"**General Description:**\n>{symptoms}")
                        else:
                            # Power Symptoms
                            power_symptoms = symptoms.get('power', {})
                            active_power = [k.replace('_', ' ').title() for k, v in power_symptoms.items() if v]
                            if active_power:
                                st.markdown(f"**⚡ Power:** {', '.join(active_power)}")
                            
                            # Tactile Symptoms
                            tactile_symptoms = symptoms.get('tactile', {})
                            active_tactile = [k.replace('_', ' ').title() for k, v in tactile_symptoms.items() if v]
                            if active_tactile:
                                st.markdown(f"**👋 Tactile:** {', '.join(active_tactile)}")
                            
                            # Audible Symptoms
                            audible_symptoms = symptoms.get('audible', {})
                            active_audible = [k.replace('_', ' ').title() for k, v in audible_symptoms.items() if v]
                            if active_audible:
                                st.markdown(f"**🔊 Audible:** {', '.join(active_audible)}")
                            
                            # Fuel Symptoms
                            fuel_symptoms = symptoms.get('fuel', {})
                            active_fuel = [k.replace('_', ' ').title() for k, v in fuel_symptoms.items() if v]
                            if active_fuel:
                                st.markdown(f"**⛽ Fuel/Consumption:** {', '.join(active_fuel)}")
                            
                            # Visual Symptoms
                            visual_symptoms = symptoms.get('visual', {})
                            active_visual = [k.replace('_', ' ').title() for k, v in visual_symptoms.items() if v]
                            if active_visual:
                                st.markdown(f"**👁️ Visual:** {', '.join(active_visual)}")
                            
                            # Temperature Symptoms
                            temp_symptoms = symptoms.get('temperature', {})
                            active_temp = [k.replace('_', ' ').title() for k, v in temp_symptoms.items() if v]
                            if active_temp:
                                st.markdown(f"**🌡️ Temperature:** {', '.join(active_temp)}")
                            
                            # Additional Details
                            additional = symptoms.get('additional_details', '')
                            if additional:
                                st.markdown(f"**📝 Additional Details:**\n>{additional}")

                        if data.get('has_files'):
                            st.write("📎 *User uploaded files (placeholder)*")

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

                st.markdown("### 🚗 Vehicle Details")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Vehicle:** {req_data.get('year')} {req_data.get('make')} {req_data.get('model')}")
                    st.write(f"**Mileage:** {req_data.get('mileage')}")
                    st.write(f"**Engine:** {req_data.get('engine_type')}")
                with col2:
                    if req_data.get('transmission_type'):
                        st.write(f"**Transmission:** {req_data.get('transmission_type')}")
                    if req_data.get('fuel_type'):
                        st.write(f"**Fuel Type:** {req_data.get('fuel_type')}")
                    if req_data.get('last_service_date'):
                        st.write(f"**Last Service:** {req_data.get('last_service_date')}")
                
                # Display Symptoms
                st.markdown("### 🔍 Reported Symptoms")
                symptoms = req_data.get('symptoms', {})
                
                # Handle both old format (string) and new format (dict)
                if isinstance(symptoms, str):
                    st.markdown(f"**Description:**\n>{symptoms}")
                else:
                    # Power Symptoms
                    power_symptoms = symptoms.get('power', {})
                    active_power = [k.replace('_', ' ').title() for k, v in power_symptoms.items() if v]
                    if active_power:
                        st.markdown(f"**⚡ Power:** {', '.join(active_power)}")
                    
                    # Tactile Symptoms
                    tactile_symptoms = symptoms.get('tactile', {})
                    active_tactile = [k.replace('_', ' ').title() for k, v in tactile_symptoms.items() if v]
                    if active_tactile:
                        st.markdown(f"**👋 Tactile:** {', '.join(active_tactile)}")
                    
                    # Audible Symptoms
                    audible_symptoms = symptoms.get('audible', {})
                    active_audible = [k.replace('_', ' ').title() for k, v in audible_symptoms.items() if v]
                    if active_audible:
                        st.markdown(f"**🔊 Audible:** {', '.join(active_audible)}")
                    
                    # Fuel Symptoms
                    fuel_symptoms = symptoms.get('fuel', {})
                    active_fuel = [k.replace('_', ' ').title() for k, v in fuel_symptoms.items() if v]
                    if active_fuel:
                        st.markdown(f"**⛽ Fuel/Consumption:** {', '.join(active_fuel)}")
                    
                    # Visual Symptoms
                    visual_symptoms = symptoms.get('visual', {})
                    active_visual = [k.replace('_', ' ').title() for k, v in visual_symptoms.items() if v]
                    if active_visual:
                        st.markdown(f"**👁️ Visual:** {', '.join(active_visual)}")
                    
                    # Temperature Symptoms
                    temp_symptoms = symptoms.get('temperature', {})
                    active_temp = [k.replace('_', ' ').title() for k, v in temp_symptoms.items() if v]
                    if active_temp:
                        st.markdown(f"**🌡️ Temperature:** {', '.join(active_temp)}")
                    
                    # Additional Details
                    additional = symptoms.get('additional_details', '')
                    if additional:
                        st.markdown(f"**📝 Additional Details:**\n>{additional}")

                if req_data.get('status') == 'completed':
                    st.markdown("---")
                    st.subheader("✅ Expert Diagnosis")
                    st.info(req_data.get('response'))
                    st.caption(f"Responded on: {req_data.get('response_timestamp')}")
                else:
                    st.info("Your request is currently being reviewed by an expert. Please check back later.")
            else:
                st.error("Request ID not found. Please check and try again.")
