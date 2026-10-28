"""Build the capstone report: report/output/CP45_Executive_Capstone_Report.docx (+ .pdf if LibreOffice and poppler are installed).

Inputs: data/derived/*.json, figures/*.png, src/palm_oil_traceability_model.py and notebooks/*.ipynb (Appendix B).
    python scripts/build_report.py            # DOCX + PDF
    python scripts/build_report.py --no-pdf   # DOCX only
"""
import sys
from _bootstrap import ROOT
import build_docx as report_build   # report/builder/build_docx.py (path added by _bootstrap)

if __name__ == "__main__":
    report_build.main(sys.argv[1:])
