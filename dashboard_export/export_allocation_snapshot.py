"""
Export allocation snapshot for Power BI.

This script generates a clean allocation snapshot table using:
- latest processed market data
- macro regime snapshot
- market-structure summary
- allocation category score logic

Output:
dashboard_export/output/allocation_snapshot.csv

Note:
This export only contains final snapshot results.
It does not expose private allocation parameters or rule thresholds.
"""

from pathlib import Path
import sys
import pandas as pd


# ============================================================
# 1. Project root setup
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# 2. Imports
# ============================================================

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


# ============================================================
# 3. Output path
# ============================================================

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "allocation_snapshot.csv"
HISTORY_FILE = OUTPUT_DIR / "allocation_snapshot_history.csv"


# ============================================================
# 4. Build allocation snapshot
# ============================================================

def build_allocation_export_rows():
    """
    Build allocation snapshot rows for dashboard export.

    Returns:
        pd.DataFrame: One row per allocation category.
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

    structure_snapshot = run_market_structure(
        asset_rows=asset_rows,
        vix_level=vix_level,
    )

    group_summary = structure_snapshot.get("group_summary", {})
    market_structure = structure_snapshot.get("market_structure")

    category_scores = build_category_scores(group_summary)

    allocation_result = run_allocation(
        category_scores=category_scores,
        macro_regime=macro_regime,
        vix_level=vix_level,
    )

    allocation = allocation_result["allocation"]
    eligible_scores = allocation_result["eligible_scores"]

    run_timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    
    export_rows = []

    for category, suggested_weight in allocation.items():
        export_rows.append(
            {
                "run_timestamp": run_timestamp,
                "date": pd.Timestamp.today().date(),
                "macro_regime": macro_regime,
                "market_structure": market_structure,
                "vix_level": round(vix_level, 2) if vix_level is not None else None,
                "macro_cap": allocation_result["macro_cap"],
                "sqqq_allowed": allocation_result["sqqq_allowed"],
                "category": category,
                "category_score": category_scores.get(category, 0),
                "eligible_score": eligible_scores.get(category, 0),
                "suggested_weight": suggested_weight,
                "missing_symbol_count": len(missing_symbols),
            }
        )

    return pd.DataFrame(export_rows)


# ============================================================
# 5. Export
# ============================================================

def export_allocation_snapshot():
    """
    Export allocation snapshot to CSV for Power BI.

    Outputs:
    1. allocation_snapshot.csv
       - latest snapshot only
       - overwritten each run

    2. allocation_snapshot_history.csv
       - historical snapshots
       - appended each run
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = build_allocation_export_rows()

    # Latest snapshot export
    df.to_csv(OUTPUT_FILE, index=False)

    # Historical snapshot export
    write_header = not HISTORY_FILE.exists()
    df.to_csv(
        HISTORY_FILE,
        mode="a",
        header=write_header,
        index=False,
    )

    print("Allocation snapshot exported successfully.")
    print(f"Latest output file : {OUTPUT_FILE}")
    print(f"History output file: {HISTORY_FILE}")


if __name__ == "__main__":
    export_allocation_snapshot()