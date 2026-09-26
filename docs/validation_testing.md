# Validation and Testing

## Purpose

This contribution adds automated validation and testing around the existing project workflow.

It does not replace the team's existing data preparation, analysis, forecasting or dashboard work. Its purpose is to check that important data structures and values are valid before they are used by later parts of the project.

## Final Modelling Panel Validation

File:

`src/validation/validate_panel.py`

The validator checks the existing:

`outputs/lge_panel_2000_2021.csv`

Checks include:

- required columns
- expected election years
- numeric fields
- duplicate municipality/year records
- missing critical values
- valid metro values
- turnout ranges when turnout is available
- HHI, top-share and margin ranges
- positive ENP values
- valid party and vote-count values
- expected regime categories

Missing turnout values are allowed because the existing final panel contains unavailable turnout data for some records.

## Dashboard Data Validation

File:

`src/validation/validate_dashboard_data.py`

The validator checks:

`dashboard/data/data.json`

Checks include:

- valid JSON structure
- required top-level sections
- required municipality fields
- duplicate municipality IDs
- model metadata
- binary values
- probability and share ranges
- expected regime values

The validator was successfully run against the existing dashboard dataset containing 213 municipality records.

## Automated Tests

Tests are stored in:

- `tests/test_validate_panel.py`
- `tests/test_validate_dashboard_data.py`

Run all tests with:

```bash
python -m pytest

