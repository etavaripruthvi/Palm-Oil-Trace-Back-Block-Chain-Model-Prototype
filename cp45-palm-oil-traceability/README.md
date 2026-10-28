# CP-45: Blockchain-Based Sustainable Palm Oil Traceability

**Does a permissioned blockchain beat a central database for palm oil traceability, and what does Bloomberg data say about the exposure of Unilever, Nestlé and Wilmar?**

Capstone project CP-45 · Woxsen University, MBA (Business Analytics), Team 5 · Course: *Blockchain Supply Chain & Predictive Analytics* ·
Bloomberg data captured 15 October 2026 at the Woxsen Bloomberg Lab.

> **Read [`DATA_NOTICE.md`](DATA_NOTICE.md) before making this repository public.** The workbook, the data tables in the code, and the report contain
> Bloomberg-derived values. Create the repository as **Private** unless your licence allows sharing.

This repository contains everything behind the report: the cost-benefit and Monte Carlo model, the evidence workbook, the figures, the notebook, the
report builder, the finished report (DOCX + PDF) and 28 automated tests. One command rebuilds all derived outputs.

## Headline results

**Palm oil exposure index (SPOEI, 0-100, higher = more exposed).** Wilmar 63.5 · Unilever 53.0 · Nestlé 39.9. The order is the same under all four weightings,
under all 10 leave-one-indicator-out runs and in 78% of 20,000 random weight vectors.

**Net present value of traceability vs doing nothing (USD m, 7 years, 8% discount rate).**

| | Central database (Base / Adverse / Severe) | Permissioned blockchain (Base / Adverse / Severe) | P(blockchain beats database), mixed regimes |
|---|---|---|---|
| Unilever | 20 / 52 / 124 | 16 / 56 / 143 | 35% |
| Nestlé | 44 / 96 / 206 | 47 / 111 / 247 | 42% |
| Wilmar | 90 / 182 / 414 | 86 / 197 / 471 | 38% |

* The ledger only wins when enforcement is strict (Adverse and Severe); at base it ties or loses, and it carries a fatter downside tail.
* **Parity:** Unilever's ledger would need to cost 10.7% less (or regulatory risk be 1.8× higher) to tie with the database; Wilmar's 3.0% less (2.1×); Nestlé is already past parity at base (cost multiple 1.07).
* **Recommended path:** build the database first and keep it ledger-ready, switching only if enforcement proves severe.
* The palm oil chain is largely **invisible** in Bloomberg SPLC: plantations are only 0.4% of Wilmar's visible cost base.

### Evidence status

| Layer | Status |
|---|---|
| Fundamentals, ESG scores, supplier flags, prices, SPLC panels | Bloomberg, typed from screens on 15-Oct-2026 (spot-check against the Terminal) |
| News log | Bloomberg CN headlines grouped into 22 hand-coded event clusters (severity 0-5) |
| Event probabilities, fine rate, programme costs, effectiveness, FX, discount rate | **ASSUMPTION** (authors' judgement, flagged in the model, workbook and report) |
| Distress / controversy classifier (RQ3 prediction) | **Specified, not estimated.** No labelled panel exists; notebook Part 5 runs on a synthetic panel tagged `SYNTHETIC - code test, NOT EVIDENCE` |

## Quick start

```bash
git clone <your-repo-url> && cd cp45-palm-oil-traceability
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m unittest discover -s tests -v     # 28 tests, about 40 s
python scripts/run_all.py                   # rebuild numbers, figures, notebook and report, about 30 s
python src/palm_oil_traceability_model.py   # print the model's tables and refresh data/derived CSVs
```

`make test`, `make all`, `make report-docx`, `make workbook` and `make clean` do the same (see the `Makefile`).

* `run_all.py` writes the PDF only if **LibreOffice** (`soffice`) and **poppler** (`pdftoppm`) are installed; otherwise it builds the DOCX and skips the PDF
  (`--no-pdf` forces this). `make workbook` also needs LibreOffice, to recalculate formulas.
* To change an assumption: edit `G`, `SCEN`, `PROFILES` or `OPTIONS` in `src/palm_oil_traceability_model.py`, then run `scripts/run_all.py` and
  `scripts/build_workbook.py`. The numbers in the report update automatically.
* Tested with Python 3.13 and the exact versions in [`requirements-tested.txt`](requirements-tested.txt); `requirements.txt` gives the supported ranges.
  The ranges were not install-tested in a clean environment, so if `pip` resolves something newer and a test fails, fall back to the tested versions.
* The notebook (`notebooks/CP45_Palm_Oil_Traceability_Notebook.ipynb`) needs `pip install -r requirements-optional.txt` (Jupyter; XGBoost and SHAP are optional with fallbacks).

## Repository layout

```
cp45-palm-oil-traceability/
├── README.md · DATA_NOTICE.md · LICENSE · Makefile
├── requirements.txt · requirements-tested.txt · requirements-optional.txt
├── .github/workflows/ci.yml          tests + rebuild on every push
├── src/
│   ├── palm_oil_traceability_model.py   cost-benefit engine, Monte Carlo, tornado, coverage grid
│   └── cp45_style.py                    shared chart style
├── scripts/
│   ├── run_all.py                       one-command rebuild
│   ├── compute_numbers.py · compute_extras.py   → data/derived/*.json (SPOEI, NPVs, parity, staged strategy)
│   ├── make_figures.py (+ make_fig*.py) → figures/*.png
│   ├── build_notebook.py                → notebooks/*.ipynb
│   ├── build_report.py                  → report/output/*.docx (+ .pdf)
│   └── build_workbook.py                → build/workbook_rebuilt.xlsx (rebuilds the evidence workbook)
├── workbook/                          builders for the 16-sheet evidence workbook
├── report/
│   ├── builder/                       chapter modules ch_front, ch1-ch7, appx; build_docx.py
│   └── output/                        finished DOCX and PDF
├── data/
│   ├── Palm_Oil_Traceability_Capstone_Workbook.xlsx
│   ├── derived/                       JSON numbers quoted in the report
│   └── panel/                         where a labelled classifier panel would go (template only)
├── figures/                           18 charts (f01-f18)
├── notebooks/                         analysis notebook (Parts 1-5)
├── docs/METHODOLOGY.md · DATA_DICTIONARY.md
└── tests/                             28 unittest tests
```

Pipeline: `src/` model + `data/…Workbook.xlsx` → `data/derived/*.json` → `figures/` → `report/output/`. A full run reproduces the committed outputs exactly
(same JSON values, pixel-identical figures, identical report text).

## Documentation

* [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md): SPOEI, cost-benefit equations, Monte Carlo distributions, parity and staged strategy, classifier protocol, limitations
* [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md): workbook sheets, derived JSON files, figures, panel schema
* [`data/panel/README.md`](data/panel/README.md): how to supply the labelled panel that RQ3 needs

## Team 5

| Member | Contribution |
|---|---|
| Bodineni Sai Thanmai | Led project coordination: scope, research questions RQ1-RQ4 and report structure |
| Pruthvi Teja Etavari | Mapped all three supply chains in Bloomberg SPLC and showed the palm chain is invisible (plantations are only 0.4% of Wilmar's visible cost base) |
| Vibhaas Chandra | Compiled FY2019-25 financials and the margin and interest-cover analysis (Wilmar gross margin fell from 10.9% to 7.7%) |
| Aditya Roy | Coded the ESG, Scope 3 and news evidence (22 coded news events; Wilmar has the heaviest adverse record) |
| Samuel Jebaraj | Led the palm oil and equity market analysis and assembled the final report, workbook and notebook |
| Venkata Naga Saideep Koutarapu | Led the SPOEI risk index (Wilmar 63.5, Unilever 53.0, Nestlé 39.9) and the database vs blockchain stress test |

## Licence

Source code: MIT, see [`LICENSE`](LICENSE). The licence does **not** cover Bloomberg-derived data (see [`DATA_NOTICE.md`](DATA_NOTICE.md)).
This is an academic project, not investment, legal or compliance advice.
