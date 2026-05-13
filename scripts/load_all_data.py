import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data"


def load_csv_file(file_path):
    """
    Load one CSV file into a pandas DataFrame.

    Yahoo Finance CSV files and FRED CSV files use different structures.
    - Yahoo files use extra header rows, so skiprows=[1, 2] is needed.
    - FRED US02Y file already uses a simple Date,Close structure.
    """

    ticker = file_path.stem

    if ticker == "US02Y":
        df = pd.read_csv(file_path)

        df["Date"] = pd.to_datetime(df["Date"])
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

        df = df.dropna(subset=["Close"])

        return df

    df = pd.read_csv(file_path, skiprows=[1, 2])

    return df


def load_all_market_data():
    """
    Load all CSV files from the data folder.
    """

    market_data = {}

    csv_files = DATA_PATH.glob("*.csv")

    for file_path in csv_files:
        ticker = file_path.stem

        df = load_csv_file(file_path)

        market_data[ticker] = df

        print(f"Loaded: {ticker}")

    return market_data


if __name__ == "__main__":
    data = load_all_market_data()

    print("\nTotal files loaded:", len(data))