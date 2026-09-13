PYTHON := .venv/bin/python
DBT := .venv/bin/dbt

.PHONY: setup sample-data load dbt-run narrate dry-run demo clean

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -q --upgrade pip
	$(PYTHON) -m pip install -q -r requirements.txt

sample-data:
	$(PYTHON) scripts/generate_sample_data.py

load:
	$(PYTHON) scripts/load_raw.py

dbt-run:
	cd dbt_project && DBT_PROFILES_DIR=. ../$(DBT) run

narrate:
	$(PYTHON) scripts/narrate.py --all

dry-run:
	$(PYTHON) scripts/narrate.py --all --dry-run

# Full pipeline against the bundled synthetic sample data -- no API key
# needed, prints the computed metrics for every week instead of calling Claude.
demo: sample-data load dbt-run dry-run

clean:
	rm -rf warehouse/*.duckdb dbt_project/target dbt_project/logs output/*.md
