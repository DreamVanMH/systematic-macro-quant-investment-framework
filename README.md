# Macro-Driven ETF Allocation, Timing & Position Management System (v0.2)

This repository converts the latest Excel/Google Sheets trading framework into a Python-ready project for backtesting, GitHub demonstration, Power BI visualization, and interview presentation.

## What changed in v0.2

- Added **Pullback Add Signal** logic from the V8 workbook.
- Added **Entry Type** support from the Master Position Tracker: `BREAKOUT` vs `PULLBACK`.
- Updated Power BI input files and demo deck structure to show both execution styles.

## System logic

The model follows a layered investment workflow:

1. **Macro Layer** — VIX, DXY/USD, yields, oil, gold, etc.
2. **Regime Layer** — Risk-on, Inflation risk-off, Risk-off, Mixed.
3. **Structure / Breadth Layer** — Growth, AI-Core, AI-Broad, Risk-off, Commodity, Sector groups.
4. **Allocation Layer** — diversified allocation or selected strongest asset + residual cash for small capital trading.
5. **Timing Layer** — options timing, breakout confirmation, pullback add permission.
6. **Position Layer** — staged entries, stop loss, breakeven, trailing reduction, drawdown monitoring, and entry type.

## Repository structure

```text
src/
  data_loader.py              # Load market data or exported Excel CSVs
  macro_regime.py             # Macro regime and trade bias mapping
  allocation_engine.py        # Multi-asset and single-asset allocation logic
  pullback_add_signal.py      # New V8 pullback add permission logic
  entry_type_engine.py        # New master Entry Type logic: BREAKOUT / PULLBACK
  position_manager.py         # Staged entry and risk-control rules
  backtest.py                 # Demo backtest skeleton
configs/
  *.csv / *.json              # Extracted configs from latest Excel files
powerbi/
  powerbi_model_notes.md      # Recommended Power BI table relationships and pages
docs/
  project_plan.md             # Development plan and interview demo notes
aws/
  deploy_notes.md             # AWS EC2 deployment outline
```

## Status

This is an actively developed interview demo. The Excel model remains the strategy source of truth; Python implementation is being built module by module to support reproducible backtesting and Power BI output.
