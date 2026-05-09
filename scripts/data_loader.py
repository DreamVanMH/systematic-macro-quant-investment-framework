import yfinance as yf
import pandas as pd
import os

tickers = [

    # Growth
    "QQQ",
    "TQQQ",

    # AI-Core
    "SOXL",
    "SOXX",
    "SMH",

    # Risk-off / Hedge
    "SQQQ",
    "TLT",
    "UUP",
    "SHY",

    # Commodity
    "BNO",
    "DBC",
    "GLD",
    "USO",

    # Sector / AI-Broad
    "XLE",
    "XLF",
    "XLK",
    "XLU",
    "XLI",
    "PAVE",
    "EQIX",
    "DLR",
    "IGV",

    # Mega 7
    "AAPL",
    "MSFT",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",

    # Macro Monitoring
    "^VIX",
    "^TNX",
    "BTC-USD",
    "USDCNY=X",
    "CAD=X"
]

output_folder = "../data"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for ticker in tickers:

    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        start="2015-01-01",
        auto_adjust=True
    )

    filename = ticker.replace("^", "") + ".csv"

    df.to_csv(f"{output_folder}/{filename}")

    print(f"Saved: {filename}")

print("All ETF data downloaded successfully.")