PY ?= python3

.PHONY: help install test all numbers figures notebook report report-docx workbook clean

help:
	@echo 'make install      pip install -r requirements.txt'
	@echo 'make test         run the 28 unit tests (~40 s)'
	@echo 'make all          rebuild numbers, figures, notebook, report (DOCX + PDF if LibreOffice/poppler present)'
	@echo 'make report-docx  same, DOCX only'
	@echo 'make workbook    rebuild the evidence workbook into build/ (needs LibreOffice to recalc)'
	@echo 'make clean        remove build/ and caches'

install:
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) -m unittest discover -s tests -v

all:
	$(PY) scripts/run_all.py

report-docx:
	$(PY) scripts/run_all.py --no-pdf

numbers:
	$(PY) scripts/compute_numbers.py && $(PY) scripts/compute_extras.py

figures:
	$(PY) scripts/make_figures.py

notebook:
	$(PY) scripts/build_notebook.py

report:
	$(PY) scripts/build_report.py

workbook:
	$(PY) scripts/build_workbook.py

clean:
	rm -rf build .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
