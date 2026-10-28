"""Rebuild everything from the model and the evidence workbook:

    1. compute_numbers   data/derived/nums.json            (all numbers the report quotes)
    2. compute_extras    data/derived/parity2.json, staged.json
    3. make_figures      figures/*.png                      (+ power.json, fine_rob.json, impact.json)
    4. build_notebook    notebooks/*.ipynb
    5. build_report      report/output/*.docx (+ .pdf if LibreOffice and poppler are installed)

    python scripts/run_all.py              # everything
    python scripts/run_all.py --no-report  # stop after the notebook
    python scripts/run_all.py --no-pdf     # DOCX only
"""
import argparse
import runpy
import sys
import time
from pathlib import Path
from _bootstrap import ROOT

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-report", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()
    here = Path(__file__).resolve().parent
    steps = [("compute_numbers.py", []), ("compute_extras.py", []), ("make_figures.py", []), ("build_notebook.py", [])]
    if not a.no_report:
        steps.append(("build_report.py", ["--no-pdf"] if a.no_pdf else []))
    for name, argv in steps:
        print(f"\n=== {name} ===", flush=True)
        t0 = time.time()
        sys.argv = [name] + argv
        runpy.run_path(str(here / name), run_name="__main__")
        print(f"--- {name} done in {time.time() - t0:.1f}s")
    print("\nAll steps finished. Outputs: data/derived/, figures/, notebooks/, report/output/")
