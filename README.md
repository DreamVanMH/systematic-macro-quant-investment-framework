# Systematic Macro Quant Investment Framework

Institutional-style US equity-focused macro liquidity and ETF allocation research framework integrating:

- Macro regime analysis
- Cross-asset monitoring
- ETF allocation modeling
- Execution logic
- Pullback scoring
- Position management
- Staged exposure management
- Risk analytics
- Institutional-style research workflow

---

# Project Overview

The framework combines macro, liquidity, volatility, rates, commodity, AI-chain, and cross-asset monitoring systems into a unified US equity-focused allocation and execution engine.

- Quantitative research
- ETF allocation analysis
- Regime-based portfolio modeling
- Execution timing analysis
- Risk management
- Performance analytics
- Power BI visualization
- AWS-based backtesting infrastructure

The framework combines macro, cross-asset, volatility, commodity, AI-chain, and risk-off monitoring systems into a unified allocation and execution engine.
The framework is primarily designed around US equity and growth-asset interpretation rather than traditional global macro forecasting. Macro signals are interpreted through liquidity, rates, USD flows, volatility, and growth leadership dynamics to support ETF allocation and execution decisions.

---

# Core Investment Workflow

Macro Signals
→ Liquidity Interpretation
→ US Equity Regime Classification
→ Trade Bias
→ Structure Analysis
→ Allocation Engine
→ Execution Timing
→ Position Management
→ Risk Analytics

---

# Current Development

## Data Layer

- Automated ETF and macro data download pipeline using Python and yfinance
- Historical market data storage in structured CSV format
- Cross-asset monitoring universe integration
- Structured research data architecture for scalable analytics workflows

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

# System Features

## Macro Regime Engine

- Risk-on / Risk-off classification
- Volatility monitoring
- Yield, liquidity, and USD-flow interpretation
- US equity-centered macro liquidity framework
- Inflation and commodity pressure analysis
- Cross-asset confirmation workflows
- Macro trade-bias generation

## Allocation Engine

- Diversified ETF allocation logic
- Capital-constrained single-asset selection logic
- Relative-strength comparison workflows
- Risk-overlay integration
- Regime-sensitive allocation adjustments

## Execution Framework

- Breakout execution logic
- Pullback execution logic
- Pullback-quality scoring
- Execution-quality scoring and staged deployment analysis
- Options-structure and volatility-overlay integration
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

## Research Validation

- Walk-forward testing workflows
- Out-of-sample validation methodologies
- Monte Carlo robustness analysis
- Risk-adjusted performance evaluation
- Recovery factor analysis
- Volatility and drawdown analytics
- Structured performance attribution workflows
- Parameter sensitivity analysis
- Research reproducibility and structured analytical outputs

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

Currently converting institutional-style Excel-based macro allocation and execution systems into scalable Python research infrastructure and Power BI analytical dashboards.

Current development priorities include:

- Python signal engine migration
- Allocation automation
- Research workflow modularization
- Backtesting infrastructure
- Dashboard export architecture
- Institutional-style analytics visualization

---

# Research Infrastructure Migration

The following institutional-style research components are currently implemented within the Excel and Google Sheets framework and are being progressively translated into modular Python infrastructure:

- Macro signal engine
- Allocation engine
- Execution engine
- Position-state transition engine
- Pullback-scoring engine
- Risk analytics module
- Monte Carlo simulation workflows
- Walk-forward optimization workflows
- Strategy comparison framework
- Parameter optimization engine
- Dashboard export architecture
- Power BI institutional dashboard
- AWS deployment workflows

---

# Repository Structure

```text
data/
scripts/
signals/
allocation/
execution/
analytics/
dashboard_export/
powerbi/
```

| Folder            | Corresponding Logic                      |
| ----------------- | ---------------------------------------- |
| macro/            | Macro Signals                            |
| regime/           | Regime Classification                    |
| trade_bias/       | Trade Bias                               |
| structure/        | Structure Analysis                       |
| allocation/       | Allocation                               |
| execution/        | Execution                                |
| risk_management/  | Risk Management                          |
| analytics/        | Walk-forward / Monte Carlo / Sharpe / DD |
| dashboard_export/ | Python → Power BI export                 |
| powerbi/          | Institutional dashboard                  |
| data/             | Historical data                          |
| scripts/          | Utility / pipeline scripts               |

Disclaimer

This repository is for research, educational, and demonstration purposes only and does not constitute investment advice.
