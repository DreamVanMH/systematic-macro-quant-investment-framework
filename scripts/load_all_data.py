import pandas as pd
from pathlib import Path


DATA_PATH = Path("../data")


def load_csv_file(file_path):
    """
    Load one CSV file into a pandas DataFrame.
    """

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