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
        symptoms="Symptoms",
        obd_codes="P0101; DROP TABLE"
    )
    assert "OBD Codes can only contain alphanumeric characters, commas, and spaces." in errors
