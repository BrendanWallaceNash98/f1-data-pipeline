.PHONY: setup test run

VENV = venv/bin

setup:
	python3 -m venv venv && \
	source venv/bin/activate && \
	$(VENV)/pip install e . && \
	$(VENV)/pip install -r requirements.txt && \
	./make_env_file.sh

dev_run:
	$(VENV)/dagster dev -f orchestration/definitions.py

pipeline_run:
	$(VENV)/python3 orchestration/run_job.py

run_tests:
	$(VENV)/python3 tests/sql/test_sql_scripts.py
	$(VENV)/pytest tests/unit/ -v