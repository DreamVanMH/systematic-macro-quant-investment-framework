import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.load_all_data import load_all_market_data
from macro.macro_signal_engine import generate_macro_snapshot

if __name__ == "__main__":
    market_data = load_all_market_data()
    macro_snapshot = generate_macro_snapshot(market_data)

    snapshot_df = macro_snapshot["snapshot"].copy()
    summary_df = macro_snapshot["summary"].copy()

    # format snapshot display
    snapshot_df["Latest Close"] = snapshot_df["Latest Close"].round(4)
    snapshot_df["Daily Change %"] = snapshot_df["Daily Change %"].round(4)

    print("\n=== MACRO ENVIRONMENT FILTER SNAPSHOT ===\n")
    print(snapshot_df.to_string(index=False))

    # format summary display
    summary_row = summary_df.iloc[0]

    print("\n=== MACRO SUMMARY ===\n")
    print(f"Macro Regime         : {summary_row['Macro Regime']}")
    print(f"Trade Bias           : {summary_row['Trade Bias']}")
    print(f"Risk-on Score        : {summary_row['risk_on_score']}")
    print(f"Risk-off Score       : {summary_row['risk_off_score']}")
    print(f"Inflation Score      : {summary_row['inflation_score']}")
    print(f"Rate Pressure Score  : {summary_row['rate_pressure_score']}")
    print(f"USD Liquidity Score  : {summary_row['usd_liquidity_score']}")