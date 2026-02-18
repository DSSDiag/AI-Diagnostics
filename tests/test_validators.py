import pytest
from src.validators import validate_vehicle_input

def test_valid_input():
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="1HGCM82633A004352",
        engine_type="Gasoline",
        symptoms="Car is making a rattling noise.",
        obd_codes="P0300, P0420"
    )
    assert errors == []

def test_missing_required_fields():
    errors = validate_vehicle_input(
        make="",
        model="",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        symptoms="",
        obd_codes=""
    )
    assert "Make is required." in errors
    assert "Model is required." in errors
    assert "Symptoms description is required." in errors

def test_invalid_make_model_format():
    errors = validate_vehicle_input(
        make="Toy@ta",
        model="Camry!",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        symptoms="Valid symptoms description",
        obd_codes=""
    )
    assert "Make contains invalid characters. Only alphanumeric, spaces, hyphens, periods, and apostrophes are allowed." in errors
    assert "Model contains invalid characters. Only alphanumeric, spaces, hyphens, periods, and apostrophes are allowed." in errors

def test_invalid_year_range():
    from datetime import datetime
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=1800,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        symptoms="Valid symptoms description",
        obd_codes=""
    )
    assert f"Year must be between 1900 and {datetime.now().year + 1}." in errors

def test_invalid_mileage():
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=-100,
        vin="",
        engine_type="Gasoline",
        symptoms="Valid symptoms description",
        obd_codes=""
    )
    assert "Mileage cannot be negative." in errors

def test_invalid_vin():
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="INVALIDVIN",
        engine_type="Gasoline",
        symptoms="Valid symptoms description",
        obd_codes=""
    )
    assert "VIN must be exactly 17 alphanumeric characters (excluding I, O, Q)." in errors

def test_invalid_engine_type():
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Nuclear",
        symptoms="Valid symptoms description",
        obd_codes=""
    )
    assert "Invalid engine type selected." in errors

def test_short_symptoms():
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        symptoms="Short",
        obd_codes=""
    )
    assert "Please provide a more detailed description of the symptoms (at least 10 characters)." in errors

def test_invalid_obd_codes():
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="",
        engine_type="Gasoline",
        symptoms="Valid symptoms description",
        obd_codes="INVALID, P0300"
    )
    # Check for substring match because the error message contains the specific code
    assert any("Invalid OBD code format: INVALID" in e for e in errors)

def test_vin_case_insensitive():
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=2015,
        mileage=50000,
        vin="1hgcm82633a004352", # Lowercase
        engine_type="Gasoline",
        symptoms="Valid symptoms description",
        obd_codes=""
    )
    assert errors == []

def test_valid_input_with_special_chars():
    errors = validate_vehicle_input(
        make="Kia cee'd",
        model="Model S.",
        year=2024,
        mileage=50000,
        vin="1HGCM82633A004352",
        engine_type="Gasoline",
        symptoms="Car is making a rattling noise.",
        obd_codes="P0300, P0420"
    )
    assert errors == []

def test_future_year():
    from datetime import datetime
    future_year = datetime.now().year + 2
    errors = validate_vehicle_input(
        make="Toyota",
        model="Camry",
        year=future_year,
        mileage=50000,
        vin="1HGCM82633A004352",
        engine_type="Gasoline",
        symptoms="Car is making a rattling noise.",
        obd_codes=""
    )
    assert any("Year must be between 1900 and" in e for e in errors)
