# CLAUDE.md - Supermarket Price Compare

## Project Context
Boodschappen prijsvergelijker voor Nederlandse supermarkten.
Scrapet prijzen, vergelijkt totaalkosten inclusief bezorging.

## Coding Standards
- Type hints voor alle functies
- Google style docstrings
- Max 100 regels per bestand
- Async voor alle scraping operaties

## Commando's
- `make install` - Installeer dependencies + playwright browsers
- `make test` - Run alle tests
- `make scrape` - Run alle scrapers
- `make run` - Start Streamlit UI

## Supermarkt Specifics
- Albert Heijn: Bonus kaart acties, bezorging vanaf €0
- Jumbo: Extra's voordeel, gratis bezorging vanaf €75
- Dirk: Dirk prijzen altijd laag
- Plus: Route 99 acties
- Flink: Alleen bezorging, snelle delivery
- Picnic: Alleen bezorging, gratis vanaf €35

## Anti-Scraping Maatregelen
- Respecteer robots.txt
- Rate limiting: max 1 request per 2 seconden
- Random delays tussen requests
- Rotate user agents
- Gebruik headless browser alleen waar nodig

## Architecture
```
src/
├── config/         # Settings and constants
├── models/         # Pydantic models
├── scrapers/       # Supermarket scrapers
├── services/       # Business logic
├── database/       # SQLAlchemy models + CRUD
├── api/            # FastAPI routes
└── ui/             # Streamlit app
```

## Testing
- Unit tests: `pytest tests/unit -v`
- Integration tests: `pytest tests/integration -v`
- E2E tests: `pytest tests/e2e -v`
- All tests: `make test`

## Database
SQLite database at `data/supermarket.db`
- Supermarket: Store info + delivery costs
- Product: Product details
- PriceRecord: Price history per product per store
- FavoriteProduct: User's saved products
- ShoppingList: User's shopping lists
