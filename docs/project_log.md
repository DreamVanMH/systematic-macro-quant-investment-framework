# Systematic Macro Quant Investment Framework

## Project Development Log

---

# 2026-05-09

## Completed Today

### Project Structure Initialization

- Built institutional-style project folder structure:
  - data/
  - scripts/
  - macro/
  - regime/
  - execution/
  - risk_management/
  - powerbi/
  - docs/
    ...

### CSV Data Pipeline

- Implemented CSV market data loader
- Successfully loaded:
  - VIX
  - TNX
  - UUP
  - BTC
  - GLD
  - QQQ
  - TQQQ
  - SQQQ
  - and other ETF datasets

### Data Cleaning Fix

- Fixed yfinance multi-row CSV header issue
- Added:
  ```python
  skiprows=[1,2]
  ```
  Macro Snapshot Engine

## Implemented:

- get_latest_close()
- get_daily_change_pct()
- generate_macro_snapshot()
- Successfully Generated
- Macro monitoring snapshot table
- Daily percentage changes
- Latest market close tracking

## Current System Status

### Completed Layers

- Data Layer
- Market Data Loader
- Basic Macro Snapshot Engine

### In Progress

- Macro Regime Engine

### Not Started Yet

- Allocation Engine
- Trade Bias Engine
- Execution Engine
- Pullback Scoring System
- Risk Management Engine
- Backtesting Framework
- Power BI Dashboard
- SQL Database Layer
- AWS Deployment
- Monte Carlo Testing
- Walk-Forward Validation
- GitHub Portfolio Cleanup

---

## Next Planned Step

### regime_engine.py

Goal:
Convert raw macro signals into market regimes.

Examples:

- Risk-on
- Risk-off
- Inflationary
- Defensive
- AI Expansion
- Commodity Rotation

Initial Logic:

- VIX thresholds
- QQQ momentum
- TNX direction
- DXY pressure
- Commodity confirmation

---

## Long-Term Roadmap

### Phase 1 — Core Framework

- Data Layer
- Macro Engine
- Regime Engine
- Allocation Logic

### Phase 2 — Execution System

- Pullback logic
- Breakout logic
- Position management
- Trailing system

### Phase 3 — Quant Validation

- Python backtesting
- Walk-forward testing
- Monte Carlo simulation
- Parameter optimization

### Phase 4 — Institutional Packaging

- Power BI dashboard
- GitHub portfolio
- AWS deployment
- Strategy presentation deck
