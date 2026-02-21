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
    if not make or make == "Select Make":
        errors.append("Please select a Car Make from the dropdown.")
    elif len(make) > 50:
        errors.append("Car Make must be less than 50 characters.")

    # Validate Model
    if not model or model == "Select Model":
        errors.append("Please select a Car Model from the dropdown.")
    elif len(model) > 50:
        errors.append("Car Model must be less than 50 characters.")

    # Validate Year
    if not isinstance(year, int) or year == 0 or year < 1980 or year > 2025:
        errors.append("Please select a valid Year from the dropdown.")

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
    valid_engines = ["2", "3", "4", "5", "6", "8", "10", "11", "12", "Rotary"]
    if engine_type not in valid_engines:
        errors.append("Invalid Engine Type selected.")

    # Validate Transmission Type
    valid_transmissions = ["Automatic", "Manual", "CVT", "Semi-Automatic", "Unknown"]
    if transmission_type not in valid_transmissions:
        errors.append("Invalid Transmission Type selected.")

    # Validate Fuel Type
    valid_fuel_types = ["Petrol/Unleaded", "Diesel", "Hybrid", "Bio-Diesel", "Alcohol (E85/Methanol)"]
    if fuel_type not in valid_fuel_types:
        errors.append("Invalid Fuel Type selected.")

    # Validate Last Service Date (Optional)
    if last_service_date:
        if len(last_service_date) > 100:
            errors.append("Last Service Date must be less than 100 characters.")
        # Basic check for potentially malicious content
        elif re.search(r"<script.*?>", last_service_date, re.IGNORECASE | re.DOTALL):
            errors.append("Invalid characters detected in Last Service Date.")

    # Validate Symptoms
    if isinstance(symptoms, dict):
        # Check if at least one symptom is selected in each category
        categories_to_check = ['power', 'tactile', 'audible', 'fuel', 'visual', 'temperature']
        categories_missing_selection = []
        all_categories_no_change = True
        
        for category in categories_to_check:
            if category in symptoms:
                category_symptoms = symptoms[category]
                has_selection = False
                has_non_no_change = False
                
                for key, value in category_symptoms.items():
                    if value:  # If any checkbox is checked
                        has_selection = True
                        if key != 'no_change':  # Track if there's a selection other than "no change"
                            has_non_no_change = True
                
                if not has_selection:
                    category_name = category.replace('_', ' ').title()
                    categories_missing_selection.append(category_name)
                
                if has_non_no_change:
                    all_categories_no_change = False

                # Validate 'other' text if provided
                other_text = category_symptoms.get('other', '')
                if other_text:
                    if len(other_text) > 500:
                        errors.append(f"{category.title()} 'Other' description must be less than 500 characters.")
                    elif re.search(r"<script.*?>", other_text, re.IGNORECASE | re.DOTALL):
                        errors.append(f"Invalid characters detected in {category.title()} 'Other' description.")
        
        # Error if any category has no selection
        if categories_missing_selection:
            errors.append(f"Please select at least one option in the following categories: {', '.join(categories_missing_selection)}")
        
        # Error if all categories only have "No change" selected
        if all_categories_no_change and not categories_missing_selection:
            errors.append("You cannot select 'No change' in all categories. Please describe at least one symptom in any category.")
        
        # Validate additional details if provided
        additional_details = symptoms.get('additional_details', '')
        if additional_details:
            if len(additional_details) > 2000:
                errors.append("Additional details must be less than 2000 characters.")
            elif re.search(r"<script.*?>", additional_details, re.IGNORECASE | re.DOTALL):
                errors.append("Invalid characters detected in additional details.")
    else:
        # Fallback for old string format (backward compatibility)
        if not symptoms:
            errors.append("Symptoms description is required.")
        elif len(symptoms) > 1000:
            errors.append("Symptoms description must be less than 1000 characters.")
        elif re.search(r"<script.*?>", symptoms, re.IGNORECASE | re.DOTALL):
            errors.append("Invalid characters detected in Symptoms.")

    # Validate OBD Codes (Optional)
    if obd_codes:
        if len(obd_codes) > 50:
            errors.append("OBD Codes must be less than 50 characters.")
        elif not re.match(r"^[A-Z0-9,\s]+$", obd_codes):
            errors.append("OBD Codes can only contain alphanumeric characters, commas, and spaces.")

    return errors
