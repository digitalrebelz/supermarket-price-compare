#!/bin/bash
# Run all scrapers to update prices

set -e

echo "Running scrapers..."

# Activate virtual environment
source venv/bin/activate

# Run scraper service
python -m src.services.scraper_service

echo "Scraping complete!"
