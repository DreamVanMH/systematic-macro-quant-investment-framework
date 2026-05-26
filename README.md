# Systematic Macro Quant Investment Framework

A macro-aware ETF and selected-equity allocation, execution-monitoring, and risk-management research framework.

This project converts a spreadsheet-based investment decision-support workflow into a Python, CSV, and Power BI research infrastructure. The current Python MVP covers macro regime monitoring, market-structure classification, allocation scoring, latest-snapshot export, allocation-history export, and Power BI dashboard visualization.

The framework is designed as a research and portfolio-demonstration project, not as a fully automated trading system.

---

## Core Workflow

```text
Macro Environment Filter
→ Market Structure Classification
→ Allocation Scoring
→ Execution Monitoring
→ Position & Risk Management
→ Analytics / Validation
→ Dashboard Visualization
```

The framework focuses on:

- Macro-aware ETF allocation
- Selected-equity execution monitoring
- Market-structure interpretation
- Relative-strength comparison
- Pullback and continuation signal review
- Staged exposure management
- Risk and drawdown control
- Power BI dashboard reporting

The system is primarily designed around US equity, growth, commodity, defensive, and risk-off structures rather than traditional global macro forecasting.

Macro signals are used as broad environment filters. They do not directly predict the market or automatically determine final trades.

---

## Project Positioning

This repository demonstrates the public research and analytics layer of a broader macro-aware investment framework.

The completed public-facing MVP includes:

- Python-based macro regime monitoring
- Market-structure classification
- Allocation score generation
- Latest allocation snapshot export
- Allocation history export
- Power BI dashboard visualization
- Public-safe architecture documentation

Operational spreadsheet modules are used separately for live decision-support, including option-timing review, pullback-signal evaluation, continuation confirmation, and staged risk-management workflows.

Sensitive trading parameters, live trade decisions, private thresholds, and discretionary execution details are not included in this public repository.

---

## Current Development Status

### Completed MVP

The current Python MVP has completed the following components:

- Macro regime monitoring
- Market-structure classification
- Allocation scoring
- Latest allocation snapshot CSV export
- Allocation history CSV export
- Power BI latest allocation dashboard
- Power BI allocation history monitor
- Public-safe project architecture documentation

The current Power BI dashboard includes:

- Latest allocation view
- Macro regime context
- Market-structure context
- Volatility context
- Risk-gate display
- Allocation history monitor

---

### In Progress

Current development work focuses on expanding the Python research layer and improving the portfolio-ready documentation.

In-progress modules include:

- Python migration of execution-signal logic
- Pullback and continuation-entry logic integration
- Position-state tracking
- Staged risk-management logic
- Trade logging and risk-performance analytics
- Power BI documentation and presentation-ready screenshots
- Public README and architecture alignment with resume positioning

---

### Planned Extensions

Future development may include:

- Automated option and execution-data ingestion
- Historical backtesting
- Walk-forward validation
- Out-of-sample testing
- Monte Carlo robustness analysis
- Expanded risk-adjusted performance analytics
- AWS-supported scalable research workflows
- Broker API or live automation review only after validation

These planned extensions are not presented as completed functionality.

---

## System Features

### 1. Macro Environment Filter

The macro layer provides broad investment context using cross-asset indicators.

It supports simplified macro regime interpretation, including:

- Panic risk-off
- Inflation risk-off
- Liquidity tightening
- Liquidity risk-on

The macro layer is used as an environment filter, not as a standalone trading signal.

---

### 2. Market Structure Classification

The market-structure layer evaluates whether current market leadership is concentrated in growth, defensive, commodity, hedge, or mixed structures.

This layer supports:

- Relative-strength comparison
- Leadership monitoring
- Risk-on / risk-off structure interpretation
- Growth versus hedge or commodity comparison
- Dashboard-level market context

The purpose is to understand tradable structure before allocation or execution decisions are reviewed.

---

### 3. Allocation Scoring

The allocation layer converts macro and market-structure context into category-level allocation preferences.

It supports:

- Category score calculation
- Eligible score adjustment
- Strongest-category monitoring
- Capital-restriction decision scenarios
- Latest allocation snapshot generation
- Allocation history tracking

The allocation output is exported to CSV and visualized in Power BI.

---

### 4. Execution Monitoring

The execution-monitoring layer is designed to support trade review rather than fully automated order placement.

It includes logic for:

- Pullback review
- Continuation confirmation
- Breakout versus pullback entry distinction
- Execution-condition evaluation
- Staged deployment review

Current live execution-support workflows remain spreadsheet-based and discretionary. Python integration is ongoing.

---

### 5. Position and Risk Management

The risk-management layer focuses on staged exposure control and capital protection.

It is designed to support:

- Position-state monitoring
- Incremental exposure management
- Breakeven transition logic
- Early-protection review
- Trailing-risk framework design
- Drawdown-control methodology
- Volatility-aware exposure review

This layer is being migrated from spreadsheet logic into Python modules.

---

### 6. Analytics and Validation

The analytics layer is designed to evaluate strategy behavior, risk-adjusted performance, and robustness.

Current and planned analytics include:

- Trade logging
- Return analysis
- Volatility analysis
- Sharpe ratio
- Maximum drawdown
- Recovery factor
- Basic backtesting workflows
- Walk-forward validation planning
- Monte Carlo robustness planning

Historical backtesting, walk-forward validation, and Monte Carlo robustness analysis are planned extensions and should not be interpreted as fully completed production validation.

---

### 7. Power BI Visualization

The Power BI layer converts exported Python outputs into dashboard views.

Current dashboard pages include:

- Latest macro allocation dashboard
- Allocation history monitor

The dashboard is designed for:

- Portfolio presentation
- Investment research discussion
- Interview demonstration
- System workflow explanation

The Power BI `.pbix` file is kept local and is not committed to the public repository by default, because it may contain local file paths, sample outputs, and internal model metadata.

---

## Technology Stack

### Programming and Data

- Python
- pandas
- NumPy
- SQL
- CSV-based data exchange

### Visualization

- Power BI
- Excel
- Google Sheets

### Infrastructure and Workflow

- GitHub
- AWS EC2
- Linux command line

---

## Repository Structure

```text
data/
scripts/
macro/
dashboard/
allocation/
execution/
risk_management/
analytics/
dashboard_export/
powerbi/
docs/
```

| Folder              | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| `data/`             | Historical market and macro data storage                   |
| `scripts/`          | Utility scripts and pipeline runners                       |
| `macro/`            | Macro regime monitoring and environment filtering          |
| `dashboard/`        | Market-structure and relative-strength monitoring          |
| `allocation/`       | Allocation score and category preference logic             |
| `execution/`        | Pullback, continuation, and execution-monitoring workflows |
| `risk_management/`  | Position-state and staged exposure-control logic           |
| `analytics/`        | Backtesting, trade logging, and risk analytics             |
| `dashboard_export/` | Python-to-Power BI CSV export layer                        |
| `powerbi/`          | Power BI dashboard documentation and local dashboard files |
| `docs/`             | Architecture, workflow, and project documentation          |

---

## Public / Private Boundary

This public repository is designed to demonstrate the research architecture, data workflow, and analytics approach.

The following items are intentionally excluded from the public repository:

- Private trading parameters
- Live position details
- Real-time execution decisions
- Sensitive option-timing rules
- Broker API credentials
- Full discretionary trade review notes
- Private backtesting output files
- Local Power BI `.pbix` files unless separately reviewed

The goal is to present the system architecture and research workflow without exposing sensitive trading logic.

---

## Research Philosophy

The framework prioritizes tradable execution quality and risk control over full-market narrative prediction.

It focuses on:

- Identifying tradable market structure
- Monitoring macro environment risk
- Comparing relative strength across asset categories
- Reviewing execution quality before deployment
- Managing exposure through staged risk controls
- Building research outputs that can be visualized and explained

The system is not designed to predict exact market tops or bottoms.

It is designed to support disciplined decision-making under changing macro and market-structure conditions.

---

## Portfolio Use

This project can be used as a portfolio demonstration for roles related to:

- Quantitative investment research
- Financial data analysis
- Portfolio analytics
- ETF strategy research
- Systematic investment research
- Power BI dashboard development
- Python-based financial analytics

The project demonstrates the ability to connect:

```text
Investment logic
→ Data pipeline
→ Python research modules
→ CSV export
→ Power BI dashboard
→ Portfolio-ready explanation
```

---

## Disclaimer

This repository is for research, educational, and demonstration purposes only.

It does not constitute investment advice, financial advice, or a recommendation to buy or sell any security.

The framework is not a production trading system and should not be used for live trading without independent validation, risk review, and compliance consideration.
