# FinSight AI Ultra Advanced Dashboard

Google Finance inspired stock market dashboard with fully functional demo UI.

## Features
- Google Finance style home page and stock detail page
- Search box with clickable results
- Watchlist add/remove
- Equity sector and market list navigation
- Region tabs: US, Europe, India, Currencies, Crypto, Futures
- Interactive chart: area/line/bar/candle buttons, compare, indicators, time ranges
- News cards, earnings, market movers, risk heatmap
- AI Research panel with questions, chat, deep search/watchlist analysis buttons
- Theme switch, settings, profile, alerts, sidebar collapse, research expand

## Run in VS Code
1. Extract ZIP
2. Open folder in VS Code
3. Open terminal
4. Install backend requirements:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run backend:
   ```powershell
   uvicorn api:app --reload
   ```
6. Open `index.html` with Live Server.

Backend is optional for the UI demo, but keep it running for project completeness.
