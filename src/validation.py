import re

def validate_input(make, model, year, mileage, vin, engine_type, transmission_type, 
                   fuel_type, last_service_date, symptoms, obd_codes):
    """
    Validates the input data for a diagnostic request.

    Args:
        make (str): Car make.
        model (str): Car model.
        year (int): Car year.
        mileage (int): Car mileage.
        vin (str): Vehicle Identification Number (optional).
        engine_type (str): Engine type.
        transmission_type (str): Transmission type.
        fuel_type (str): Fuel type.
        last_service_date (str): Last service date (optional).
        symptoms (dict): Dictionary of symptoms organized by category.
        obd_codes (str): OBD-II codes (optional).

    Returns:
        list: A list of error messages. If empty, input is valid.
    """
    errors = []

    # Validate Make
    if not make:
        errors.append("Car Make is required.")
    elif len(make) > 50:
        errors.append("Car Make must be less than 50 characters.")
    elif not re.match(r"^[a-zA-Z0-9\s-]+$", make):
        errors.append("Car Make can only contain alphanumeric characters, spaces, and hyphens.")

    # Validate Model
    if not model:
        errors.append("Car Model is required.")
    elif len(model) > 50:
        errors.append("Car Model must be less than 50 characters.")
    elif not re.match(r"^[a-zA-Z0-9\s-]+$", model):
        errors.append("Car Model can only contain alphanumeric characters, spaces, and hyphens.")

    # Validate Year
    if not isinstance(year, int) or year < 1900 or year > 2025:
        errors.append("Year must be between 1900 and 2025.")

    # Validate Mileage
    if not isinstance(mileage, int) or mileage < 0:
        errors.append("Mileage must be a non-negative integer.")

    # Validate VIN (Optional)
    if vin:
        if len(vin) != 17:
             errors.append("VIN must be exactly 17 characters.")
        elif not re.match(r"^[A-HJ-NPR-Z0-9]+$", vin): # Standard VIN excludes I, O, Q
             errors.append("VIN contains invalid characters (I, O, and Q are not allowed in standard VINs).")

    # Validate Engine Type
    valid_engines = ["Gasoline", "Diesel", "Hybrid", "Electric", "Other"]
    if engine_type not in valid_engines:
        errors.append("Invalid Engine Type selected.")

    # Validate Transmission Type
    valid_transmissions = ["Automatic", "Manual", "CVT", "Semi-Automatic", "Unknown"]
    if transmission_type not in valid_transmissions:
        errors.append("Invalid Transmission Type selected.")

    # Validate Fuel Type
    valid_fuel_types = ["Regular", "Premium", "Diesel", "Electric", "Hybrid", "Other"]
    if fuel_type not in valid_fuel_types:
        errors.append("Invalid Fuel Type selected.")

    # Validate Last Service Date (Optional)
    if last_service_date:
        if len(last_service_date) > 100:
            errors.append("Last Service Date must be less than 100 characters.")
        # Basic check for potentially malicious content
        elif re.search(r"<script.*?>", last_service_date, re.IGNORECASE):
            errors.append("Invalid characters detected in Last Service Date.")

    # Validate Symptoms
    if isinstance(symptoms, dict):
        # Check if at least one symptom is selected or additional details provided
        has_symptom = False
        for category in ['power', 'tactile', 'audible', 'fuel', 'visual', 'temperature']:
            if category in symptoms:
                for key, value in symptoms[category].items():
                    if value:
                        has_symptom = True
                        break
                if has_symptom:
                    break
        
        additional_details = symptoms.get('additional_details', '')
        if not has_symptom and not additional_details:
            errors.append("Please select at least one symptom or provide additional details.")
        
        # Validate additional details if provided
        if additional_details:
            if len(additional_details) > 2000:
                errors.append("Additional details must be less than 2000 characters.")
            elif re.search(r"<script.*?>", additional_details, re.IGNORECASE):
                errors.append("Invalid characters detected in additional details.")
    else:
        # Fallback for old string format (backward compatibility)
        if not symptoms:
            errors.append("Symptoms description is required.")
        elif len(symptoms) > 1000:
            errors.append("Symptoms description must be less than 1000 characters.")
        elif re.search(r"<script.*?>", symptoms, re.IGNORECASE):
            errors.append("Invalid characters detected in Symptoms.")

    # Validate OBD Codes (Optional)
    if obd_codes:
        if len(obd_codes) > 50:
            errors.append("OBD Codes must be less than 50 characters.")
        elif not re.match(r"^[A-Z0-9,\s]+$", obd_codes):
            errors.append("OBD Codes can only contain alphanumeric characters, commas, and spaces.")

    return errors
