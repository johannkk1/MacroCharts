import yfinance as yf

ticker = "^GDAXI"
period = "5y"
interval = "1d"

print(f"Downloading {ticker} for {period} with {interval}...")
try:
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if df is None or df.empty:
        print("Data is empty or None")
    else:
        print(df.head())
        print(df.tail())
        print(f"Shape: {df.shape}")
except Exception as e:
    print(f"Error: {e}")
