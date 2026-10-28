"""Put src/, workbook/, scripts/ and report/builder/ on sys.path for the tests."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
for sub in ("src", "workbook", "scripts", "report/builder"):
    p = str(ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)
DERIVED = ROOT / "data" / "derived"
WORKBOOK = ROOT / "data" / "Palm_Oil_Traceability_Capstone_Workbook.xlsx"
