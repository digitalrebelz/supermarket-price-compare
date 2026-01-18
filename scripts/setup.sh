#!/bin/bash
# Setup script for Supermarket Price Compare

set -e

echo "Setting up Supermarket Price Compare..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Create data directory
mkdir -p data logs

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

# Seed database
echo "Seeding database..."
python scripts/seed_data.py

echo ""
echo "Setup complete!"
echo ""
echo "To start the application:"
echo "  source venv/bin/activate"
echo "  make run"
