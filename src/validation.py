import re

def validate_input(make, model, year, mileage, vin, engine_type, symptoms, obd_codes):
    """
    Validates the input data for a diagnostic request.

    Args:
        make (str): Car make.
        model (str): Car model.
        year (int): Car year.
        mileage (int): Car mileage.
        vin (str): Vehicle Identification Number (optional).
        engine_type (str): Engine type.
        symptoms (str): Description of the problem.
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

    # Validate Symptoms
    if not symptoms:
        errors.append("Symptoms description is required.")
    elif len(symptoms) > 1000:
        errors.append("Symptoms description must be less than 1000 characters.")
    # Check for potential XSS (basic check for script tags)
    elif re.search(r"<script.*?>", symptoms, re.IGNORECASE):
        errors.append("Invalid characters detected in Symptoms.")

    # Validate OBD Codes (Optional)
    if obd_codes:
        if len(obd_codes) > 50:
            errors.append("OBD Codes must be less than 50 characters.")
        elif not re.match(r"^[A-Z0-9,\s]+$", obd_codes):
            errors.append("OBD Codes can only contain alphanumeric characters, commas, and spaces.")

    return errors
