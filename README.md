# Hung Council Watch: Forecasting Coalition Risk in South Africa's 2026 Local Elections

**DIRISA Student Datathon Challenge 2026 — Team Eduvos**

**Live dashboard:** https://eduvos-hung-councils.netlify.app
(includes a 2026 risk map and an election-day simulator; it also runs offline: open `docs/index.html` in any browser)

## The question

South African local politics has fragmented sharply. One-party-dominant municipalities fell from 70% in 2000 to 16% in 2021, and hung councils, where no party wins a majority, jumped from 27 after the 2016 election to 72 after 2021. Hung councils mean coalition government, which has been linked to unstable administrations, frequent changes of mayor and disrupted service delivery.

**Which South African municipalities are most likely to experience a hung council after the 2026 Local Government Elections, and how can two decades of political fragmentation data be used to forecast where coalition government will be needed?**

This matters to **voters and journalists** (where could the result change who governs?), **political parties** (where will coalitions be needed?) and **the IEC and government** (where to prepare for coalition instability before it happens).

We began by testing whether voter turnout follows an *inverted U* against political competition: low in one-party towns, highest in competitive councils and low again in fragmented ones. Tested across five elections and within municipalities over time, that hypothesis was not supported, which led us to the question above. The full story, including our initial and final problem statements, is in `notebooks/00_methodology.ipynb`.

## Key results

| | |
|---|---|
| Elections analysed | 2000, 2006, 2011, 2016 and 2021: all 213 current municipalities, with 263 councils linked across boundary changes |
| Main finding | One-party dominance collapsed (70% of municipalities in 2000, 16% in 2021) and hung councils rose from 27 to 72 between 2016 and 2021 |
| Model selected | Logistic regression on the leading party's vote share, chosen by validation in time order (forward chaining) over a baseline, a full logistic regression and tuned XGBoost |
| Test on the unseen 2021 election | ROC-AUC 0.88, PR-AUC 0.75; 62 of the 72 councils that became hung were flagged |
| Expected hung councils in 2026 | About 77 (72 after 2021), with 61 at high risk; about 100 if leading parties lose another 6 points |
| Highest average risk | Gauteng, Western Cape, Northern Cape, KwaZulu-Natal |

Tuned XGBoost scored best in standard cross-validation but was beaten on future elections, a key finding documented in the ML notebook.

## Repository structure

```
├── data/
│   ├── raw/                         Original IEC results, zipped (see data/raw/README.md)
│   │   └── 2021_provincial/         The nine 2021 provincial files
│   └── cleaned/                     Cleaned files produced by the 01_cleaning notebooks
├── notebooks/
│   ├── 00_methodology.ipynb             Problem statement (initial and final) and pipeline
│   ├── 01_cleaning_2000 … 2021.ipynb     Cleaning of each election
│   ├── 02_EDA_LGE_2000-2021.ipynb        Audit, linking, features, EDA and hypothesis tests
│   └── 03_ML_Hung_Councils_2026.ipynb    KMeans regimes, model comparison, 2026 forecast
├── outputs/                         Panel dataset, cleaning log, test results, 2026 forecast
├── models/                          Trained models (joblib)
├── figures/                         All charts used in the notebooks and slides
├── dashboard/                       Dashboard source code, data and build script
├── docs/
│   ├── index.html                   The built dashboard (single self-contained file)
│   └── validation_testing.md        Details of the validation layer and its tests
├── src/validation/                  Validators for the modelling panel and dashboard data
├── tests/                           Automated pytest suite for the validators
├── .github/workflows/               GitHub Actions: runs the tests on every push and pull request
├── reports/                         Presentation slides, video script and project guide
└── requirements.txt
```

## How to reproduce

1. **Install** Python 3.10 or newer, then the packages: `pip install -r requirements.txt`
2. **Run the notebooks.** Open Jupyter in this folder (`jupyter lab` or `jupyter notebook`) and run the notebooks in number order, each with **Kernel → Restart & Run All**:
   - `00_methodology` describes the problem and the pipeline
   - `01_cleaning_2000` to `01_cleaning_2021` recreate everything in `data/cleaned/` from `data/raw/`
   - `02_EDA_LGE_2000-2021` creates `outputs/lge_panel_2000_2021.csv` and the EDA figures
   - `03_ML_Hung_Councils_2026` trains the models and writes the 2026 forecast
3. **Validate and test** (optional): `python -m pytest` runs the 25 automated tests; the validator commands are listed [below](#running-the-validators).
4. **Rebuild the dashboard** (only after editing `dashboard/src/template.html`): `python dashboard/build_dashboard.py`, then copy `dashboard/dist/index.html` to `docs/index.html` (see `dashboard/README.md`).

All paths are relative, so no file locations need editing, and the whole pipeline runs from the raw files in under two minutes. The cleaned files are already included, so you can also start directly at `02_EDA`. Large CSV files are stored as `.zip`, and pandas reads them directly. The ML notebook takes one to two minutes because of the XGBoost tuning.

## Data sources

- Electoral Commission of South Africa (IEC), municipal election results 2000–2021: https://results.elections.org.za/home/downloads/me-results
- Municipal Demarcation Board, local municipality and province boundaries (used in the dashboard map)

## Data limitations

- **2016 turnout** in the cleaned file measures only the leading party's votes as a share of registered voters (found and proven in the EDA notebook, documented in `01_cleaning_2016`), so 2016 turnout is excluded; 2016 vote shares are used. Recomputing it from the raw file is future work.
- **2021 data** was originally combined in Excel and lost most of the Western Cape to Excel's row limit. `01_cleaning_2021` now combines the nine provincial files in code and checks that all 213 municipalities are present.
- **Hung council** is defined as the leading party winning less than 50% of the PR vote; exact seat rounding can occasionally differ.
- **Boundary changes** in 2006, 2011 and 2016: municipalities are linked across elections by code and name, so some histories cover slightly different areas.
- **Past results only:** the forecast does not include polling, new parties or local events, which is why the dashboard offers swing scenarios and an election-day simulator.
- **2024 national and provincial election results** are not yet used. That election, in which no party won a national majority and the MK party grew sharply, is the most recent signal of voter shifts; adding its results per municipality is our main planned next step.
- **One source type:** we used IEC municipal election results (2000–2021) plus Municipal Demarcation Board boundaries. Cross-referencing voter registration statistics and census data by municipality is planned future work.

## Software engineering validation layer

Alongside the data preparation, exploratory analysis, machine-learning forecasting and dashboard, the project includes a validation and automated-testing layer. It does not change the team's cleaning, EDA, modelling or dashboard work; it adds quality checks in front of the model and the website. Full details are in `docs/validation_testing.md`.

### 1. Modelling-panel validation

`src/validation/validate_panel.py` checks the combined 2000–2021 panel (`outputs/lge_panel_2000_2021.csv`) that the model is trained on:

- required columns are present and numeric fields contain valid numbers
- all five election years (2000, 2006, 2011, 2016, 2021) are represented
- there are no duplicate municipality–year records
- critical fields are not missing (turnout may be missing, because 2016 turnout is excluded)
- values are within valid ranges: turnout between 0 and 100, vote shares between 0 and 1, positive Effective Number of Parties, non-negative vote counts, metro flags of 0 or 1
- competition-regime labels are valid

### 2. Dashboard deployment-data validation

`src/validation/validate_dashboard_data.py` checks the JSON file the dashboard is built from (`dashboard/data/data.json`, covering all 213 municipalities) before deployment:

- the file exists and contains valid JSON
- required dashboard sections and municipality fields are present
- municipality identifiers are unique
- model metadata is present
- binary values contain only `0` or `1`
- probabilities and leading-party shares stay between `0` and `1`
- competition-regime values match those used by the dashboard

This validator checks the data contract the website expects; it does not assess the forecasting method itself.

### How it fits into the pipeline

```text
Raw IEC election results
        │
        ▼
Cleaning  →  EDA  →  modelling panel  →  panel validation
                                              │
                                              ▼
                                    Machine learning forecast
                                              │
                                              ▼
                     Dashboard deployment data  →  deployment-data validation
                                              │
                                              ▼
                                  Dashboard build  →  deployed website
```

### Automated testing

The tests in `tests/test_validate_panel.py` and `tests/test_validate_dashboard_data.py` cover valid and invalid cases, including missing fields, missing election years, negative vote counts, invalid turnout values, duplicate records, missing dashboard sections, duplicate municipality identifiers, invalid probabilities and invalid category values. They use synthetic data and never modify the real datasets or forecasts. A GitHub Actions workflow (`.github/workflows/validation-tests.yml`) runs them automatically on every push and pull request.

```bash
python -m pytest        # latest result: 25 passed
```

### Running the validators

```bash
python src/validation/validate_panel.py outputs/lge_panel_2000_2021.csv
python -m src.validation.validate_dashboard_data dashboard/data/data.json
```

Both currently pass on the real project data.

### Development workflow

The validation layer was developed on the feature branch `feature/validation-testing` and merged into `main` through a reviewed pull request (#1), so each change is traceable in the commit history.

## Presentation and documents

The `reports/` folder contains the presentation slides (22 slides, with references), the video script and a plain-language guide to the project and dashboard.

## Methods and references

- Laakso, M. & Taagepera, R. (1979). "Effective" number of parties. *Comparative Political Studies*, 12(1), 3–27.
- Lind, J. T. & Mehlum, H. (2010). With or without U? *Oxford Bulletin of Economics and Statistics*, 72(1), 109–118.
- Chen, T. & Guestrin, C. (2016). XGBoost: a scalable tree boosting system. *Proceedings of KDD 2016*, 785–794.
- Rousseeuw, P. J. (1987). Silhouettes. *Journal of Computational and Applied Mathematics*, 20, 53–65.
- Pedregosa, F. et al. (2011). Scikit-learn: machine learning in Python. *JMLR*, 12, 2825–2830.
- Tools: Python (pandas, NumPy, Matplotlib, SciPy, statsmodels, scikit-learn, XGBoost, joblib, pytest), Jupyter, D3.js, Netlify, Git, GitHub and GitHub Actions.

## Team Eduvos

| Name | Role |
|---|---|
| Thabang Manyama | Deployment and building machine learning models |
| Kamogelo Morweng | Building machine learning models and deployment |
| Ndodzo Sididzha | Data collection and deployment validation |
| Zwayi Mbokane | Data cleaning |
| Katlego Bopape | Data cleaning and building machine learning models |
| Unarine Luvhengo | Exploratory data analysis and presentations |
