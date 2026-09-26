import json
import sys
from pathlib import Path

# Defines the sections that the dashboard expects in data.json.
# If one of these sections is missing, the website may fail to build
# or display incomplete information.

EXPECTED_TOP_LEVEL_KEYS = {
    "munis",
    "trend",
    "model",
    "rocs",
    "table",
    "swing_ref",
}

VALID_REGIMES = {
    "Competitive",
    "Dominant",
    "Fragmented",
}


BINARY_VALUES = {
    0,
    1,
}

# Each municipality record must contain these fields because
# the existing dashboard uses them for maps, charts, forecasts,
# historical information and the election simulator.

REQUIRED_MUNICIPALITY_FIELDS = {
    "id",
    "name",
    "prov",
    "metro",
    "lp",
    "ts",
    "enp",
    "margin",
    "parties",
    "hung",
    "p",
    "rg",
    "to",
    "hist",
    "xgb",
}


REQUIRED_MODEL_FIELDS = {
    "b0",
    "b1",
    "selected",
}

 #Load the dashboard JSON file and confirm that it is valid JSON.
def load_dashboard_data(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"[FAIL] Dashboard data file not found: {path}")
        return None

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError:
        print("[FAIL] Dashboard data is not valid JSON.")
        return None

    print(f"[PASS] Dashboard data file loaded: {path.name}")

    return data

#Check that all major sections required by the dashboard exist.
def check_top_level_structure(data):
    if not isinstance(data, dict):
        print("[FAIL] Dashboard data must contain a JSON object.")
        return False

    missing_keys = EXPECTED_TOP_LEVEL_KEYS - set(data.keys())

    if missing_keys:
        print(
            "[FAIL] Missing dashboard sections: "
            + ", ".join(sorted(missing_keys))
        )
        return False

    print("[PASS] Dashboard top-level structure is valid.")

    return True

#Check that every municipality contains the fields used by the website.
def check_municipality_structure(data):
    municipalities = data.get("munis")

    if not isinstance(municipalities, list):
        print("[FAIL] 'munis' must be a list.")
        return False

    if len(municipalities) == 0:
        print("[FAIL] No municipality records found.")
        return False

    for index, municipality in enumerate(municipalities):
        if not isinstance(municipality, dict):
            print(
                f"[FAIL] Municipality record {index} "
                "is not a JSON object."
            )
            return False

        missing_fields = (
            REQUIRED_MUNICIPALITY_FIELDS
            - set(municipality.keys())
        )

        if missing_fields:
            print(
                f"[FAIL] Municipality record {index} "
                f"is missing fields: "
                f"{', '.join(sorted(missing_fields))}"
            )
            return False

    print(
        f"[PASS] Municipality structure is valid "
        f"for {len(municipalities)} records."
    )

    return True

#Prevent duplicate municipality records from reaching the dashboard.
def check_duplicate_municipality_ids(data):
    municipalities = data["munis"]

    municipality_ids = [
        municipality["id"]
        for municipality in municipalities
    ]

    if len(municipality_ids) != len(set(municipality_ids)):
        print("[FAIL] Duplicate municipality IDs found.")
        return False

    print("[PASS] No duplicate municipality IDs found.")

    return True

#Check dashboard values such as probabilities and binary indicators.
def check_municipality_values(data):
    municipalities = data["munis"]

    for index, municipality in enumerate(municipalities):
        regime = municipality["rg"]

        if regime not in VALID_REGIMES:
            print(
                f"[FAIL] Municipality record {index} "
                f"has invalid regime: {regime}"
            )
            return False

        if municipality["metro"] not in BINARY_VALUES:
            print(
                f"[FAIL] Municipality record {index} "
                "has an invalid metro value."
            )
            return False

        if municipality["hung"] not in BINARY_VALUES:
            print(
                f"[FAIL] Municipality record {index} "
                "has an invalid hung value."
            )
            return False

        for field in ["p", "xgb", "ts"]:
            value = municipality[field]

            if not isinstance(value, (int, float)):
                print(
                    f"[FAIL] Municipality record {index} "
                    f"has a non-numeric {field} value."
                )
                return False

            if value < 0 or value > 1:
                print(
                    f"[FAIL] Municipality record {index} "
                    f"has {field} outside 0-1."
                )
                return False

    print("[PASS] Municipality values are within valid ranges.")

    return True

#Check that the model metadata required by the dashboard is present
def check_model_structure(data):
    model = data.get("model")

    if not isinstance(model, dict):
        print("[FAIL] 'model' must be a JSON object.")
        return False

    missing_fields = REQUIRED_MODEL_FIELDS - set(model.keys())

    if missing_fields:
        print(
            "[FAIL] Model information is missing fields: "
            + ", ".join(sorted(missing_fields))
        )
        return False

    print("[PASS] Model metadata structure is valid.")

    return True

#Run all dashboard deployment validation checks.
def validate_dashboard_data(data):
    checks = [
        check_top_level_structure(data),
    ]

    if not all(checks):
        return False

    checks.extend(
        [
            check_municipality_structure(data),
            check_duplicate_municipality_ids(data),
            check_model_structure(data),
            check_municipality_values(data),
        ]
    )

    return all(checks)


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python -m "
            "src.validation.validate_dashboard_data "
            "<data.json>"
        )
        return 1

    data = load_dashboard_data(sys.argv[1])

    if data is None:
        return 1

    print("\nRunning dashboard deployment checks...")

    if validate_dashboard_data(data):
        print("\n[PASS] Dashboard deployment data is valid.")
        return 0

    print("\n[FAIL] Dashboard deployment data is invalid.")
    return 1

# Only run the command-line validator when this file is executed directly.
# This allows the functions to also be imported safely by pytest.

if __name__ == "__main__":
    raise SystemExit(main())