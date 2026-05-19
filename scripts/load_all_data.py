import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data"
PROCESSED_DATA_PATH = PROJECT_ROOT / "processed_data"


def add_change_pct(df):
    """
    Add daily percentage change based on Close price.

    Output columns:
    Date, Close, change_pct
    """

    df = df.copy()

    df["Date"] = pd.to_datetime(df["Date"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])
    df = df.sort_values("Date").reset_index(drop=True)

    df["change_pct"] = df["Close"].pct_change() * 100

    return df


def load_csv_file(file_path):
    """
    Load one raw CSV file and standardize it.

    Yahoo Finance CSV files and FRED CSV files use different structures.
    - Yahoo files use extra header rows, so skiprows=[1, 2] is needed.
    - FRED US02Y file already uses a simple Date,Close structure.

    Final output:
    Date, Close, change_pct
    """

    ticker = file_path.stem

    # FRED file: US02Y.csv
    if ticker == "US02Y":
        df = pd.read_csv(file_path)

        df["Date"] = pd.to_datetime(df["Date"])
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

        df = df[["Date", "Close"]].copy()
        df = add_change_pct(df)

        return df

    # Yahoo Finance files
    df = pd.read_csv(file_path, skiprows=[1, 2])

    # In your original yfinance format, after skiprows=[1, 2],
    # the first column may be named "Price", but it is actually Date.
    if "Date" not in df.columns:
        first_col = df.columns[0]
        df = df.rename(columns={first_col: "Date"})

    if "Close" not in df.columns:
        raise ValueError(
            f"{ticker}: missing Close column after loading raw CSV. "
            f"Current columns: {list(df.columns)}"
        )

    df = df[["Date", "Close"]].copy()
    df = add_change_pct(df)

    return df


def rebuild_processed_data():
    """
    Read raw CSV files from data/,
    standardize them,
    calculate change_pct,
    and save clean CSV files into processed_data/.
    """

    PROCESSED_DATA_PATH.mkdir(exist_ok=True)

    csv_files = sorted(RAW_DATA_PATH.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DATA_PATH}")

    processed_data = {}

    for file_path in csv_files:
        ticker = file_path.stem

        df = load_csv_file(file_path)

        output_path = PROCESSED_DATA_PATH / f"{ticker}.csv"
        df.to_csv(output_path, index=False)

        processed_data[ticker] = df

        print(f"Processed: {ticker} -> {output_path}")

    print("\nAll raw data files have been standardized successfully.")

    return processed_data


def load_processed_csv_file(file_path):
    """
    Load one standardized CSV file from processed_data/.
    """

    ticker = file_path.stem

    df = pd.read_csv(file_path)

    required_columns = {"Date", "Close", "change_pct"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{ticker}: missing columns in processed file: {missing_columns}"
        )

    df["Date"] = pd.to_datetime(df["Date"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df["change_pct"] = pd.to_numeric(df["change_pct"], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])
    df = df.sort_values("Date").reset_index(drop=True)

    return df


def load_all_market_data(source="processed", rebuild_if_missing=True, verbose=False):
    """
    Load all market data into a dictionary.

    source="processed":
        Load standardized CSV files from processed_data/.

    source="raw":
        Load raw files from data/ and standardize in memory.

    rebuild_if_missing=True:
        If processed_data/ does not exist or is empty,
        rebuild it from raw data automatically.
    """

    market_data = {}

    if source == "raw":
        csv_files = sorted(RAW_DATA_PATH.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError(f"No raw CSV files found in {RAW_DATA_PATH}")

        for file_path in csv_files:
            ticker = file_path.stem

            df = load_csv_file(file_path)

            market_data[ticker] = df

            if verbose:
                print(f"Loaded raw: {ticker}")

        return market_data

    if source == "processed":
        if rebuild_if_missing:
            if not PROCESSED_DATA_PATH.exists() or not list(PROCESSED_DATA_PATH.glob("*.csv")):
                print("processed_data/ is missing or empty. Rebuilding from raw data...")
                rebuild_processed_data()

        csv_files = sorted(PROCESSED_DATA_PATH.glob("*.csv"))

        if not csv_files:
            raise FileNotFoundError(
                f"No processed CSV files found in {PROCESSED_DATA_PATH}"
            )

        for file_path in csv_files:
            ticker = file_path.stem

            df = load_processed_csv_file(file_path)

            market_data[ticker] = df

            if verbose:
                print(f"Loaded processed: {ticker}")

        return market_data

    raise ValueError("source must be either 'raw' or 'processed'")


if __name__ == "__main__":
    rebuild_processed_data()

    data = load_all_market_data(source="processed")

    print("\nTotal files loaded:", len(data))
    print("Processed data rebuild completed successfully.")     