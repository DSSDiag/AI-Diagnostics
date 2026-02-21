import streamlit as st
from src.storage import create_request, get_request, get_all_requests, update_request_response
from src.validation import validate_input

st.set_page_config(page_title="Automotive AI Diagnostics", layout="wide", page_icon="🚗")

st.title("🚗 Automotive Fault Diagnostics")

# Mock User Login for Expert and Admin
# In a real app, this would use a secure authentication system.
EXPERT_PASSWORD = "password123"
ADMIN_PASSWORD = "admin456"

# Tabs for different user roles
tab1, tab2, tab3, tab4 = st.tabs(["Car Owner (Submit Issue)", "Expert Dashboard (For Mechanics)", "Check Diagnosis Status", "Admin Area"])

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
    
    # Popular models by make
    MODELS_BY_MAKE = {
        "Abarth": ["Select Model", "500", "595", "695", "124 Spider", "Punto", "Other"],
        "Alfa Romeo": ["Select Model", "147", "156", "159", "Brera", "Giulia", "Giulietta", "GTV", "MiTo", "Spider", "Stelvio", "Tonale", "Other"],
        "Aston Martin": ["Select Model", "DB7", "DB9", "DB11", "DBS", "DBX", "Rapide", "Vantage", "Virage", "Vanquish", "Other"],
        "Audi": ["Select Model", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "e-tron", "e-tron GT", "Q2", "Q3", "Q4 e-tron", "Q5", "Q7", "Q8", "Q8 e-tron", "R8", "RS3", "RS4", "RS5", "RS6", "RS7", "S3", "S4", "S5", "S6", "S7", "S8", "TT", "Other"],
        "Bentley": ["Select Model", "Arnage", "Azure", "Bentayga", "Continental GT", "Continental GTC", "Flying Spur", "Mulsanne", "Other"],
        "BMW": ["Select Model", "1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series", "8 Series", "i3", "i4", "i5", "i7", "iX", "iX1", "iX3", "M2", "M3", "M4", "M5", "M8", "X1", "X2", "X3", "X3 M", "X4", "X4 M", "X5", "X5 M", "X6", "X6 M", "X7", "Z3", "Z4", "Other"],
        "BYD": ["Select Model", "Atto 3", "Dolphin", "Han", "Seal", "Sea Lion 6", "Song", "Song Plus", "Tang", "Other"],
        "Chery": ["Select Model", "Omoda 5", "Tiggo 4", "Tiggo 7", "Tiggo 7 Pro", "Tiggo 8", "Tiggo 8 Pro", "Other"],
        "Chevrolet": ["Select Model", "Camaro", "Colorado", "Corvette", "Equinox", "Express", "Silverado", "Suburban", "Tahoe", "Trailblazer", "Traverse", "Other"],
        "Chrysler": ["Select Model", "300", "300C", "Grand Voyager", "Neon", "PT Cruiser", "Sebring", "Voyager", "Other"],
        "Citroen": ["Select Model", "Berlingo", "Boxer", "C1", "C2", "C3", "C3 Aircross", "C4", "C4 Cactus", "C5", "C5 Aircross", "C5 X", "C6", "Dispatch", "DS3", "DS4", "DS5", "Jumper", "Jumpy", "Relay", "SpaceTourer", "Xsara", "Other"],
        "Cupra": ["Select Model", "Ateca", "Born", "Formentor", "Leon", "Terramar", "Tavascan", "Other"],
        "Dacia": ["Select Model", "Duster", "Logan", "Sandero", "Spring", "Jogger", "Other"],
        "Daewoo": ["Select Model", "Kalos", "Lacetti", "Lanos", "Leganza", "Nubira", "Tacuma", "Other"],
        "Daihatsu": ["Select Model", "Charade", "Cuore", "Feroza", "Rocky", "Sirion", "Terios", "YRV", "Other"],
        "Dodge": ["Select Model", "Challenger", "Charger", "Durango", "Journey", "Neon", "Nitro", "Viper", "Other"],
        "Ferrari": ["Select Model", "296 GTB", "296 GTS", "458", "488 GTB", "488 Spider", "812 Competizione", "812 GTS", "812 Superfast", "California", "California T", "F12berlinetta", "F8 Spider", "F8 Tributo", "FF", "GTC4Lusso", "Portofino", "Portofino M", "Purosangue", "Roma", "SF90 Spider", "SF90 Stradale", "Other"],
        "Fiat": ["Select Model", "124 Spider", "500", "500C", "500L", "500X", "Bravo", "Doblo", "Ducato", "Freemont", "Grande Punto", "Linea", "Panda", "Punto", "Scudo", "Tipo", "Other"],
        "Ford": ["Select Model", "Bronco", "Bronco Sport", "Edge", "Escape", "Everest", "Explorer", "F-150", "Fiesta", "Focus", "Fusion", "Galaxy", "Kuga", "Maverick", "Mondeo", "Mustang", "Puma", "Ranger", "S-Max", "Territory", "Transit", "Transit Custom", "Other"],
        "Genesis": ["Select Model", "G70", "G80", "G90", "GV60", "GV70", "GV80", "Other"],
        "GWM": ["Select Model", "Haval H2", "Haval H6", "Haval H9", "Haval Jolion", "Tank 300", "Tank 500", "Ute", "Other"],
        "Holden": ["Select Model", "Astra", "Barina", "Calais", "Captiva", "Colorado", "Commodore", "Cruze", "Insignia", "Malibu", "Monaro", "Spark", "Statesman", "Trailblazer", "Trax", "Ute", "Other"],
        "Honda": ["Select Model", "Accord", "Accord Euro", "BR-V", "City", "Civic", "CR-V", "CR-Z", "e:NS1", "e:NP1", "e:NY1", "HR-V", "Integra", "Jazz", "Legend", "Odyssey", "Passport", "Pilot", "Ridgeline", "S2000", "WR-V", "ZR-V", "Other"],
        "Hyundai": ["Select Model", "Accent", "Elantra", "Getz", "i20", "i20 N", "i30", "i30 N", "i40", "IONIQ", "IONIQ 5", "IONIQ 6", "IONIQ 9", "Kona", "Kona Electric", "Palisade", "Santa Cruz", "Santa Fe", "Sonata", "Staria", "Tucson", "Venue", "Veloster", "Other"],
        "Infiniti": ["Select Model", "EX", "FX", "G", "M", "Q30", "Q50", "Q60", "Q70", "QX30", "QX50", "QX55", "QX60", "QX70", "QX80", "Other"],
        "Isuzu": ["Select Model", "D-Max", "MU-X", "Other"],
        "Jaguar": ["Select Model", "E-Pace", "F-Pace", "F-Type", "I-Pace", "S-Type", "XE", "XF", "XJ", "XJR", "XK", "Other"],
        "Jeep": ["Select Model", "Cherokee", "Commander", "Compass", "Gladiator", "Grand Cherokee", "Grand Cherokee L", "Patriot", "Renegade", "Wrangler", "Other"],
        "Kia": ["Select Model", "Carnival", "Ceed", "Cerato", "EV6", "EV9", "Mohave", "Niro", "Niro EV", "Picanto", "Pro Ceed", "Rio", "Seltos", "Sorento", "Soul", "Sportage", "Stinger", "Stonic", "Telluride", "Other"],
        "Lamborghini": ["Select Model", "Aventador", "Gallardo", "Huracan", "Revuelto", "Urus", "Other"],
        "Land Rover": ["Select Model", "Defender", "Discovery", "Discovery Sport", "Evoque", "Freelander", "Range Rover", "Range Rover Sport", "Range Rover Velar", "Other"],
        "LDV": ["Select Model", "D90", "Deliver 9", "G10", "Mifa 6", "Mifa 9", "T60", "T60 Max", "Other"],
        "Lexus": ["Select Model", "CT", "ES", "GS", "GX", "IS", "LC", "LS", "LX", "NX", "RC", "RC F", "RX", "RZ", "UX", "Other"],
        "Mahindra": ["Select Model", "Bolero", "Pik Up", "Scorpio", "Thar", "XUV300", "XUV400", "XUV700", "Other"],
        "Maserati": ["Select Model", "Ghibli", "GranCabrio", "GranTurismo", "Grecale", "Levante", "MC20", "Quattroporte", "Other"],
        "Mazda": ["Select Model", "2", "3", "6", "BT-50", "CX-3", "CX-30", "CX-5", "CX-60", "CX-70", "CX-80", "CX-90", "CX-9", "MX-5", "MX-30", "Other"],
        "McLaren": ["Select Model", "540C", "570GT", "570S", "600LT", "620R", "650S", "675LT", "720S", "765LT", "Artura", "GT", "MP4-12C", "Other"],
        "Mercedes-Benz": ["Select Model", "A-Class", "AMG GT", "B-Class", "C-Class", "CLA", "CLS", "E-Class", "EQA", "EQB", "EQC", "EQE", "EQS", "G-Class", "GLA", "GLB", "GLC", "GLE", "GLS", "S-Class", "SL", "SLC", "Sprinter", "V-Class", "Vito", "Other"],
        "MG": ["Select Model", "3", "4", "5", "6", "Cyberster", "HS", "HS PHEV", "Marvel R", "ZS", "ZS EV", "Other"],
        "Mini": ["Select Model", "Clubman", "Convertible", "Countryman", "Coupe", "Hatch", "John Cooper Works", "Paceman", "Roadster", "Other"],
        "Mitsubishi": ["Select Model", "3000GT", "ASX", "Carisma", "Colt", "Eclipse Cross", "Eclipse Cross PHEV", "Galant", "i-MiEV", "Lancer", "Mirage", "Outlander", "Outlander PHEV", "Pajero", "Pajero Sport", "Triton", "Other"],
        "Nissan": ["Select Model", "350Z", "370Z", "Altima", "Ariya", "Armada", "Frontier", "GT-R", "Juke", "Leaf", "Maxima", "Micra", "Murano", "Navara", "Note", "Pathfinder", "Patrol", "Pulsar", "Qashqai", "Sentra", "Skyline", "Tiida", "Titan", "X-Trail", "Z", "Other"],
        "Opel": ["Select Model", "Astra", "Corsa", "Grandland", "Insignia", "Mokka", "Zafira", "Other"],
        "Peugeot": ["Select Model", "108", "208", "308", "408", "508", "2008", "3008", "4008", "5008", "Boxer", "Expert", "Partner", "Rifter", "Traveller", "Other"],
        "Porsche": ["Select Model", "718 Boxster", "718 Cayman", "911", "Cayenne", "Cayenne E-Hybrid", "Macan", "Macan Electric", "Panamera", "Taycan", "Other"],
        "RAM": ["Select Model", "1500", "1500 Classic", "2500", "3500", "Other"],
        "Renault": ["Select Model", "Arkana", "Austral", "Captur", "Clio", "Duster", "Kadjar", "Kangoo", "Koleos", "Laguna", "Master", "Megane", "Scenic", "Trafic", "Zoe", "Other"],
        "Rolls-Royce": ["Select Model", "Cullinan", "Dawn", "Ghost", "Phantom", "Silver Shadow", "Silver Seraph", "Spectre", "Wraith", "Other"],
        "Skoda": ["Select Model", "Enyaq", "Fabia", "Kamiq", "Karoq", "Kodiaq", "Octavia", "Scala", "Superb", "Other"],
        "SsangYong": ["Select Model", "Actyon", "Korando", "Musso", "Rexton", "Tivoli", "Torres", "Other"],
        "Subaru": ["Select Model", "BRZ", "Crosstrek", "Forester", "Impreza", "Legacy", "Levorg", "Liberty", "Outback", "Solterra", "WRX", "WRX STI", "XV", "Other"],
        "Suzuki": ["Select Model", "Across", "Baleno", "Grand Vitara", "Ignis", "Jimny", "Kizashi", "S-Cross", "Splash", "Swift", "SX4", "Vitara", "Other"],
        "Tesla": ["Select Model", "Cybertruck", "Model 3", "Model S", "Model X", "Model Y", "Roadster", "Other"],
        "Toyota": ["Select Model", "86", "Aurion", "Avalon", "Camry", "C-HR", "Corolla", "Corolla Cross", "Dyna", "Fortuner", "GR86", "GR Corolla", "GR Supra", "HiAce", "Hilux", "Kluger", "LandCruiser", "LandCruiser 200", "LandCruiser 300", "Lite Ace", "Prado", "ProAce", "RAV4", "RAV4 PHEV", "Rukus", "Supra", "Tarago", "Yaris", "Yaris Cross", "Other"],
        "Volkswagen": ["Select Model", "Amarok", "Arteon", "Caddy", "Caravelle", "Crafter", "Golf", "ID.3", "ID.4", "ID.5", "Multivan", "Passat", "Polo", "T-Cross", "T-Roc", "Tiguan", "Tiguan Allspace", "Touareg", "Touran", "Transporter", "Other"],
        "Volvo": ["Select Model", "C30", "C40", "C70", "EX30", "EX40", "EX90", "S40", "S60", "S80", "S90", "V40", "V60", "V90", "XC40", "XC60", "XC70", "XC90", "Other"],
    }
    
    YEARS = ["Select Year"] + [str(year) for year in range(2025, 1979, -1)]
    
    # Vehicle information is outside the form so that selecting a make
    # triggers a re-run and the model dropdown updates dynamically.
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
        engine_type = st.selectbox("Engine Type", ["2", "3", "4", "5", "6", "8", "10", "11", "12", "Rotary"])

    with col3:
        transmission_type = st.selectbox("Transmission", ["Automatic", "Manual", "CVT", "Semi-Automatic", "Unknown"])
        fuel_type = st.selectbox("Fuel Type", ["Petrol/Unleaded", "Diesel", "Hybrid", "Bio-Diesel", "Alcohol (E85/Methanol)"])
        last_service_date = st.text_input("Last Service Date (Optional)", placeholder="YYYY-MM-DD or e.g., 3 months ago")

    with st.form("diagnostic_request_form"):
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
            power_more = st.checkbox("Increased power")
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

# --- TAB 4: ADMIN AREA ---
with tab4:
    st.header("🔐 Admin Area")
    st.markdown("Administrative dashboard for webapp monitoring and management")
    
    # Simple Authentication Check
    if 'admin_logged_in' not in st.session_state:
        st.session_state['admin_logged_in'] = False
    
    if not st.session_state['admin_logged_in']:
        password = st.text_input("Enter Admin Password", type="password", key="admin_password")
        if st.button("Login as Admin"):
            if password == ADMIN_PASSWORD:
                st.session_state['admin_logged_in'] = True
                st.rerun()
            else:
                st.error("Incorrect admin password.")
    else:
        st.success("Logged in as Administrator")
        if st.button("Logout", key="admin_logout"):
            st.session_state['admin_logged_in'] = False
            st.rerun()
        
        st.markdown("---")
        
        # Get all requests for statistics
        all_requests = get_all_requests()
        
        # Calculate statistics
        total_requests = len(all_requests)
        pending_count = sum(1 for req in all_requests.values() if req.get('status') == 'pending')
        completed_count = sum(1 for req in all_requests.values() if req.get('status') == 'completed')
        
        # Display key metrics
        st.subheader("📊 Key Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Requests", total_requests)
        with col2:
            st.metric("Pending Requests", pending_count)
        with col3:
            st.metric("Completed Requests", completed_count)
        
        st.markdown("---")
        
        # Activity Overview
        st.subheader("📈 Recent Activity")
        if all_requests:
            # Sort requests by timestamp (most recent first)
            sorted_requests = sorted(
                all_requests.items(), 
                key=lambda x: x[1].get('timestamp', ''), 
                reverse=True
            )
            
            # Show recent activity timeline
            st.markdown("**Latest 10 Requests:**")
            for i, (req_id, data) in enumerate(sorted_requests[:10]):
                status_icon = "✅" if data.get('status') == 'completed' else "⏳"
                status = data.get('status', 'unknown')
                year = data.get('year', 'N/A')
                make = data.get('make', 'Unknown')
                model = data.get('model', 'Unknown')
                st.markdown(f"{status_icon} **{year} {make} {model}** - {data.get('timestamp')} - Status: {status.upper()}")
        else:
            st.info("No activity yet.")
        
        st.markdown("---")
        
        # Detailed Request List
        st.subheader("🗂️ All Requests Details")
        
        if all_requests:
            # Filter options
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
            with filter_col2:
                sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])
            
            # Apply filters
            filtered_requests = all_requests
            if status_filter != "All":
                filtered_requests = {k: v for k, v in all_requests.items() if v.get('status') == status_filter.lower()}
            
            # Sort
            sorted_filtered = sorted(
                filtered_requests.items(),
                key=lambda x: x[1].get('timestamp', ''),
                reverse=(sort_order == "Newest First")
            )
            
            st.markdown(f"**Showing {len(sorted_filtered)} requests**")
            
            # Display detailed information for each request
            for req_id, data in sorted_filtered:
                status_color = "🟢" if data.get('status') == 'completed' else "🟡"
                year = data.get('year', 'N/A')
                make = data.get('make', 'Unknown')
                model = data.get('model', 'Unknown')
                with st.expander(f"{status_color} {year} {make} {model} - ID: {req_id[:12]}..."):
                    # Request metadata
                    st.markdown("### Request Information")
                    meta_col1, meta_col2 = st.columns(2)
                    with meta_col1:
                        st.write(f"**Request ID:** `{req_id}`")
                        st.write(f"**Submitted:** {data.get('timestamp')}")
                        status = data.get('status', 'unknown')
                        st.write(f"**Status:** {status.upper()}")
                    with meta_col2:
                        if data.get('status') == 'completed':
                            st.write(f"**Responded:** {data.get('response_timestamp')}")
                        st.write(f"**Has Files:** {'Yes' if data.get('has_files') else 'No'}")
                    
                    # Vehicle Details
                    st.markdown("### 🚗 Vehicle Details")
                    veh_col1, veh_col2, veh_col3 = st.columns(3)
                    with veh_col1:
                        st.write(f"**Make:** {data.get('make', 'Unknown')}")
                        st.write(f"**Model:** {data.get('model', 'Unknown')}")
                        st.write(f"**Year:** {data.get('year', 'N/A')}")
                    with veh_col2:
                        st.write(f"**Mileage:** {data.get('mileage', 0)} km")
                        st.write(f"**Engine:** {data.get('engine_type', 'Unknown')}")
                        if data.get('vin'):
                            st.write(f"**VIN:** {data.get('vin')}")
                    with veh_col3:
                        st.write(f"**Transmission:** {data.get('transmission_type', 'N/A')}")
                        st.write(f"**Fuel Type:** {data.get('fuel_type', 'N/A')}")
                        if data.get('last_service_date'):
                            st.write(f"**Last Service:** {data['last_service_date']}")
                    
                    if data.get('obd_codes'):
                        st.write(f"**OBD Codes:** {data['obd_codes']}")
                    
                    # Display Symptoms
                    st.markdown("### 🔍 Reported Symptoms")
                    symptoms = data.get('symptoms', {})
                    
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
                    
                    # Expert Response (if completed)
                    if data.get('status') == 'completed' and data.get('response'):
                        st.markdown("### ✅ Expert Diagnosis")
                        st.info(data.get('response'))
                    
                    st.markdown("---")
        else:
            st.info("No requests to display.")
