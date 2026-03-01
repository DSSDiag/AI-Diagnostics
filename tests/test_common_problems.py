import os
import pytest
import src.storage
from src.storage import (
    create_common_problem,
    get_common_problem,
    get_all_common_problems,
    update_common_problem,
    delete_common_problem,
    search_common_problems,
)
from src.validation import validate_common_problem


@pytest.fixture(autouse=True)
def mock_common_problems_path(tmp_path, monkeypatch):
    """Use a temporary file for common problems storage during tests."""
    test_file = tmp_path / "test_common_problems.json"
    monkeypatch.setattr(src.storage, "COMMON_PROBLEMS_FILE", str(test_file))


# ---------------------------------------------------------------------------
# Storage tests
# ---------------------------------------------------------------------------

def _sample_entry(**kwargs):
    base = {
        "make": "Toyota",
        "model": "Hilux",
        "year_from": 2005,
        "year_to": 2015,
        "fault": "Rear main seal leak",
        "symptoms": ["Oil leak under engine", "Burning oil smell"],
        "repair": "Replace rear main seal and reseal mating surfaces.",
        "obd_codes": "",
        "added_by": "admin",
    }
    base.update(kwargs)
    return base


def test_create_and_retrieve():
    pid = create_common_problem(_sample_entry())
    assert pid is not None

    entry = get_common_problem(pid)
    assert entry is not None
    assert entry["make"] == "Toyota"
    assert entry["model"] == "Hilux"
    assert entry["problem_id"] == pid
    assert "created_at" in entry


def test_get_all():
    pid1 = create_common_problem(_sample_entry())
    pid2 = create_common_problem(_sample_entry(make="Ford", model="Ranger"))
    all_probs = get_all_common_problems()
    assert pid1 in all_probs
    assert pid2 in all_probs
    assert len(all_probs) == 2


def test_update_common_problem():
    pid = create_common_problem(_sample_entry())
    result = update_common_problem(pid, {"fault": "Updated fault description"})
    assert result is True
    entry = get_common_problem(pid)
    assert entry["fault"] == "Updated fault description"


def test_update_nonexistent_returns_false():
    result = update_common_problem("nonexistent-id", {"fault": "X"})
    assert result is False


def test_delete_common_problem():
    pid = create_common_problem(_sample_entry())
    result = delete_common_problem(pid)
    assert result is True
    assert get_common_problem(pid) is None


def test_delete_nonexistent_returns_false():
    result = delete_common_problem("nonexistent-id")
    assert result is False


def test_search_by_make():
    create_common_problem(_sample_entry(make="Toyota"))
    create_common_problem(_sample_entry(make="Ford", model="Ranger"))
    results = search_common_problems(make="Toyota")
    assert all(e["make"] == "Toyota" for e in results.values())
    assert len(results) == 1


def test_search_by_model():
    create_common_problem(_sample_entry(model="Hilux"))
    create_common_problem(_sample_entry(model="Camry"))
    results = search_common_problems(model="Camry")
    assert len(results) == 1
    assert list(results.values())[0]["model"] == "Camry"


def test_search_by_year_within_range():
    create_common_problem(_sample_entry(year_from=2005, year_to=2015))
    create_common_problem(_sample_entry(year_from=2016, year_to=2022, model="Camry"))

    results_2010 = search_common_problems(year=2010)
    assert len(results_2010) == 1

    results_2018 = search_common_problems(year=2018)
    assert len(results_2018) == 1
    assert list(results_2018.values())[0]["model"] == "Camry"

    results_all = search_common_problems()
    assert len(results_all) == 2


def test_search_no_match():
    create_common_problem(_sample_entry(make="Toyota"))
    results = search_common_problems(make="Ferrari")
    assert len(results) == 0


def test_search_empty_library():
    results = search_common_problems(make="Toyota")
    assert results == {}


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

def test_validate_valid_entry():
    errors = validate_common_problem(
        make="Toyota",
        model="Hilux",
        year_from=2005,
        year_to=2015,
        fault="Rear main seal leak",
        symptoms=["Oil leak", "Burning smell"],
        repair="Replace rear main seal.",
        obd_codes="",
    )
    assert errors == []


def test_validate_missing_make():
    errors = validate_common_problem(
        make="Select Make", model="Hilux", year_from=2005, year_to=2015,
        fault="Fault", symptoms=["Symptom"], repair="Repair",
    )
    assert any("make" in e.lower() for e in errors)


def test_validate_missing_model():
    errors = validate_common_problem(
        make="Toyota", model="", year_from=2005, year_to=2015,
        fault="Fault", symptoms=["Symptom"], repair="Repair",
    )
    assert any("model" in e.lower() for e in errors)


def test_validate_year_range_inverted():
    errors = validate_common_problem(
        make="Toyota", model="Hilux", year_from=2015, year_to=2005,
        fault="Fault", symptoms=["Symptom"], repair="Repair",
    )
    assert any("year" in e.lower() for e in errors)


def test_validate_missing_fault():
    errors = validate_common_problem(
        make="Toyota", model="Hilux", year_from=2005, year_to=2015,
        fault="", symptoms=["Symptom"], repair="Repair",
    )
    assert any("fault" in e.lower() for e in errors)


def test_validate_empty_symptoms():
    errors = validate_common_problem(
        make="Toyota", model="Hilux", year_from=2005, year_to=2015,
        fault="Fault", symptoms=[], repair="Repair",
    )
    assert any("symptom" in e.lower() for e in errors)


def test_validate_missing_repair():
    errors = validate_common_problem(
        make="Toyota", model="Hilux", year_from=2005, year_to=2015,
        fault="Fault", symptoms=["Symptom"], repair="",
    )
    assert any("repair" in e.lower() for e in errors)


def test_validate_invalid_obd_codes():
    errors = validate_common_problem(
        make="Toyota", model="Hilux", year_from=2005, year_to=2015,
        fault="Fault", symptoms=["Symptom"], repair="Repair",
        obd_codes="p0300; invalid!",
    )
    assert any("obd" in e.lower() for e in errors)


def test_validate_valid_obd_codes():
    errors = validate_common_problem(
        make="Toyota", model="Hilux", year_from=2005, year_to=2015,
        fault="Fault", symptoms=["Symptom"], repair="Repair",
        obd_codes="P0300, P0301",
    )
    assert errors == []
