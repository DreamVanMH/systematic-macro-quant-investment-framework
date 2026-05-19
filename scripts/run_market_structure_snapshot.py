"""
Run market structure snapshot.

This public runner loads standardized market data and generates
a market-structure snapshot using private group mapping and rules.

This script intentionally prints only group-level summary.
It does not print the full private asset universe.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.load_all_data import load_all_market_data
from dashboard.market_structure import (
    build_market_structure_rows,
    run_market_structure,
)

def get_latest_vix_level(market_data):
    """
    Get latest VIX level from standardized market_data.
    """

    if "VIX" not in market_data:
        return None

    df = market_data["VIX"]

    if df.empty or "Close" not in df.columns:
        return None

    latest_vix = df["Close"].iloc[-1]

    try:
        return float(latest_vix)
    except (TypeError, ValueError):
        return None


def print_snapshot(snapshot, missing_count=0):
    print("\n==============================")
    print("Market Structure Snapshot")
    print("==============================")

    print(f"\nMarket Structure: {snapshot.get('market_structure')}")
    vix_level = snapshot.get("vix_level")

    if vix_level is not None:
        print(f"VIX Level       : {vix_level:.2f}")
    else:
        print("VIX Level       : N/A")

    print("\nGroup Summary:")
    for group, summary in snapshot.get("group_summary", {}).items():
        print(
            f"- {group}: "
            f"Green={summary.get('green_count')}, "
            f"Red={summary.get('red_count')}, "
            f"Bias={summary.get('bias')}"
        )

    if missing_count > 0:
        print(f"\nMissing symbols: {missing_count}")
        print("Note: Missing symbol details are hidden in the public runner.")


def main():
    market_data = load_all_market_data()

    vix_level = get_latest_vix_level(market_data)

    asset_rows, missing_symbols = build_market_structure_rows(market_data)

    snapshot = run_market_structure(
        asset_rows=asset_rows,
        vix_level=vix_level,
    )

    print_snapshot(snapshot, missing_count=len(missing_symbols))


if __name__ == "__main__":
    main()