"""Rebuild the 16-sheet evidence workbook from the Python data modules in workbook/.

Default: writes build/workbook_rebuilt.xlsx (formulas, then LibreOffice recalculation so cached values exist)
and leaves the shipped data/Palm_Oil_Traceability_Capstone_Workbook.xlsx untouched.
    python scripts/build_workbook.py                 # rebuild + recalc into build/
    python scripts/build_workbook.py --install       # ...and overwrite the shipped workbook with the result
    python scripts/build_workbook.py --no-recalc     # skip LibreOffice (formulas only; Excel recalculates on open)
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _bootstrap import ROOT, WORKBOOK
from openpyxl import Workbook
import wb_a, wb_b1, wb_b2, wb_c1, wb_c2, wb_c3


def build(out: Path) -> Path:
    wb = Workbook()
    wb.remove(wb.active)
    wb_a.build_fundamentals(wb); wb_a.build_market(wb); wb_a.build_prices(wb); wb_a.build_esg(wb)
    wb_b1.build_supply(wb); wb_b2.build_news(wb); wb_b2.build_risk(wb)
    wb_c1.build_assumptions(wb)
    for co, nm, pc in wb_c1.PROF:
        wb_c1.build_roi(wb, co, nm, pc)
    wb_c2.build_mc(wb); wb_c2.build_sens(wb)
    wb_c3.build_front(wb)
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


def recalc(path: Path) -> bool:
    """Open + re-save with headless LibreOffice so every formula has a cached value. Returns False if soffice is missing."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        print("[warn] LibreOffice not found: formulas have no cached values (Excel will compute them on open).")
        return False
    with tempfile.TemporaryDirectory() as td:
        subprocess.run([soffice, "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", td, str(path)],
                       check=True, capture_output=True, timeout=300)
        shutil.move(str(Path(td) / path.name), str(path))
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "build" / "workbook_rebuilt.xlsx")
    ap.add_argument("--no-recalc", action="store_true")
    ap.add_argument("--install", action="store_true", help="copy the result over data/Palm_Oil_Traceability_Capstone_Workbook.xlsx")
    a = ap.parse_args()
    path = build(a.out)
    ok = False if a.no_recalc else recalc(path)
    print("built", path, "| recalculated" if ok else "| not recalculated")
    if a.install:
        shutil.copy(path, WORKBOOK); print("installed ->", WORKBOOK)
