import pytest
from src.validation import validate_input

def test_validate_input_valid():
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="1HGCM82633A004352", # Valid format
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="2024-01-15",
        symptoms="Strange noise from engine.",
        obd_codes="P0300, P0420"
    )
    assert errors == []

def test_validate_input_valid_optional_empty():
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Strange noise from engine.",
        obd_codes=""
    )
    assert errors == []

def test_validate_input_missing_required():
    errors = validate_input(
        make="",
        model="",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="",
        obd_codes=""
    )
    assert "Car Make is required." in errors
    assert "Car Model is required." in errors
    assert "Symptoms description is required." in errors

def test_validate_input_invalid_make_model():
    errors = validate_input(
        make="Toyota!",
        model="Camry@",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Symptoms",
        obd_codes=""
    )
    assert "Car Make can only contain alphanumeric characters, spaces, and hyphens." in errors
    assert "Car Model can only contain alphanumeric characters, spaces, and hyphens." in errors

def test_validate_input_invalid_year_mileage():
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=1800,
        mileage=-10,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Symptoms",
        obd_codes=""
    )
    assert "Year must be between 1900 and 2025." in errors
    assert "Mileage must be a non-negative integer." in errors

def test_validate_input_invalid_vin():
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="123", # Too short
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Symptoms",
        obd_codes=""
    )
    assert "VIN must be exactly 17 characters." in errors

    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="1HGCM82633A00435I", # Invalid char I
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Symptoms",
        obd_codes=""
    )
    assert "VIN contains invalid characters (I, O, and Q are not allowed in standard VINs)." in errors

def test_validate_input_invalid_engine():
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Nuclear",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Symptoms",
        obd_codes=""
    )
    assert "Invalid Engine Type selected." in errors

def test_validate_input_symptoms_xss():
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="<script>alert('xss')</script>",
        obd_codes=""
    )
    assert "Invalid characters detected in Symptoms." in errors

def test_validate_input_long_fields():
    long_string = "a" * 51
    errors = validate_input(
        make=long_string,
        model=long_string,
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Symptoms",
        obd_codes=long_string
    )
    assert "Car Make must be less than 50 characters." in errors
    assert "Car Model must be less than 50 characters." in errors
    assert "OBD Codes must be less than 50 characters." in errors

def test_validate_input_invalid_obd():
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Symptoms",
        obd_codes="P0101; DROP TABLE"
    )
    assert "OBD Codes can only contain alphanumeric characters, commas, and spaces." in errors

# New tests for enhanced vehicle details and categorized symptoms

def test_validate_input_new_format_valid():
    """Test validation with new categorized symptoms format"""
    symptoms_data = {
        "power": {
            "loss_of_power": True,
            "intermittent_power_loss": False,
            "no_power_change": False,
            "power_surges": False,
            "increased_power": False,
            "hesitation_lag": False
        },
        "tactile": {
            "vibration": True,
            "rough_engine": False,
            "pulling_to_side": False,
            "shaking": False,
            "jerking": False,
            "stiff_controls": False
        },
        "audible": {
            "rattling": True,
            "knocking": False,
            "grinding": False,
            "squealing": False,
            "humming": False,
            "clicking": False
        },
        "fuel": {
            "increased_consumption": False,
            "fuel_smell": False,
            "decreased_mileage": False,
            "fuel_leak": False,
            "difficulty_starting": False,
            "stalling": False
        },
        "visual": {
            "white_smoke": False,
            "black_smoke": False,
            "blue_smoke": False,
            "warning_lights": True,
            "fluid_leak": False,
            "corrosion": False
        },
        "temperature": {
            "overheating": False,
            "running_hot": False,
            "running_cold": False,
            "ac_issues": False,
            "heater_issues": False
        },
        "additional_details": "Engine makes noise when starting cold"
    }
    
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="1HGCM82633A004352",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="2024-01-15",
        symptoms=symptoms_data,
        obd_codes="P0300"
    )
    assert errors == []

def test_validate_input_new_format_with_only_additional_details():
    """Test validation when only additional details are provided"""
    symptoms_data = {
        "power": {},
        "tactile": {},
        "audible": {},
        "fuel": {},
        "visual": {},
        "temperature": {},
        "additional_details": "Car has intermittent issue that's hard to describe"
    }
    
    errors = validate_input(
        make="Honda",
        model="Civic",
        year=2018,
        mileage=30000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Manual",
        fuel_type="Premium",
        last_service_date="",
        symptoms=symptoms_data,
        obd_codes=""
    )
    assert errors == []

def test_validate_input_new_format_no_symptoms():
    """Test validation when no symptoms or details are provided"""
    symptoms_data = {
        "power": {
            "loss_of_power": False,
            "intermittent_power_loss": False,
            "no_power_change": False,
            "power_surges": False,
            "increased_power": False,
            "hesitation_lag": False
        },
        "tactile": {},
        "audible": {},
        "fuel": {},
        "visual": {},
        "temperature": {},
        "additional_details": ""
    }
    
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms=symptoms_data,
        obd_codes=""
    )
    assert "Please select at least one symptom or provide additional details." in errors

def test_validate_input_invalid_transmission():
    """Test validation with invalid transmission type"""
    symptoms_data = {
        "power": {"loss_of_power": True},
        "tactile": {},
        "audible": {},
        "fuel": {},
        "visual": {},
        "temperature": {},
        "additional_details": ""
    }
    
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="InvalidType",
        fuel_type="Regular",
        last_service_date="",
        symptoms=symptoms_data,
        obd_codes=""
    )
    assert "Invalid Transmission Type selected." in errors

def test_validate_input_invalid_fuel_type():
    """Test validation with invalid fuel type"""
    symptoms_data = {
        "power": {"loss_of_power": True},
        "tactile": {},
        "audible": {},
        "fuel": {},
        "visual": {},
        "temperature": {},
        "additional_details": ""
    }
    
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="InvalidFuel",
        last_service_date="",
        symptoms=symptoms_data,
        obd_codes=""
    )
    assert "Invalid Fuel Type selected." in errors

def test_validate_input_long_additional_details():
    """Test validation with excessively long additional details"""
    symptoms_data = {
        "power": {},
        "tactile": {},
        "audible": {},
        "fuel": {},
        "visual": {},
        "temperature": {},
        "additional_details": "a" * 2001  # Too long
    }
    
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms=symptoms_data,
        obd_codes=""
    )
    assert "Additional details must be less than 2000 characters." in errors

def test_validate_input_xss_in_additional_details():
    """Test validation to catch XSS attempts in additional details"""
    symptoms_data = {
        "power": {},
        "tactile": {},
        "audible": {},
        "fuel": {},
        "visual": {},
        "temperature": {},
        "additional_details": "<script>alert('xss')</script>"
    }
    
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms=symptoms_data,
        obd_codes=""
    )
    assert "Invalid characters detected in additional details." in errors

def test_validate_input_long_service_date():
    """Test validation with excessively long service date"""
    symptoms_data = {
        "power": {"loss_of_power": True},
        "tactile": {},
        "audible": {},
        "fuel": {},
        "visual": {},
        "temperature": {},
        "additional_details": ""
    }
    
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="a" * 101,  # Too long
        symptoms=symptoms_data,
        obd_codes=""
    )
    assert "Last Service Date must be less than 100 characters." in errors

def test_validate_input_backward_compatibility():
    """Test that old string-based symptoms still work"""
    errors = validate_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        transmission_type="Automatic",
        fuel_type="Regular",
        last_service_date="",
        symptoms="Engine makes a strange noise",
        obd_codes=""
    )
    assert errors == []

