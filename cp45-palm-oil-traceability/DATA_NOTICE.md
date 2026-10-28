# Data notice - read before making this repository public

This project uses **Bloomberg Terminal** data (functions SPLC, FA, ESG, CN, HP/GP, DES), transcribed by hand from screens captured
on **15 October 2026** at the Woxsen Bloomberg Lab. Bloomberg data are licensed and are normally **not** redistributable.

Bloomberg-derived values appear in:

| Location | What it contains |
|---|---|
| `data/Palm_Oil_Traceability_Capstone_Workbook.xlsx` | fundamentals, ESG scores, supplier lists, news log, prices |
| `workbook/wb_a.py`, `wb_b1.py`, `wb_b2.py` | the same values as Python dictionaries (the workbook is built from these) |
| `src/palm_oil_traceability_model.py` | 8-week price tables for KOZ6 Comdty, WIL SP, NESN SW, ULVR LN; FY2025 revenue and COGS |
| `data/derived/*.json`, `figures/*.png`, `report/output/*` | numbers and charts computed from the above |

**Recommended:** create the GitHub repository as **Private**, and confirm with your faculty supervisor / the Bloomberg Lab whether the
Woxsen licence allows academic code-sharing of transcribed values before you switch it to Public. If it does not, remove the files listed
above (or replace the values with placeholders) before publishing; the model code itself contains no Bloomberg data apart from the tables noted.

Everything marked **ASSUMPTION** in the model and the report (probabilities, fine rates, programme costs, effectiveness, FX, discount rate)
is a modelling input chosen by the authors; it is not Bloomberg data and not an observation.

A labelled classifier panel built from Bloomberg history (`data/panel/spoei_panel.csv`) is excluded from version control by `.gitignore`.
