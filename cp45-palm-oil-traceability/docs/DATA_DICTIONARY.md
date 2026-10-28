# Data dictionary

## 1. Evidence workbook - `data/Palm_Oil_Traceability_Capstone_Workbook.xlsx`

16 sheets, built by `scripts/build_workbook.py` from `workbook/wb_*.py`. Blue text = typed value (Bloomberg or assumption), black = formula,
green = cross-sheet link, yellow fill = key assumption / headline output.

| Sheet | Contents | Nature |
|---|---|---|
| `Start_Here` | purpose, colour legend, sheet map, review of the draft plan | text |
| `Summary` | headline results and findings | live formulas |
| `Assumptions` | all judgement inputs and the Base / Adverse / Severe switch | **ASSUMPTION** |
| `ROI_ULVR`, `ROI_NESN`, `ROI_WIL` | year-by-year cost-benefit: SQ vs DB vs BC | live formulas |
| `MC_Results` | Monte Carlo (20,000 draws x 4 regimes) | static, from Python |
| `Sensitivity` | tornado and coverage x substitution heat map | static, from Python |
| `Risk_Index` | SPOEI, three weight sets | formulas on Bloomberg inputs |
| `Supply_Chain` | SPLC panels, Wilmar supplier table, brand-owner supplier tables, HHI, coverage | Bloomberg SPLC |
| `News_Events` | hand-coded controversy log (12-month window) | Bloomberg CN, hand-coded |
| `ESG` | BESG scores and GHG scopes | Bloomberg ESG |
| `Fundamentals` | income statement, balance sheet, cash flow, ratios (FY2019-25) | Bloomberg FA |
| `Market_Data` | snapshot and CPO futures statistics | Bloomberg DES / GP |
| `Price_Analytics` | aligned daily prices, returns, volatility, correlation, beta | Bloomberg HP/GP |
| `Next_Steps` | data still to pull and the Bloomberg route for each | text |

`MC_Results` and `Sensitivity` are written by the Python model and are *not* formulas; change `src/palm_oil_traceability_model.py`, then re-run
`python scripts/build_workbook.py` (or `make workbook`).

## 2. Derived numbers - `data/derived/*.json`

Written by `scripts/compute_numbers.py`, `compute_extras.py`, `make_figs_diagnostics.py`, `make_figs_scenarios.py`, `make_fig_heatmap.py`; read by the report builder and tests.

| File | Content |
|---|---|
| `nums.json` | every number quoted in the report: margins (`gm_/om_/cov_/dio_/fcf_/rev_` x ULVR/NESN/WIL), SPOEI indicator values and scores (`ind`, `score`, `score_exnews`), SPLC visibility (`w_*`, `n_*`, `u_*`), deterministic results (`det`), Monte Carlo summary (`mc`), `cpo_sigma`, market statistics (`mkt`), tornado, parity, blueprint |
| `parity2.json` | per firm: `cost_mult`, `preg_mult` and the DB / BC cost inputs used |
| `staged.json` | keys `"<firm>|<series>"` for DB, BC, "Staged (upper)", "Staged (conservative)"; values `mean`, `p5`, `ppos` (USD m / probability) |
| `power.json` | sample-size / power curve for the AUC test (`f16_power.png`) |
| `fine_rob.json` | robustness of the BC-vs-DB conclusion to the fine rate |
| `impact.json` | operating-income impact (`oi`, `imp`, `imp_sev`) behind the risk-return heat map |

## 3. Figures - `figures/`

| File | Shows |
|---|---|
| f01_margins | gross and operating margins, FY2019-25, three firms |
| f02_cpo_equities | Bursa Malaysia CPO Dec-26 contract (KOZ6 Comdty) and the three equities rebased to 100 at 17-Aug-2026 |
| f03_besg_scope1 | Bloomberg ESG disclosure score (BESG) and Scope 1 emissions (2016 = 100) |
| f04_scope3 | Scope 3 emissions and 2024 intensity (kt CO2e per USD bn revenue) |
| f05_splc_visibility | supplier cost visible in SPLC as % of COGS, and share of listed suppliers carrying a Bloomberg flag |
| f06_news | hand-coded Bloomberg CN headlines, last 12 months (bubble size = severity 1-5) |
| f07_spoei | SPOEI indicator heat map (base weights) and SPOEI under four weightings |
| f08_architecture | permissioned traceability architecture: physical flow, oracle inputs, ledger events, contracts |
| f09_scenario_npv | NPV benefit vs status quo, by firm and scenario |
| f10_cost_decomp | PV of total cost by option, base scenario |
| f11_mc | Monte Carlo NPV distributions |
| f12_tornado | one-at-a-time sensitivity of the Unilever blockchain NPV |
| f13_cov_excl | PV of supplier-substitution cost: coverage x exclusion share |
| f14_leverage | Wilmar's visible suppliers: criticality to Wilmar vs Wilmar's leverage over the supplier |
| f15_risk_return | expected benefit vs 5th-percentile downside of each intervention |
| f16_power | positive events needed to detect a given AUC against chance (Hanley-McNeil, 80% power) |
| f17_spoei_gap | what makes Wilmar's SPOEI higher than Nestle's and Unilever's |
| f18_heatmap | risk-cost heat map: SPOEI vs economic impact of untraced exposure (bubble size = blockchain NPV) |

## 4. Classifier panel (not supplied) - `data/panel/`

See `data/panel/README.md` for the column definitions. The notebook looks for `data/panel/spoei_panel.csv`.
