# FRED API Setup Guide

## Get Your Free FRED API Key

The Federal Reserve Economic Data (FRED) provides free access to official U.S. economic indicators.

### Step 1: Create a FRED Account
1. Go to https://fred.stlouisfed.org/
2. Click "My Account" → "API Keys"
3. Sign up for a free account (takes 1 minute)

### Step 2: Request an API Key
1. Once logged in, go to https://fred.stlouisfed.org/docs/api/api_key.html
2. Click "Request API Key"
3. Fill out the simple form (name, email, purpose: "Personal Project")
4. You'll receive your API key instantly

### Step 3: Set the API Key

#### For Local Development (Mac/Linux):
```bash
export FRED_API_KEY="your_api_key_here"
```

Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent:
```bash
echo 'export FRED_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

#### For Local Development (Windows):
```cmd
set FRED_API_KEY=your_api_key_here
```

#### For Production Deployment:
When deploying to Render/Railway/Fly.io, add `FRED_API_KEY` as an environment variable in the platform's dashboard.

### Step 4: Verify It Works
```bash
cd "/Users/johann/Desktop/MACRO CHARTS"
python3 -c "from economic_data import get_interest_rate; import json; print(json.dumps(get_interest_rate(), indent=2))"
```

You should see the current Fed Funds Rate (around 4.58% as of late 2024).

## What Data is Fetched?

With the FRED API key, you'll get live data for:
- **Jobless Claims** (ICSA) - Weekly initial unemployment claims
- **CPI** (CPIAUCSL) - Consumer Price Index, inflation rate
- **PMI** (NAPM) - ISM Manufacturing PMI
- **Fed Funds Rate** (DFF) - Federal Funds Effective Rate

## Without API Key

The app will work without an API key, but will show fallback/mock data instead of live economic indicators.
