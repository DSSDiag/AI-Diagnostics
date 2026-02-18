import re
from datetime import datetime

def validate_vehicle_input(make, model, year, mileage, vin, engine_type, symptoms, obd_codes):
    """
    Validates vehicle data and symptoms.

    Args:
        make (str): Car make.
        model (str): Car model.
        year (int): Car year.
        mileage (int): Car mileage.
        vin (str): Vehicle Identification Number (optional).
        engine_type (str): Engine type.
        symptoms (str): Description of the problem.
        obd_codes (str): Comma-separated OBD-II codes (optional).

    Returns:
        list: A list of error messages. If empty, validation passed.
    """
    errors = []

    # Make validation
    if not make:
        errors.append("Make is required.")
    elif len(make) < 2 or len(make) > 50:
        errors.append("Make must be between 2 and 50 characters.")
    elif not re.match(r"^[a-zA-Z0-9\s\-\'\.]+$", make):
        errors.append("Make contains invalid characters. Only alphanumeric, spaces, hyphens, periods, and apostrophes are allowed.")

    # Model validation
    if not model:
        errors.append("Model is required.")
    elif len(model) < 1 or len(model) > 50:
        errors.append("Model must be between 1 and 50 characters.")
    elif not re.match(r"^[a-zA-Z0-9\s\-\'\.]+$", model):
        errors.append("Model contains invalid characters. Only alphanumeric, spaces, hyphens, periods, and apostrophes are allowed.")

    # Year validation
    current_year = datetime.now().year
    try:
        year = int(year)
        if not (1900 <= year <= current_year + 1):
            errors.append(f"Year must be between 1900 and {current_year + 1}.")
    except (ValueError, TypeError):
        errors.append("Year must be a valid number.")

    # Mileage validation
    try:
        mileage = float(mileage)
        if mileage < 0:
            errors.append("Mileage cannot be negative.")
    except (ValueError, TypeError):
        errors.append("Mileage must be a valid number.")

    # VIN validation (optional)
    if vin:
        vin = vin.strip().upper()
        # Check standard VIN format (17 chars, no I, O, Q)
        if not re.match(r"^[A-HJ-NPR-Z0-9]{17}$", vin):
             errors.append("VIN must be exactly 17 alphanumeric characters (excluding I, O, Q).")

    # Engine Type
    valid_engines = ["Gasoline", "Diesel", "Hybrid", "Electric", "Other"]
    if engine_type not in valid_engines:
        errors.append("Invalid engine type selected.")

    # Symptoms validation
    if not symptoms:
        errors.append("Symptoms description is required.")
    elif len(symptoms) < 10:
        errors.append("Please provide a more detailed description of the symptoms (at least 10 characters).")

    # OBD Codes validation (optional)
    if obd_codes:
        # Split by comma and strip whitespace
        codes = [code.strip() for code in obd_codes.split(',') if code.strip()]
        for code in codes:
             if not re.match(r"^[PBCU][0-9]{4}$", code, re.IGNORECASE):
                 errors.append(f"Invalid OBD code format: {code}. Expected format like P0123.")

    return errors
