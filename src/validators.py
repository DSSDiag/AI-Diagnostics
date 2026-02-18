import re

def validate_make(make):
    """
    Validates the car make.
    Allowed: Alphanumeric, spaces, hyphens.
    Length: 2-50 characters.
    """
    if not make:
        return False, "Car Make is required."
    if not (2 <= len(make) <= 50):
        return False, "Car Make must be between 2 and 50 characters."
    if not re.match(r"^[\w\s-]+$", make):
        return False, "Car Make contains invalid characters."
    return True, ""

def validate_model(model):
    """
    Validates the car model.
    Allowed: Alphanumeric, spaces, hyphens.
    Length: 1-50 characters.
    """
    if not model:
        return False, "Car Model is required."
    if not (1 <= len(model) <= 50):
        return False, "Car Model must be between 1 and 50 characters."
    if not re.match(r"^[\w\s-]+$", model):
        return False, "Car Model contains invalid characters."
    return True, ""

def validate_vin(vin):
    """
    Validates the VIN.
    Allowed: Alphanumeric.
    Length: 17 characters.
    """
    if not vin:
        return True, ""  # Optional
    if len(vin) != 17:
        return False, "VIN must be exactly 17 characters."
    if not re.match(r"^[a-zA-Z0-9]+$", vin):
        return False, "VIN contains invalid characters."
    return True, ""

def validate_symptoms(symptoms):
    """
    Validates the symptoms description.
    Length: 10-2000 characters.
    """
    if not symptoms:
        return False, "Symptoms description is required."
    if not (10 <= len(symptoms) <= 2000):
        return False, "Symptoms must be between 10 and 2000 characters."
    return True, ""

def validate_obd_codes(obd_codes):
    """
    Validates OBD-II codes.
    Format: Comma-separated 5-char codes (e.g., P0300, C1234).
    """
    if not obd_codes:
        return True, ""  # Optional

    # Split by comma and strip whitespace
    codes = [code.strip() for code in obd_codes.split(',')]

    for code in codes:
        if not re.match(r"^[PCBU][0-9A-F]{4}$", code.upper()):
            return False, f"Invalid OBD code format: {code}. Expected format like P0300."

    return True, ""
