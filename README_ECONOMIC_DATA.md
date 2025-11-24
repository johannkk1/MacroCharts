# Setup Instructions for Real Economic Data

To enable real-time economic data from official sources, you need to set up a free FRED API key:

## 1. Get a FRED API Key (Free)

1. Visit: https://fred.stlouisfed.org/docs/api/api_key.html
2. Click "Request API Key"
3. Create a free account
4. Copy your API key

## 2. Set Environment Variable

### macOS/Linux:
```bash
export FRED_API_KEY="your_api_key_here"
```

### Or add to your shell profile (~/.zshrc or ~/.bashrc):
```bash
echo 'export FRED_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Windows:
```cmd
set FRED_API_KEY=your_api_key_here
```

## 3. Restart the Flask App

```bash
# Stop the current app (Ctrl+C)
# Then restart:
python3 app.py
```

## Data Sources

With the FRED API key, the app fetches:
- **Jobless Claims** (ICSA): Weekly initial unemployment claims
- **CPI** (CPIAUCSL): Consumer Price Index for inflation
- **PMI** (NAPM): ISM Manufacturing PMI
- **Fed Funds Rate** (DFF): Federal Funds Effective Rate

All data is cached for 5 minutes to minimize API calls.

## Without API Key

The app works without an API key by using realistic fallback data. The economic panel will still display and update, but with mock values instead of live data.
