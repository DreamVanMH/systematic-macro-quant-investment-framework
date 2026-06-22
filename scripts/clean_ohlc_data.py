from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data"
OHLC_DATA_DIR = PROJECT_ROOT / "ohlc_data"

REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]
CLOSE_ONLY_COLUMNS = ["Date", "Close"]


def read_raw_or_standard_ohlc(csv_path: Path) -> pd.DataFrame | None:
    """
    Read either:

    1. yfinance multi-header CSV:
       Price,Close,High,Low,Open,Volume
       Ticker,SOXL,SOXL,SOXL,SOXL,SOXL
       Date,,,,,
       2015-01-02,...

    2. Standard OHLC CSV:
       Date,Open,High,Low,Close,Volume
       2015-01-02,...

    3. Close-only macro/Fed CSV:
       Date,Close
       1976-06-01,7.26

       This should be skipped because it is not OHLC data.
    """

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    lines = csv_path.read_text(encoding="utf-8").splitlines()

    if not lines:
        raise ValueError("Empty CSV file.")

    first_line = lines[0]

    if first_line.startswith("Price,"):
        raw_df = pd.read_csv(csv_path, skiprows=3, header=None)

        if raw_df.shape[1] < 6:
            raise ValueError(
                f"Expected at least 6 columns for yfinance OHLC data, got {raw_df.shape[1]}"
            )

        # Keep up to 7 columns because some yfinance files include:
        # Date, Adj Close, Close, High, Low, Open, Volume
        raw_df = raw_df.iloc[:, : min(raw_df.shape[1], 7)].copy()

        candidate_mappings = [
            {
                "name": "date_adjclose_close_high_low_open_volume",
                "columns": ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"],
                "rename": {
                    "Date": "Date",
                    "Open": "Open",
                    "High": "High",
                    "Low": "Low",
                    "Close": "Close",
                    "Volume": "Volume",
                },
            },
            {
                "name": "date_close_high_low_open_volume",
                "columns": ["Date", "Close", "High", "Low", "Open", "Volume"],
                "rename": {
                    "Date": "Date",
                    "Open": "Open",
                    "High": "High",
                    "Low": "Low",
                    "Close": "Close",
                    "Volume": "Volume",
                },
            },
            {
                "name": "date_open_high_low_close_volume",
                "columns": ["Date", "Open", "High", "Low", "Close", "Volume"],
                "rename": {
                    "Date": "Date",
                    "Open": "Open",
                    "High": "High",
                    "Low": "Low",
                    "Close": "Close",
                    "Volume": "Volume",
                },
            },
            {
                "name": "project_shifted_close_high_low_open_as_volume",
                "columns": ["Date", "Close", "High_or_Close", "High", "Low", "Open"],
                "rename": {
                    "Date": "Date",
                    "Open": "Open",
                    "High": "High",
                    "Low": "Low",
                    "Close": "Close",
                },
            },
        ]
        
        valid_candidates = []

        for mapping in candidate_mappings:
            if len(mapping["columns"]) != raw_df.shape[1]:
                continue

            candidate = raw_df.copy()
            candidate.columns = mapping["columns"]

            fixed = pd.DataFrame()
            fixed["Date"] = candidate["Date"]
            fixed["Open"] = candidate[mapping["rename"]["Open"]]
            fixed["High"] = candidate[mapping["rename"]["High"]]
            fixed["Low"] = candidate[mapping["rename"]["Low"]]
            fixed["Close"] = candidate[mapping["rename"]["Close"]]

            if "Volume" in mapping["rename"]:
                fixed["Volume"] = candidate[mapping["rename"]["Volume"]]
            else:
                fixed["Volume"] = None

            x = fixed.copy()
            for col in ["Open", "High", "Low", "Close"]:
                x[col] = pd.to_numeric(x[col], errors="coerce")

            invalid = x[
                (x["High"] < x["Low"])
                | (x["High"] < x["Open"])
                | (x["High"] < x["Close"])
                | (x["Low"] > x["Open"])
                | (x["Low"] > x["Close"])
            ]

            valid_candidates.append(
                {
                    "name": mapping["name"],
                    "df": fixed,
                    "invalid_rows": len(invalid),
                }
            )

        if not valid_candidates:
            raise ValueError(
                f"No compatible yfinance mapping found for {csv_path.name} with {raw_df.shape[1]} columns."
            )

        best = min(valid_candidates, key=lambda item: item["invalid_rows"])

        if best["invalid_rows"] > 0:
            print(
                f"[WARN] {csv_path.name}: best yfinance mapping "
                f"{best['name']} still has {best['invalid_rows']} invalid OHLC rows."
            )
        else:
            print(f"[OK] {csv_path.name}: using yfinance mapping {best['name']}")

        return best["df"]

    df = pd.read_csv(csv_path)

    columns = list(df.columns)

    if columns == CLOSE_ONLY_COLUMNS:
        print("[SKIP] Close-only macro/Fed data detected: Date,Close")
        return None

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required OHLC columns: {missing}."
        )

    return df


def clean_ohlc_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize date and numeric columns for OHLC replay.

    Final output:
    Date, Open, High, Low, Close, Volume

    Also repairs small OHLC inconsistencies by recalculating:
    High = max(Open, High, Low, Close)
    Low  = min(Open, High, Low, Close)

    This is used only after the best column mapping has already been selected.
    """

    df = df.copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    for col in ["Open", "High", "Low", "Close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Volume" not in df.columns:
        df["Volume"] = None
    else:
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")

    df = df.dropna(subset=["Date", "Open", "High", "Low", "Close"])

    # Repair small row-level OHLC inconsistencies after mapping selection.
    price_cols = ["Open", "High", "Low", "Close"]
    df["High"] = df[price_cols].max(axis=1)
    df["Low"] = df[price_cols].min(axis=1)

    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    return df[REQUIRED_COLUMNS]


def clean_one_file(raw_csv_path: Path) -> str:
    """
    Clean one raw CSV from data/ into ohlc_data/.

    Returns:
        "success"
        "skipped"
        "failed"
    """

    asset = raw_csv_path.stem.upper()
    output_path = OHLC_DATA_DIR / f"{asset}.csv"

    print(f"\nProcessing {asset}")
    print(f"Raw:  {raw_csv_path}")
    print(f"OHLC: {output_path}")

    try:
        raw_df = read_raw_or_standard_ohlc(raw_csv_path)

        if raw_df is None:
            return "skipped"

        clean_df = clean_ohlc_dataframe(raw_df)

        if clean_df.empty:
            raise ValueError("Cleaned dataframe is empty.")

        OHLC_DATA_DIR.mkdir(parents=True, exist_ok=True)
        clean_df.to_csv(output_path, index=False)

        print(f"[OK] {asset}: saved {len(clean_df)} rows.")
        return "success"

    except Exception as exc:
        print(f"[FAILED] {asset}: {exc}")
        return "failed"


def main() -> int:
    print("============================================")
    print("Batch Clean OHLC Data")
    print("============================================")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Raw data dir: {RAW_DATA_DIR}")
    print(f"OHLC data dir: {OHLC_DATA_DIR}")

    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(f"Raw data directory not found: {RAW_DATA_DIR}")

    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("\n[WARNING] No CSV files found in data/.")
        return 0

    success = []
    skipped = []
    failed = []

    for csv_path in csv_files:
        result = clean_one_file(csv_path)
        asset = csv_path.stem.upper()

        if result == "success":
            success.append(asset)
        elif result == "skipped":
            skipped.append(asset)
        else:
            failed.append(asset)

    print("\n============================================")
    print("Batch Clean Summary")
    print("============================================")
    print(f"Success: {len(success)}")
    print(f"Skipped: {len(skipped)}")
    print(f"Failed:  {len(failed)}")

    if success:
        print("\nSuccess assets:")
        print(success)

    if skipped:
        print("\nSkipped non-OHLC assets:")
        print(skipped)

    if failed:
        print("\nFailed assets:")
        print(failed)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())