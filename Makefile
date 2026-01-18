.PHONY: install test lint format run scrape clean test-cov

PYTHON := python3
VENV := venv
SRC := src
TESTS := tests

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	$(VENV)/bin/pip install -r requirements-dev.txt
	$(VENV)/bin/playwright install chromium

test:
	$(VENV)/bin/pytest $(TESTS) -v --tb=short

test-cov:
	$(VENV)/bin/pytest $(TESTS) -v --cov=$(SRC) --cov-report=html

lint:
	$(VENV)/bin/ruff check $(SRC) $(TESTS)
	$(VENV)/bin/mypy $(SRC)

format:
	$(VENV)/bin/black $(SRC) $(TESTS)
	$(VENV)/bin/isort $(SRC) $(TESTS)

run:
	$(VENV)/bin/streamlit run $(SRC)/ui/streamlit_app.py

scrape:
	$(VENV)/bin/python -m src.services.scraper_service

clean:
	pkill -f "streamlit run" 2>/dev/null || true
	rm -rf __pycache__ .pytest_cache .mypy_cache htmlcov .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
