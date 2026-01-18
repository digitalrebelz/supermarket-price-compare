# Error Log

## Common Issues and Solutions

### Scraping Errors
- **CloudFlare protection**: Use stealth mode, rotate user agents
- **Rate limiting**: Increase delay between requests
- **Selector changes**: Update CSS selectors in constants.py

### Database Errors
- **Locked database**: Ensure single writer, use WAL mode
- **Migration issues**: Run `alembic upgrade head`

### UI Errors
- **Session state lost**: Use st.session_state properly
- **Port in use**: Run `make clean` to kill existing processes
