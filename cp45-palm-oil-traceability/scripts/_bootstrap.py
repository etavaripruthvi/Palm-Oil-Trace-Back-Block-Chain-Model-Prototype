"""Shared path setup for every script in scripts/ (import this first)."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DERIVED = DATA / "derived"
FIGURES = ROOT / "figures"
WORKBOOK = DATA / "Palm_Oil_Traceability_Capstone_Workbook.xlsx"
for sub in ("src", "workbook", "report/builder"):
    p = str(ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)
DERIVED.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
