# Systematic Macro Quant Investment Framework

Macro-aware ETF trend-following and risk-management research framework focused on tradable signal
generation, pullback-based execution refinement, staged position management, and dashboard visualization.

Macro Environment Filter
→ Trend / Flow Selection
→ Dashboard Relative Strength
→ Pullback Continuation Entry
→ Position & Risk Management
→ Analytics
→ Dashboard Visualization

---

# Project Overview

The framework focuses on tradable ETF trend-following, pullback refinement, and risk-management workflows using macro-aware market filters and dashboard-based relative-strength monitoring.

- Quantitative research
- ETF allocation analysis
- Execution timing analysis
- Risk management
- Performance analytics
- Power BI visualization
- AWS-supported research infrastructure

The framework combines macro-aware market filters, relative-strength monitoring, pullback refinement, and staged risk-management workflows into a tradable ETF execution framework.
The framework is primarily designed around US equity and growth-asset interpretation rather than traditional global macro forecasting. Macro signals are interpreted through liquidity, rates, USD flows, volatility, and growth leadership dynamics to support ETF allocation and execution decisions.

---

# Core Investment Workflow

Macro Environment Filter
→ Trend / Flow Selection
→ Dashboard Relative Strength
→ Pullback Continuation Entry
→ Position & Risk Management
→ Analytics
→ Dashboard Visualization

---

# Current Development

## Data Layer

- Automated ETF and macro data download pipeline using Python and yfinance
- Historical market data storage in structured CSV format
- Cross-asset monitoring universe integration
- Structured market-data workflows supporting dashboard visualization and execution research

## Research Framework

Includes monitoring systems across:

### Growth

- QQQ
- TQQQ

### AI-Core

- SOXL
- SOXX
- SMH

### Risk-off

- SQQQ
- TLT
- UUP
- VIX

### Commodity & Inflation

- BNO
- GLD
- DBC
- USO

### AI-Broad & Infrastructure

- XLK
- XLI
- IGV
- EQIX
- DLR
- PAVE

### Mega-Cap Technology

- AAPL
- MSFT
- AMZN
- GOOGL
- META
- TSLA

---

# CTA Core Philosophy

The framework follows a macro-aware CTA-style workflow:

- Identify the strongest tradable trend / flow
- Confirm continuation conditions
- Execute staged deployment
- Protect capital through systematic risk management

The system prioritizes:

- trend continuation
- pullback refinement
- staged exposure management
- risk-adjusted execution

rather than bottom prediction or full-market interpretation.

# System Features

## Macro Environment Filter

- Provides broad regime and trade-bias context
- Supports four simplified macro environments:
  - Panic Risk-off
  - Inflation Risk-off
  - Liquidity Tightening
  - Liquidity Risk-on
- Does not directly determine the final tradable asset

## Dashboard & Allocation Layer

- Relative-strength comparison
- Strongest-asset selection
- Capital-restriction execution scenarios
- Dashboard-based deployment preference
- Commodity / hedge / growth leadership comparison

## Execution Framework

- Breakout execution logic
- Pullback execution logic
- Pullback-quality scoring
- Execution-condition scoring and staged deployment analysis
- Options inputs are treated as optional execution confirmation, not as a core regime driver
- Trade structure confirmation workflows
- Adaptive execution-condition evaluation

## Position Management

- Staged exposure management
- Incremental scaling workflows
- Breakeven conversion logic
- Early-protection overlays
- Adaptive trailing frameworks
- Drawdown-control methodologies
- Volatility-aware exposure management

## Analytics & Validation

- Basic backtesting workflows
- Drawdown and volatility analytics
- Sharpe-ratio evaluation
- Recovery-factor monitoring
- Structured trade logging
- Ongoing Python research migration

---

# Technology Stack

## Programming & Analytics

- Python
- pandas
- NumPy
- SQL

## Visualization

- Power BI
- Excel
- Google Sheets

## Infrastructure

- AWS EC2
- GitHub

---

# Current Status

Currently converting Excel-based macro-aware allocation and execution systems into scalable Python research infrastructure and Power BI analytical dashboards.

Current development priorities include:

- Python migration of the CTA-style trend / flow selection engine
- Pullback continuation-entry logic
- Position and risk-management logic
- Dashboard visualization for relative strength and capital-restriction scenarios
- Basic backtesting and risk analytics

---

# Current migration focuses on:

- Macro environment filtering
- Dashboard export architecture
- Pullback continuation-entry logic
- Position-state management
- Risk-management automation
- Power BI visualization

---

# Repository Structure

```text
data/
scripts/
macro/
allocation/
execution/
risk_management/
dashboard_export/
analytics/
powerbi/
docs/
```

| Folder            | Corresponding Logic                                               |
| ----------------- | ----------------------------------------------------------------- |
| macro/            | Macro environment filtering                                       |
| execution/        | CTA trend-following and pullback continuation entry               |
| risk_management/  | Position-state management and staged exposure control             |
| allocation/       | Dashboard-based strongest-asset and capital-restriction scenarios |
| dashboard_export/ | Python → Power BI export                                          |
| analytics/        | Backtesting and risk analytics                                    |
| powerbi/          | Dashboard visualization                                           |
| data/             | Historical market data                                            |
| scripts/          | Utility and data pipeline scripts                                 |
| docs/             | Architecture and workflow documentation                           |

The framework prioritizes tradable execution quality and risk control over full-market narrative interpretation.

Disclaimer

This repository is for research, educational, and demonstration purposes only and does not constitute investment advice.
