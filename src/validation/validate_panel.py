import sys
from pathlib import Path

import pandas as pd


# The schema expected from the team's final modelling panel.
REQUIRED_COLUMNS = {
    "year",
    "panel_id",
    "name",
    "province",
    "metro",
    "turnout",
    "enp",
    "hhi",
    "top_share",
    "margin",
    "parties_contesting",
    "leading_party",
    "total_valid",
    "log_valid",
    "regime",
}

EXPECTED_YEARS = {2000, 2006, 2011, 2016, 2021}

VALID_REGIMES = {
    "Dominant (ENP < 2)",
    "Competitive (2–3)",
    "Fragmented (ENP ≥ 3)",
}

NUMERIC_COLUMNS = {
    "year",
    "metro",
    "turnout",
    "enp",
    "hhi",
    "top_share",
    "margin",
    "parties_contesting",
    "total_valid",
    "log_valid",
}

# Turnout is intentionally excluded because the finished team panel
# contains missing turnout values, especially for 2016.
CRITICAL_COLUMNS = REQUIRED_COLUMNS - {"turnout"}


def load_panel(file_path):
    """Load the final modelling panel from CSV."""
    path = Path(file_path)

    if not path.exists():
        print(f"[FAIL] Panel file not found: {path}")
        return None

    try:
        data = pd.read_csv(path)
    except Exception as error:
        print(f"[FAIL] Could not read panel file: {error}")
        return None

    print(f"[PASS] Panel file loaded: {path.name}")
    return data


def check_required_columns(data):
    """Check that the final panel contains all required columns."""
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        print(
            "[FAIL] Missing required columns:",
            ", ".join(sorted(missing_columns)),
        )
        return False

    print("[PASS] Required panel columns are present.")
    return True


def check_numeric_columns(data):
    """Check that expected numeric fields contain numeric values."""
    for column in NUMERIC_COLUMNS:
        converted = pd.to_numeric(data[column], errors="coerce")

        invalid_values = converted.isna() & data[column].notna()

        if invalid_values.any():
            print(f"[FAIL] Non-numeric values found in '{column}'.")
            return False

    print("[PASS] Numeric panel fields contain valid numeric values.")
    return True


def check_expected_years(data):
    """Check that the panel contains the expected election years."""
    years = set(
        pd.to_numeric(data["year"], errors="coerce")
        .dropna()
        .astype(int)
        .unique()
    )

    if years != EXPECTED_YEARS:
        print(
            f"[FAIL] Election years do not match expected years. "
            f"Found: {sorted(years)}"
        )
        return False

    print("[PASS] Expected election years are present.")
    return True


def check_duplicate_records(data):
    """Check for duplicate municipality/year panel records."""
    duplicates = data.duplicated(
        subset=["year", "panel_id"],
        keep=False,
    )

    if duplicates.any():
        print(
            f"[FAIL] Found {duplicates.sum()} rows involved in "
            "duplicate year/panel_id records."
        )
        return False

    print("[PASS] No duplicate municipality/year records found.")
    return True


def check_critical_missing_values(data):
    """
    Check fields that must be populated.

    Turnout is not treated as critical because missing turnout values
    are part of the team's existing final panel.
    """
    missing = data[list(CRITICAL_COLUMNS)].isna().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        print("[FAIL] Missing values found in critical fields:")
        print(missing.to_string())
        return False

    print("[PASS] No missing values found in critical fields.")
    return True


def check_value_ranges(data):
    """Check basic integrity rules for numeric panel values."""

    if not data["metro"].isin([0, 1]).all():
        print("[FAIL] Metro must contain only 0 or 1.")
        return False

    turnout = data["turnout"].dropna()

    if not turnout.between(0, 100).all():
        print("[FAIL] Turnout values must be between 0 and 100.")
        return False

    for column in ["hhi", "top_share", "margin"]:
        if not data[column].between(0, 1).all():
            print(f"[FAIL] {column} values must be between 0 and 1.")
            return False

    if not (data["enp"] > 0).all():
        print("[FAIL] ENP values must be greater than 0.")
        return False

    if not (data["parties_contesting"] >= 1).all():
        print("[FAIL] parties_contesting must be at least 1.")
        return False

    if not (data["total_valid"] >= 0).all():
        print("[FAIL] total_valid cannot contain negative values.")
        return False

    if not (data["log_valid"] >= 0).all():
        print("[FAIL] log_valid cannot contain negative values.")
        return False

    print("[PASS] Panel numeric values are within valid ranges.")
    return True


def check_regime_values(data):
    """Check that regime labels match the team's panel categories."""
    invalid_regimes = set(data["regime"].dropna().unique()) - VALID_REGIMES

    if invalid_regimes:
        print(
            "[FAIL] Invalid regime values found:",
            ", ".join(sorted(invalid_regimes)),
        )
        return False

    print("[PASS] Panel regime values are valid.")
    return True


def validate_panel(data):
    """
    Validate the final modelling-panel contract.

    This function reports integrity problems only.
    It does not clean or modify the team's dataset.
    """
    checks = [
        check_required_columns,
        check_numeric_columns,
        check_expected_years,
        check_duplicate_records,
        check_critical_missing_values,
        check_value_ranges,
        check_regime_values,
    ]

    for check in checks:
        if not check(data):
            return False

    return True

def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python src/validation/validate_panel.py "
            "outputs/lge_panel_2000_2021.csv"
        )
        return 1

    data = load_panel(sys.argv[1])

    if data is None:
        return 1

    print("\nRunning modelling-panel checks...")

    if validate_panel(data):
        print("\n[PASS] Final modelling panel is valid.")
        return 0

    print("\n[FAIL] Final modelling panel failed validation.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())