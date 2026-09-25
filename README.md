# Hung Council Watch: Forecasting Coalition Risk in South Africa's 2026 Local Elections

**DIRISA Student Datathon Challenge 2026 - Team Eduvos**

**Live dashboard:** https://eduvos-hung-councils.netlify.app
(includes an election-day simulator; also runs offline: open `docs/index.html` in any browser)

## The question

South African local politics has fragmented sharply: one-party-dominant municipalities fell from 70% in 2000 to 16% in 2021, and hung councils, where no party wins a majority, jumped from 27 after the 2016 election to 72 after 2021. Hung councils mean coalition government, which has been linked to unstable administrations and disrupted service delivery.

**Which South African municipalities are most likely to experience a hung council after the 2026 Local Government Elections, and how can two decades of political fragmentation data be used to forecast where coalition government will be needed?**

This matters to **voters and journalists** (where could the result change who governs?), **political parties** (where will coalitions be needed?) and **the IEC and government** (where to prepare for coalition instability).

We began by testing whether voter turnout follows an *inverted U* against political competition. Tested across five elections, that hypothesis was not supported, which led us to the question above. The full story is in `notebooks/00\_methodology.ipynb`.

## Key results

|||
|-|-|
|Elections analysed|2000, 2006, 2011, 2016 and 2021 (all 213 current municipalities)|
|Model selected|Logistic regression on the leading party's vote share, chosen by forward-chaining validation|
|Test on the unseen 2021 election|ROC-AUC 0.88, PR-AUC 0.75; 62 of 72 hung councils flagged|
|Expected hung councils in 2026|About 77 (72 after 2021); about 100 if leading parties lose another 6 points|
|Highest average risk|Gauteng, Western Cape, Northern Cape, KwaZulu-Natal|

Tuned XGBoost scored best in standard cross-validation but was beaten on future elections, a key finding documented in the ML notebook.

## Repository structure

```
├── data/
│   ├── raw/                     Original IEC results, zipped (see data/raw/README.md)
│   │   └── 2021\_provincial/     The nine 2021 provincial files
│   └── cleaned/                 Cleaned files produced by the 01\_cleaning notebooks
├── notebooks/
│   ├── 00\_methodology.ipynb             Problem statement (initial and final) and pipeline
│   ├── 01\_cleaning\_2000 … 2021.ipynb     Cleaning of each election
│   ├── 02\_EDA\_LGE\_2000-2021.ipynb       Audit, linking, features, EDA and hypothesis tests
│   └── 03\_ML\_Hung\_Councils\_2026.ipynb   KMeans regimes, model comparison, 2026 forecast
├── outputs/                     Panel dataset, cleaning log, test results, 2026 forecast
├── models/                      Trained models (joblib)
├── figures/                     All charts used in the report and slides
├── dashboard/                   Dashboard source code and build script
├── docs/index.html              The built dashboard (also served by GitHub Pages)
└── reports/                     Project guide, presentation slides and speaker script
```

## How to reproduce

1. Install Python 3.10 or newer, then the packages: `pip install -r requirements.txt`
2. Open Jupyter in this folder: `jupyter lab` (or `jupyter notebook`)
3. Run the notebooks in number order, each with **Kernel → Restart \& Run All**:

   * `01\_cleaning\_2000` to `01\_cleaning\_2021` recreate everything in `data/cleaned/` from `data/raw/`
   * `02\_EDA\_LGE\_2000-2021` creates `outputs/lge\_panel\_2000\_2021.csv` and the EDA figures
   * `03\_ML\_Hung\_Councils\_2026` trains the models and writes the 2026 forecast

All paths are relative, so no file locations need editing. The cleaned files are already included, so you can also start directly at `02\_EDA`. Large CSV files are stored as `.zip`; pandas reads them directly. The ML notebook takes one to two minutes because of the XGBoost tuning.

To rebuild the dashboard after editing `dashboard/src/template.html`, run `python dashboard/build\_dashboard.py` (see `dashboard/README.md`).

## Data sources

* Electoral Commission of South Africa (IEC), municipal election results 2000–2021: https://results.elections.org.za/home/downloads/me-results
* Municipal Demarcation Board, local municipality and province boundaries (used in the dashboard map)

## Data limitations

* **2016 turnout** in the cleaned file measures only the leading party's votes as a share of registered voters (found and proven in the EDA notebook, documented in `01\_cleaning\_2016`), so 2016 turnout is excluded; 2016 vote shares are used. Recomputing it from the raw file is future work.
* **2021 data** was originally combined in Excel and lost most of the Western Cape to Excel's row limit. `01\_cleaning\_2021` now combines the nine provincial files in code and checks that all 213 municipalities are present.
* **Hung council** is defined as the leading party winning less than 50% of the PR vote; exact seat rounding can occasionally differ.
* **Boundary changes** in 2006, 2011 and 2016: municipalities are linked across elections by code and name, so some histories cover slightly different areas.
* The forecast uses past election results only; polling, new parties and local events are not included, which is why the dashboard offers swing scenarios.

## Methods and references

* Laakso, M. \& Taagepera, R. (1979). "Effective" number of parties. *Comparative Political Studies*, 12(1), 3–27.
* Lind, J. T. \& Mehlum, H. (2010). With or without U? *Oxford Bulletin of Economics and Statistics*, 72(1), 109–118.
* Chen, T. \& Guestrin, C. (2016). XGBoost: a scalable tree boosting system. *Proceedings of KDD 2016*, 785–794.
* Rousseeuw, P. J. (1987). Silhouettes. *Journal of Computational and Applied Mathematics*, 20, 53–65.
* Pedregosa, F. et al. (2011). Scikit-learn: machine learning in Python. *JMLR*, 12, 2825–2830.
* Tools: Python (pandas, NumPy, Matplotlib, SciPy, statsmodels, scikit-learn, XGBoost, joblib), Jupyter, D3.js, Netlify.

## Team Eduvos

|Name|Role|
|-|-|
|*Thabang Manyama*|*Deployment \& Building machine learning models*|
|*Kamogelo Morweng*|*Building machine learning models \& Deployment*|
|*Ndodzo Sididzha*|*Data collection*|
|*Zwayi Mbokane*|*Data Cleaning*|
|*Katlego Bopape*|*Data Cleaning \& Building machine learning models*|
|*Unarine Luvhengo*|*Exploratory data analysis \& presentations<br />*|



