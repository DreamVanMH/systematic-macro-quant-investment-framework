import yfinance as yf
import pandas as pd
from pathlib import Path

tickers = [

    # Growth
    "QQQ",
    "TQQQ",
    "NQ=F",

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

PROJECT_ROOT = Path(__file__).resolve().parents[1]
output_folder = PROJECT_ROOT / "data"

output_folder.mkdir(exist_ok=True)

for ticker in tickers:

    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        start="2015-01-01",
        auto_adjust=True
    )

    filename_map = {
    "^VIX": "VIX",
    "^TNX": "TNX",
    "NQ=F": "NQ1",
    }

    output_name = filename_map.get(ticker, ticker.replace("^", ""))
    filename = output_name + ".csv"

    df.to_csv(output_folder / filename)

    print(f"Saved: {filename}")

print("All ETF data downloaded successfully.")