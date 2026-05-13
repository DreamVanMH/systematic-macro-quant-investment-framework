import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")


FRED_SERIES = {
    "US02Y": "DGS2",
}


def download_fred_series(series_id: str, output_name: str):
    """
    Download one FRED time series as CSV.

    Example:
    DGS2 = 2-Year Treasury Constant Maturity Rate
    """

    DATA_DIR.mkdir(exist_ok=True)

    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"

    df = pd.read_csv(url)

    df.columns = ["Date", "Close"]

    df["Date"] = pd.to_datetime(df["Date"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna(subset=["Close"])

    output_path = DATA_DIR / f"{output_name}.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved {output_name} from FRED series {series_id} to {output_path}")


if __name__ == "__main__":
    for output_name, series_id in FRED_SERIES.items():
        download_fred_series(series_id, output_name)