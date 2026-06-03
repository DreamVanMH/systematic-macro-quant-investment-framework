import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


FRED_SERIES = {
    "US02Y": "DGS2",
}


load_dotenv(PROJECT_ROOT / ".env")

FRED_API_KEY = os.getenv("FRED_API_KEY")

if not FRED_API_KEY:
    raise ValueError(
        "FRED_API_KEY not found. Please add FRED_API_KEY=your_key to the .env file."
    )


def download_fred_series(series_id: str, output_name: str, max_retries: int = 3, wait_seconds: int = 5):
    """
    Download one FRED time series using official FRED API.

    Example:
    DGS2 = 2-Year Treasury Constant Maturity Rate

    Output format must stay compatible with load_all_data.py:
    Date, Close
    """

    DATA_DIR.mkdir(exist_ok=True)

    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
    }

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Downloading {output_name} from FRED series {series_id}... attempt {attempt}/{max_retries}")

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if "observations" not in data:
                raise ValueError(f"No observations returned for {series_id}. Response: {data}")

            df = pd.DataFrame(data["observations"])

            if df.empty:
                raise ValueError(f"Empty data returned for {series_id}")

            df = df[["date", "value"]].copy()

            df = df.rename(
                columns={
                    "date": "Date",
                    "value": "Close",
                }
            )

            df["Date"] = pd.to_datetime(df["Date"])
            df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

            df = df.dropna(subset=["Close"])
            df = df.sort_values("Date").reset_index(drop=True)

            output_path = DATA_DIR / f"{output_name}.csv"
            df.to_csv(output_path, index=False)

            print(f"Saved {output_name} from FRED series {series_id} to {output_path}")
            return True

        except requests.exceptions.Timeout:
            print(f"Timeout while downloading {series_id}")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error while downloading {series_id}: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Network error while downloading {series_id}: {e}")

        except Exception as e:
            print(f"Unexpected error while downloading {series_id}: {e}")
            return False

        if attempt < max_retries:
            print(f"Waiting {wait_seconds} seconds before retry...")
            time.sleep(wait_seconds)

    print(f"Failed after {max_retries} attempts: {series_id}")
    return False


if __name__ == "__main__":
    failed_series = []

    for output_name, series_id in FRED_SERIES.items():
        success = download_fred_series(series_id, output_name)

        if not success:
            failed_series.append(output_name)

        time.sleep(1)

    if failed_series:
        print("\nSome FRED series failed:")
        for item in failed_series:
            print(f"- {item}")
    else:
        print("\nAll FRED series downloaded successfully.")