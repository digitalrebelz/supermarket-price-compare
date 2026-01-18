# Project Context

## Overview
Supermarket Price Compare is a Dutch grocery price comparison tool that scrapes prices from multiple supermarkets and helps users find the cheapest option for their shopping list.

## Target Supermarkets
1. Albert Heijn (ah.nl) - Largest Dutch supermarket
2. Jumbo (jumbo.com) - Second largest
3. Dirk (dirk.nl) - Budget-friendly
4. Plus (plus.nl) - Regional supermarket
5. Flink (goflink.com) - Quick delivery service
6. Picnic (picnic.app) - Online-only supermarket

## Key Features
- Search products across all supermarkets
- Match similar products automatically
- Calculate total cost including delivery/pickup
- Apply bonus card discounts
- Maintain shopping lists
- Track price history

## Technical Decisions
- SQLite for simplicity (no external DB needed)
- Playwright for JavaScript-heavy sites
- httpx for API-based supermarkets
- Streamlit for rapid UI development
- AsyncIO for concurrent scraping
