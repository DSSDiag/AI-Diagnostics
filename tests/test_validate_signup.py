import pytest
from datetime import date
from src.validation import validate_signup


def _valid_dob():
    """Return a date-of-birth for a 30-year-old (exact year arithmetic)."""
    today = date.today()
    return today.replace(year=today.year - 30)


def test_validate_signup_valid():
    errors = validate_signup(
        name="Alice Smith",
        email="alice@example.com",
        password="SecurePass1",
        dob=_valid_dob(),
        occupation="Mechanic",
    )
    assert errors == []


def test_validate_signup_missing_name():
    errors = validate_signup("", "a@b.com", "Password1", _valid_dob(), "Tech")
    assert "Full name is required." in errors


def test_validate_signup_short_name():
    errors = validate_signup("A", "a@b.com", "Password1", _valid_dob(), "Tech")
    assert "Name must be at least 2 characters." in errors


def test_validate_signup_long_name():
    errors = validate_signup("A" * 101, "a@b.com", "Password1", _valid_dob(), "Tech")
    assert "Name must be less than 100 characters." in errors


def test_validate_signup_name_xss():
    errors = validate_signup("<script>alert(1)</script>", "a@b.com", "Password1", _valid_dob(), "Tech")
    assert "Invalid characters detected in name." in errors


def test_validate_signup_name_html_tag():
    errors = validate_signup('<img onerror="bad()">', "a@b.com", "Password1", _valid_dob(), "Tech")
    assert "Invalid characters detected in name." in errors


def test_validate_signup_missing_email():
    errors = validate_signup("Bob", "", "Password1", _valid_dob(), "Driver")
    assert "Email address is required." in errors


def test_validate_signup_invalid_email():
    errors = validate_signup("Bob", "notanemail", "Password1", _valid_dob(), "Driver")
    assert "Please enter a valid email address." in errors


def test_validate_signup_email_too_long():
    long_email = "a" * 250 + "@b.com"
    errors = validate_signup("Bob", long_email, "Password1", _valid_dob(), "Driver")
    assert "Email address is too long." in errors


def test_validate_signup_missing_password():
    errors = validate_signup("Bob", "b@b.com", "", _valid_dob(), "Driver")
    assert "Password is required." in errors


def test_validate_signup_short_password():
    errors = validate_signup("Bob", "b@b.com", "Abc1", _valid_dob(), "Driver")
    assert "Password must be at least 8 characters long." in errors


def test_validate_signup_password_no_letter():
    errors = validate_signup("Bob", "b@b.com", "12345678", _valid_dob(), "Driver")
    assert "Password must contain at least one letter." in errors


def test_validate_signup_password_no_digit():
    errors = validate_signup("Bob", "b@b.com", "NoDigits!", _valid_dob(), "Driver")
    assert "Password must contain at least one number." in errors


def test_validate_signup_too_young():
    today = date.today()
    young_dob = today.replace(year=today.year - 10)
    errors = validate_signup("Bob", "b@b.com", "Password1", young_dob, "Student")
    assert "You must be at least 16 years old to register." in errors


def test_validate_signup_invalid_dob():
    errors = validate_signup("Bob", "b@b.com", "Password1", "not-a-date", "Driver")
    assert "Please enter a valid date of birth." in errors


def test_validate_signup_missing_dob():
    errors = validate_signup("Bob", "b@b.com", "Password1", None, "Driver")
    assert "Date of birth is required." in errors


def test_validate_signup_missing_occupation():
    errors = validate_signup("Bob", "b@b.com", "Password1", _valid_dob(), "")
    assert "Occupation is required." in errors


def test_validate_signup_occupation_too_long():
    errors = validate_signup("Bob", "b@b.com", "Password1", _valid_dob(), "O" * 101)
    assert "Occupation must be less than 100 characters." in errors


def test_validate_signup_occupation_xss():
    errors = validate_signup("Bob", "b@b.com", "Password1", _valid_dob(), "<script>bad()</script>")
    assert "Invalid characters detected in occupation." in errors


def test_validate_signup_dob_string():
    errors = validate_signup("Bob", "b@b.com", "Password1", "1990-06-15", "Technician")
    assert errors == []
