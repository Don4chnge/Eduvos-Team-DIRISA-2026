from src.validation.validate_dashboard_data import (
    check_top_level_structure,
    check_municipality_structure,
    check_duplicate_municipality_ids,
    check_model_structure,
    check_municipality_values,
    validate_dashboard_data,
    
)

# Creates a small valid dashboard dataset for testing.
# The values are synthetic and are not real election forecasts.
def create_valid_dashboard_data():
    return {
        "munis": [
            {
                "id": "TEST001",
                "name": "Test Municipality",
                "prov": "Test Province",
                "metro": 0,
                "lp": "Test Party",
                "ts": 0.55,
                "enp": 2.1,
                "margin": 0.10,
                "parties": 5,
                "hung": 0,
                "p": 0.40,
                "rg": "Competitive",
                "to": 50.0,
                "hist": [],
                "xgb": 0.42,
            }
        ],
        "trend": [],
        "model": {
            "b0": 1.0,
            "b1": 2.0,
            "selected": "Test Model",
        },
        "rocs": {},
        "table": [],
        "swing_ref": 0.0,
    }

# Confirm that correctly structured deployment data passes validation.
def test_valid_dashboard_data_passes():
    data = create_valid_dashboard_data()

    assert validate_dashboard_data(data) is True

# Confirm that missing required data is detected
def test_missing_top_level_section_fails():
    data = create_valid_dashboard_data()
    del data["trend"]

    assert check_top_level_structure(data) is False

# Confirm that invalid probability and category values are rejected.
def test_missing_municipality_field_fails():
    data = create_valid_dashboard_data()
    del data["munis"][0]["p"]

    assert check_municipality_structure(data) is False


def test_duplicate_municipality_ids_fail():
    data = create_valid_dashboard_data()

    duplicate = data["munis"][0].copy()
    data["munis"].append(duplicate)

    assert check_duplicate_municipality_ids(data) is False


def test_missing_model_field_fails():
    data = create_valid_dashboard_data()
    del data["model"]["selected"]

    assert check_model_structure(data) is False
    
def test_probability_outside_range_fails():
    data = create_valid_dashboard_data()

    data["munis"][0]["p"] = 1.5

    assert check_municipality_values(data) is False


def test_invalid_regime_fails():
    data = create_valid_dashboard_data()

    data["munis"][0]["rg"] = "Unknown"

    assert check_municipality_values(data) is False


def test_invalid_binary_value_fails():
    data = create_valid_dashboard_data()

    data["munis"][0]["metro"] = 2

    assert check_municipality_values(data) is False