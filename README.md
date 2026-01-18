# Supermarket Price Compare

Een slimme boodschappen-prijsvergelijker die automatisch de websites van Nederlandse supermarkten afstruint om de voordeligste winkeloptie te vinden.

## Features

- **Multi-supermarket vergelijking**: Albert Heijn, Jumbo, Dirk, Plus, Flink, Picnic
- **Slimme prijsvergelijking**: Inclusief bezorgkosten, ophaalkosten en bonuskaart acties
- **Product matching**: Automatische matching van vergelijkbare producten
- **Boodschappenlijst**: Sla je favoriete producten op
- **Live prijzen**: Periodieke updates via scrapers

## Installatie

```bash
# Clone repository
git clone https://github.com/yourusername/supermarket-price-compare.git
cd supermarket-price-compare

# Installeer dependencies
make install

# Start de applicatie
make run
```

## Gebruik

1. Open de Streamlit UI op http://localhost:8501
2. Zoek naar producten in de zoekbalk
3. Voeg producten toe aan je boodschappenlijst
4. Bekijk de prijsvergelijking met totaalkosten

## Development

```bash
# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run scrapers manually
make scrape
```

## Supermarkten

| Supermarkt | Bezorging | Gratis vanaf | Ophalen | Bonuskaart |
|------------|-----------|--------------|---------|------------|
| Albert Heijn | €5.95 | - | Ja | Bonuskaart |
| Jumbo | €7.95 | €75 | Ja | Extra's |
| Dirk | €5.95 | - | Ja | - |
| Plus | €6.95 | - | Ja | Plus-punten |
| Flink | €2.99 | - | Nee | - |
| Picnic | €0 | €35 | Nee | - |

## License

MIT License
