import pandas as pd

from src.validation.validate_panel import validate_panel


def create_valid_panel():
    """Create a small synthetic panel matching the team's final schema."""
    return pd.DataFrame(
        {
            "year": [2000, 2006, 2011, 2016, 2021],
            "panel_id": ["M001", "M001", "M001", "M001", "M001"],
            "name": [
                "Test Municipality",
                "Test Municipality",
                "Test Municipality",
                "Test Municipality",
                "Test Municipality",
            ],
            "province": [
                "Test Province",
                "Test Province",
                "Test Province",
                "Test Province",
                "Test Province",
            ],
            "metro": [0, 0, 0, 0, 0],
            "turnout": [55.0, 54.0, 56.0, None, 58.0],
            "enp": [2.1, 2.2, 2.3, 2.4, 2.5],
            "hhi": [0.45, 0.44, 0.43, 0.42, 0.41],
            "top_share": [0.55, 0.54, 0.53, 0.52, 0.51],
            "margin": [0.15, 0.14, 0.13, 0.12, 0.11],
            "parties_contesting": [5, 5, 6, 6, 7],
            "leading_party": [
                "Test Party",
                "Test Party",
                "Test Party",
                "Test Party",
                "Test Party",
            ],
            "total_valid": [10000, 11000, 12000, 13000, 14000],
            "log_valid": [4.0, 4.1, 4.2, 4.3, 4.4],
            "regime": [
                "Competitive (2–3)",
                "Competitive (2–3)",
                "Competitive (2–3)",
                "Competitive (2–3)",
                "Competitive (2–3)",
            ],
        }
    )


def test_valid_panel_passes():
    data = create_valid_panel()

    assert validate_panel(data) is True


def test_missing_required_column_fails():
    data = create_valid_panel()
    data = data.drop(columns=["province"])

    assert validate_panel(data) is False


def test_non_numeric_value_fails():
    data = create_valid_panel()

    # Convert the column to object so the test can deliberately
    # insert invalid text and verify that the validator catches it.
    data["enp"] = data["enp"].astype(object)
    data.loc[0, "enp"] = "invalid"

    assert validate_panel(data) is False

def test_missing_expected_year_fails():
    data = create_valid_panel()
    data = data[data["year"] != 2021]

    assert validate_panel(data) is False


def test_duplicate_year_panel_id_fails():
    data = create_valid_panel()

    duplicate = data.iloc[[0]].copy()
    data = pd.concat([data, duplicate], ignore_index=True)

    assert validate_panel(data) is False


def test_missing_critical_value_fails():
    data = create_valid_panel()
    data.loc[0, "province"] = None

    assert validate_panel(data) is False


def test_missing_turnout_is_allowed():
    data = create_valid_panel()
    data["turnout"] = None

    assert validate_panel(data) is True


def test_invalid_metro_value_fails():
    data = create_valid_panel()
    data.loc[0, "metro"] = 2

    assert validate_panel(data) is False


def test_invalid_turnout_value_fails():
    data = create_valid_panel()
    data.loc[0, "turnout"] = 150

    assert validate_panel(data) is False


def test_invalid_hhi_value_fails():
    data = create_valid_panel()
    data.loc[0, "hhi"] = 1.5

    assert validate_panel(data) is False


def test_invalid_top_share_value_fails():
    data = create_valid_panel()
    data.loc[0, "top_share"] = -0.1

    assert validate_panel(data) is False


def test_invalid_margin_value_fails():
    data = create_valid_panel()
    data.loc[0, "margin"] = 1.2

    assert validate_panel(data) is False


def test_invalid_enp_value_fails():
    data = create_valid_panel()
    data.loc[0, "enp"] = 0

    assert validate_panel(data) is False


def test_invalid_parties_contesting_fails():
    data = create_valid_panel()
    data.loc[0, "parties_contesting"] = 0

    assert validate_panel(data) is False


def test_negative_total_valid_fails():
    data = create_valid_panel()
    data.loc[0, "total_valid"] = -1

    assert validate_panel(data) is False


def test_negative_log_valid_fails():
    data = create_valid_panel()
    data.loc[0, "log_valid"] = -1

    assert validate_panel(data) is False


def test_invalid_regime_fails():
    data = create_valid_panel()
    data.loc[0, "regime"] = "Unknown"

    assert validate_panel(data) is False