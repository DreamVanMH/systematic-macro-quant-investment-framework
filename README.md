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
- Public-safe position risk-management engine
- Close-price-based risk-management replay engine
- OHLC-based risk-management replay with daily intraday stop-touch detection

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

This layer has been partially migrated from spreadsheet logic into Python modules.

The current public Python implementation includes:

- A public-safe position risk-management engine
- Generic position tiers using LOW / MID / HIGH / NONE
- Staged add, reduce, breakeven-stop, trailing-stop, and exit actions
- A close-price-based risk-management replay engine
- An OHLC-based risk-management replay engine
- Replay output for stage, action, trailing status, peak price, drawdown, and effective stop price
- Daily OHLC stop-touch detection using the effective stop level
- OHLC warning output when daily high/low sequence is ambiguous

The replay engines are designed to validate staged risk-management behavior after a predefined entry. They are not full trade-entry backtesting engines and do not include option-timing signals, pullback scoring, continuation-entry signals, broker execution logic, or minute-level intraday stop simulation.

The OHLC replay layer uses daily Open, High, Low, and Close data to check whether the effective stop level was touched during the day. Because daily OHLC data does not show whether the high or low occurred first, sequence-ambiguous rows may be marked with:

```text
daily_ohlc_sequence_unknown
This OHLC replay layer is an intermediate validation layer between close-only replay and future minute-level replay.
```

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
- Close-price-based risk-management replay
- OHLC-based risk-management replay with daily stop-touch detection
- Basic backtesting workflow planning
- Walk-forward validation planning
- Monte Carlo robustness planning

The current replay engines validate staged risk-management behavior using historical close prices and daily OHLC data. The OHLC layer can detect whether an effective stop level was touched within a daily price bar, but it cannot determine the exact intraday sequence of high and low prices.

Full trade-entry backtesting, minute-level intraday stop simulation, walk-forward validation, and Monte Carlo robustness analysis are planned extensions and should not be interpreted as completed production validation.

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

## Daily Market Data Pipeline Automation

This project includes a scheduled daily pipeline used to refresh market data, rebuild processed data, generate macro snapshots, and export allocation dashboard files.

### Pipeline Steps

The daily pipeline runs the following scripts in order:

```bash
python scripts/data_loader.py
python scripts/download_fred_data.py
python scripts/load_all_data.py
python scripts/run_macro_snapshot.py
python dashboard_export/export_allocation_snapshot.py
```

These steps perform the following workflow:

1. Download or update market data.
2. Download or update FRED macro data.
3. Rebuild standardized processed data.
4. Generate the macro environment snapshot.
5. Export the latest allocation snapshot and allocation history for dashboard use.

### Unified Runner

Instead of running each script manually, use the unified daily pipeline runner:

```bash
python scripts/run_daily_pipeline.py
```

For manual testing, especially on weekends or outside the normal weekday guard, use:

```bash
python scripts/run_daily_pipeline.py --force
```

### Output Files

The allocation export step writes dashboard-ready CSV files to:

```text
dashboard_export/output/allocation_snapshot.csv
dashboard_export/output/allocation_snapshot_history.csv
```

The daily pipeline writes runtime logs to:

```text
logs/daily_pipeline_YYYY-MM-DD.log
```

Example:

```text
logs/daily_pipeline_2026-06-23.log
```

Runtime logs are not tracked by Git.

### Windows Task Scheduler Setup

The pipeline is scheduled through Windows Task Scheduler using:

```text
run_daily_pipeline.bat
```

The scheduled task name is:

```text
Daily Market Pipeline
```

The task is configured with five daily triggers:

```text
7:30 AM
10:30 AM
11:30 AM
12:30 PM
1:30 PM
```

This schedule allows the system to refresh snapshots during the trading day and after the market close.

### Recommended Task Scheduler Settings

Recommended settings:

```text
Allow task to be run on demand
Run task as soon as possible after a scheduled start is missed
If the task fails, restart every 5 minutes, up to 3 times
If the task is already running, do not start a new instance
```

Recommended conditions:

```text
Do not require the computer to be idle
Do not require AC power
Do not require a specific network connection
```

### Windows BAT Runner

The Windows runner uses a fixed project path and Python executable path for stability under Task Scheduler.

Example:

```bat
@echo off
cd /d "C:\Users\yingl\Documents\New folder\OneDrive\systematic-macro-quant-investment-framework"

echo ================================ >> task_scheduler_debug.log
echo Task started at %date% %time% >> task_scheduler_debug.log
echo Current directory: %cd% >> task_scheduler_debug.log
where python >> task_scheduler_debug.log 2>&1

"C:\Program Files\Python313\python.exe" scripts\run_daily_pipeline.py >> task_scheduler_debug.log 2>&1

echo Task finished at %date% %time% >> task_scheduler_debug.log
echo ================================ >> task_scheduler_debug.log
```

The debug log is used to verify that Task Scheduler correctly calls the BAT file and Python pipeline.

### Git Ignore Rules

Runtime logs should not be committed.

The following entries should be included in `.gitignore`:

```gitignore
# Runtime logs
logs/
task_scheduler_debug.log
```

### Validation

A successful run should end with:

```text
Daily pipeline completed successfully.
```

The expected final output includes:

```text
dashboard_export/output/allocation_snapshot.csv
dashboard_export/output/allocation_snapshot_history.csv
```

The Task Scheduler manual run has been validated successfully. The pipeline was confirmed to run through the full chain:

```text
Windows Task Scheduler
→ run_daily_pipeline.bat
→ scripts/run_daily_pipeline.py
→ data_loader
→ download_fred_data
→ load_all_data
→ run_macro_snapshot
→ export_allocation_snapshot
```

### Notes

If the project is moved to another computer or folder, update the project path in `run_daily_pipeline.bat`.

If Python is upgraded or reinstalled, update the Python executable path in `run_daily_pipeline.bat`.

Current example paths:

```bat
cd /d "C:\Users\yingl\Documents\New folder\OneDrive\systematic-macro-quant-investment-framework"
"C:\Program Files\Python313\python.exe" scripts\run_daily_pipeline.py
```

The main risk is that Task Scheduler may show a successful task status while the actual pipeline output is not refreshed because of a path or Python environment issue. For this reason, `task_scheduler_debug.log` should be kept during the first few days of scheduled runs.

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
