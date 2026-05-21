"""
Run daily allocation snapshot.

This script generates today's allocation snapshot using:
- latest processed market data
- macro regime snapshot
- market-structure group summary
- allocation category score logic
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.load_all_data import load_all_market_data
from macro.macro_signal_engine import generate_macro_snapshot
from dashboard.market_structure import (
    build_market_structure_rows,
    run_market_structure,
)
from allocation.allocation_engine import (
    build_category_scores,
    run_allocation,
)


def print_allocation_snapshot(snapshot, category_scores, market_structure=None):
    """
    Print allocation snapshot in a readable format.
    """

    print("==============================")
    print("Allocation Snapshot")
    print("==============================")
    print()

    print(f"Macro Regime    : {snapshot.get('macro_regime')}")

    if market_structure:
        print(f"Market Structure: {market_structure}")

    print(f"VIX Level       : {snapshot.get('vix_level'):.2f}")
    print(f"Macro Cap       : {snapshot.get('macro_cap'):.0%}")
    print(f"SQQQ Allowed    : {snapshot.get('sqqq_allowed')}")
    print()

    print("Category Scores:")
    for category, score in category_scores.items():
        print(f"- {category}: {score}")

    print()
    print("Eligible Scores:")
    for category, score in snapshot.get("eligible_scores", {}).items():
        print(f"- {category}: {score}")

    print()
    print("Categories Allocation Suggestion:")
    for category, weight in snapshot.get("allocation", {}).items():
        print(f"- {category}: {weight:.2%}")


def main():
    """
    Generate allocation snapshot from latest available data.
    """

    market_data = load_all_market_data(
    source="processed",
    rebuild_if_missing=True,
    verbose=False,
)

    macro_snapshot = generate_macro_snapshot(market_data)
    macro_summary = macro_snapshot["summary"]

    macro_regime = macro_summary["Macro Regime"].iloc[0]

    vix_level = None
    if "VIX" in market_data and not market_data["VIX"].empty:
        vix_level = float(market_data["VIX"]["Close"].iloc[-1])

    asset_rows, missing_symbols = build_market_structure_rows(market_data)

    market_snapshot = run_market_structure(
        asset_rows=asset_rows,
        vix_level=vix_level,
    )

    group_summary = market_snapshot.get("group_summary", {})
    market_structure = market_snapshot.get("market_structure")

    category_scores = build_category_scores(group_summary)

    allocation_snapshot = run_allocation(
        category_scores=category_scores,
        macro_regime=macro_regime,
        vix_level=vix_level,
    )

    print_allocation_snapshot(
        snapshot=allocation_snapshot,
        category_scores=category_scores,
        market_structure=market_structure,
    )

    if missing_symbols:
        print()
        print(f"Missing Symbols: {len(missing_symbols)}")


if __name__ == "__main__":
    main()