import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.load_all_data import load_all_market_data
from macro.macro_signal_engine import generate_macro_snapshot


if __name__ == "__main__":
    market_data = load_all_market_data()

    macro_snapshot = generate_macro_snapshot(market_data)

    print("\n=== MACRO SIGNAL SNAPSHOT ===\n")
    print(macro_snapshot)