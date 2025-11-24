import mplfinance as mpf
import yfinance as yf
import pandas as pd
import numpy as np

# === CHANGE THESE ===
ticker   = "AAPL"        # works with BTC-USD, SPY, etc.
period   = "1y"
interval = "1d"

# Download
df = yf.download(ticker, period=period, interval=interval, progress=False)

# === BULLETPROOF CLEANING (this fixes the error forever) ===
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]   # drop Adj Close
df = df.replace([np.inf, -np.inf], np.nan)            # remove infinity
df = df.dropna()                                      # drop bad rows
df = df.astype(float)                                 # FORCE all to float

# Bravos style – transparent background
my_style = mpf.make_mpf_style(
    base_mpl_style="seaborn-v0_8-darkgrid",
    marketcolors=mpf.make_marketcolors(up="#00ff00", down="#ff0000",
                                       edge="black", wick="white"),
    gridstyle="--",
    gridcolor="#404040",
    rc={"figure.facecolor": "none",
        "axes.facecolor":   "none",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white"}
)

# EMAs
ema20  = df['Close'].ewm(span=20,  adjust=False).mean()
ema50  = df['Close'].ewm(span=50,  adjust=False).mean()
ema200 = df['Close'].ewm(span=200, adjust=False).mean()

add_plots = [
    mpf.make_addplot(ema20,  color="#00ffff", width=2),
    mpf.make_addplot(ema50,  color="#ffa500", width=2),
    mpf.make_addplot(ema200, color="#ff00ff", width=2),
]

# Save the PNG
mpf.plot(df,
         type="candle",
         style=my_style,
         addplot=add_plots,
         volume=True,
         figsize=(19.2, 10.8),
         savefig=dict(fname="bravos_chart.png", dpi=400, transparent=True, bbox_inches="tight")
)

print("SUCCESS! bravos_chart.png created – perfect for DaVinci Resolve")