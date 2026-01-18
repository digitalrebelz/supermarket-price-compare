# Architecture Decisions

## ADR-001: Use Playwright for Scraping
**Context**: Supermarket websites use heavy JavaScript rendering
**Decision**: Use Playwright with Chromium for scraping
**Consequences**: Slower but more reliable scraping

## ADR-002: SQLite Database
**Context**: Need persistent storage for prices and products
**Decision**: Use SQLite with SQLAlchemy ORM
**Consequences**: Simple setup, no external dependencies, good for single-user

## ADR-003: Streamlit for UI
**Context**: Need a simple web interface quickly
**Decision**: Use Streamlit instead of custom frontend
**Consequences**: Rapid development, limited customization

## ADR-004: Fuzzy Product Matching
**Context**: Same products have different names across supermarkets
**Decision**: Use fuzzywuzzy for string similarity matching
**Consequences**: May have false positives, needs threshold tuning

## ADR-005: Rate Limiting
**Context**: Avoid being blocked by supermarket websites
**Decision**: 2 second delay between requests, random jitter
**Consequences**: Slower scraping but more reliable
