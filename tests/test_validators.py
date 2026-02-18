import pytest
from src.validators import validate_make, validate_model, validate_vin, validate_symptoms, validate_obd_codes

def test_validate_make():
    assert validate_make("Toyota")[0] is True
    assert validate_make("BMW")[0] is True
    assert validate_make("Mercedes-Benz")[0] is True
    assert validate_make("")[0] is False  # Empty
    assert validate_make("A")[0] is False  # Too short
    assert validate_make("A" * 51)[0] is False  # Too long
    assert validate_make("Citroën")[0] is True  # International
    assert validate_make("Škoda")[0] is True  # International
    assert validate_make("Toyota@")[0] is False  # Invalid char

def test_validate_model():
    assert validate_model("Camry")[0] is True
    assert validate_model("X5")[0] is True
    assert validate_model("F-150")[0] is True
    assert validate_model("")[0] is False  # Empty
    assert validate_model("A" * 51)[0] is False  # Too long
    assert validate_model("Mégane")[0] is True  # International
    assert validate_model("Camry!")[0] is False  # Invalid char

def test_validate_vin():
    assert validate_vin("")[0] is True  # Optional
    assert validate_vin("1HGCM82633A004352")[0] is True
    assert validate_vin("1HGCM82633A00435")[0] is False  # Too short
    assert validate_vin("1HGCM82633A0043522")[0] is False  # Too long
    assert validate_vin("1HGCM82633A00435!")[0] is False  # Invalid char

def test_validate_symptoms():
    valid_symptoms = "Car makes a noise." * 2
    assert validate_symptoms(valid_symptoms)[0] is True
    assert validate_symptoms("")[0] is False  # Empty
    assert validate_symptoms("Short")[0] is False  # Too short (<10)
    assert validate_symptoms("A" * 2001)[0] is False  # Too long

def test_validate_obd_codes():
    assert validate_obd_codes("")[0] is True  # Optional
    assert validate_obd_codes("P0300")[0] is True
    assert validate_obd_codes("P0300, P0420")[0] is True
    assert validate_obd_codes("C1234, B0001, U1000")[0] is True
    assert validate_obd_codes("P030")[0] is False  # Invalid format
    assert validate_obd_codes("X0300")[0] is False  # Invalid prefix
    assert validate_obd_codes("P0300, invalid")[0] is False
