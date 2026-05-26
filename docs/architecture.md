# Macro-Aware ETF and Selected-Equity Framework Architecture

This document describes the public-safe architecture of the Systematic Macro Quant Investment Framework.

The framework is a macro-aware ETF and selected-equity allocation, execution-monitoring, and risk-management research system. It converts spreadsheet-based investment decision-support workflows into Python research modules, CSV export pipelines, and Power BI dashboard visualization.

The architecture is designed for research, portfolio demonstration, and interview discussion. It is not presented as a fully automated trading system.

---

## 1. Architecture Overview

The system follows a layered workflow:

```text
Data Layer
→ Macro Regime Layer
→ Market Structure Layer
→ Allocation Layer
→ Execution Monitoring Layer
→ Position and Risk Management Layer
→ Analytics and Validation Layer
→ Dashboard Visualization Layer
```

Each layer has a separate responsibility so that macro context, allocation logic, execution review, risk control, and visualization can be developed and validated independently.

---

## 2. Current System Status

### Completed MVP

The current Python MVP includes:

- Macro regime monitoring
- Market-structure classification
- Allocation scoring
- Latest allocation snapshot CSV export
- Allocation history CSV export
- Power BI latest allocation dashboard
- Power BI allocation history monitor
- Public-safe documentation structure

### In Progress

Current development work focuses on:

- Python migration of execution-signal logic
- Pullback and continuation-entry integration
- Position-state tracking
- Staged risk-management logic
- Trade logging and risk-performance analytics
- Portfolio-ready Power BI documentation and screenshots

### Planned Extensions

Planned future development may include:

- Automated option and execution-data ingestion
- Historical backtesting
- Walk-forward validation
- Out-of-sample testing
- Monte Carlo robustness analysis
- Expanded risk-adjusted performance analytics
- AWS-supported scalable research workflows
- Broker API or live automation review only after validation

These planned extensions are not described as completed production functionality.

---

## 3. Layered Architecture

## 3.1 Data Layer

### Purpose

The data layer stores and prepares market, macro, and research input data for downstream modules.

### Responsibilities

- Store historical market data
- Store macro indicator data
- Maintain structured CSV inputs
- Provide standardized data loading for Python modules
- Support repeatable research workflows

### Current Status

Completed for the current MVP at a basic structured CSV level.

### In Progress / Future Work

- Improve automated data refresh workflows
- Expand data quality checks
- Add more structured validation before downstream processing

---

## 3.2 Macro Regime Layer

### Purpose

The macro regime layer provides broad investment environment context.

It is used as an environment filter, not as a direct trading signal.

### Responsibilities

- Monitor cross-asset macro conditions
- Interpret volatility, liquidity, rate, and inflation pressure
- Classify simplified macro environments
- Provide regime context to allocation and dashboard layers

### Supported Public Regime Categories

- Panic risk-off
- Inflation risk-off
- Liquidity tightening
- Liquidity risk-on

### Current Status

Completed in the Python MVP.

### Important Boundary

The macro layer does not automatically determine final trades. It provides context for later allocation and execution review.

---

## 3.3 Market Structure Layer

### Purpose

The market-structure layer evaluates tradable leadership and relative strength across asset categories.

### Responsibilities

- Compare risk-on, defensive, commodity, and hedge structures
- Identify whether growth leadership is strong or weak
- Monitor mixed-market conditions
- Provide dashboard-level market context
- Support allocation scoring

### Current Status

Completed in the Python MVP.

### Public-Safe Design

This layer is described by asset categories rather than full public ticker lists.

---

## 3.4 Allocation Layer

### Purpose

The allocation layer converts macro and market-structure context into category-level allocation preferences.

### Responsibilities

- Generate category scores
- Adjust scores based on eligibility rules
- Support strongest-category interpretation
- Support capital-restriction decision scenarios
- Export latest allocation snapshots
- Append allocation history snapshots

### Current Status

Completed in the Python MVP.

### Current Outputs

- Latest allocation snapshot CSV
- Allocation history CSV
- Power BI-ready allocation fields

### Important Boundary

The allocation output is a research and decision-support output. It is not a direct automated order-placement instruction.

---

## 3.5 Execution Monitoring Layer

### Purpose

The execution-monitoring layer supports trade review and execution-quality assessment.

### Responsibilities

- Review pullback conditions
- Review continuation conditions
- Distinguish breakout-style and pullback-style entries
- Evaluate execution readiness
- Support staged deployment decisions
- Integrate spreadsheet-based live decision-support logic into Python over time

### Current Status

In progress.

### Current Implementation Boundary

Operational execution-support workflows currently remain partly in Google Sheets / Excel and are reviewed discretionarily.

Python integration is ongoing.

### Important Boundary

This layer is not currently presented as a completed fully automated live execution engine.

---

## 3.6 Position and Risk Management Layer

### Purpose

The risk-management layer supports staged exposure control and capital protection.

### Responsibilities

- Track position state
- Support staged exposure management
- Review breakeven transitions
- Review early-protection logic
- Support trailing-risk framework design
- Monitor drawdown risk
- Support volatility-aware exposure review

### Current Status

In progress.

### Important Boundary

The public repository documents the framework and migration structure, but does not expose private thresholds, live position details, or full discretionary trade review rules.

---

## 3.7 Analytics and Validation Layer

### Purpose

The analytics layer evaluates strategy behavior, performance, drawdown, and robustness.

### Responsibilities

- Trade logging
- Return analysis
- Volatility analysis
- Sharpe ratio evaluation
- Maximum drawdown evaluation
- Recovery factor monitoring
- Basic backtesting workflows
- Walk-forward validation planning
- Monte Carlo robustness planning

### Current Status

Partly in progress / planned.

### Completed Scope

Basic analytics design and risk-performance metric planning are part of the research framework.

### Planned Scope

- Full historical backtesting
- Walk-forward validation
- Out-of-sample testing
- Monte Carlo robustness analysis
- Scalable AWS-supported research workflows

### Important Boundary

Walk-forward validation and Monte Carlo robustness analysis are planned extensions unless separately documented as completed in future versions.

---

## 3.8 Dashboard Visualization Layer

### Purpose

The visualization layer converts Python outputs into portfolio-ready dashboard views.

### Responsibilities

- Load exported CSV snapshots
- Visualize latest allocation context
- Display macro regime context
- Display market-structure context
- Display volatility and risk-gate context
- Track allocation history over time
- Support portfolio screenshots and interview discussion

### Current Status

Completed for the first Power BI MVP.

### Current Dashboard Pages

- Latest macro allocation dashboard
- Allocation history monitor

### Important Boundary

The local Power BI `.pbix` file is not committed to the public repository by default, because it may contain local file paths, sample outputs, and internal model metadata.

---

## 4. Data Flow

The current MVP data flow is:

```text
Market and macro data
→ Python data loading
→ Macro regime generation
→ Market-structure classification
→ Allocation scoring
→ Latest allocation snapshot export
→ Allocation history append
→ Power BI dashboard visualization
```

The current export layer produces Power BI-ready CSV outputs.

The Power BI dashboard reads these outputs to display latest allocation state and allocation history.

---

## 5. Repository Structure

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

| Folder              | Architectural Role                                              | Status                |
| ------------------- | --------------------------------------------------------------- | --------------------- |
| `data/`             | Historical market and macro data storage                        | Active                |
| `scripts/`          | Utility scripts and pipeline runners                            | Active                |
| `macro/`            | Macro regime monitoring and environment filtering               | MVP completed         |
| `dashboard/`        | Market-structure and relative-strength monitoring               | MVP completed         |
| `allocation/`       | Allocation score and category preference logic                  | MVP completed         |
| `execution/`        | Pullback, continuation, and execution-monitoring workflows      | In progress           |
| `risk_management/`  | Position-state and staged exposure-control logic                | In progress           |
| `analytics/`        | Backtesting, trade logging, and risk analytics                  | In progress / planned |
| `dashboard_export/` | Python-to-Power BI CSV export layer                             | MVP completed         |
| `powerbi/`          | Dashboard visualization documentation and local dashboard files | MVP completed locally |
| `docs/`             | Architecture, workflow, and project documentation               | Active                |

---

## 6. Public / Private Boundary

The public repository is designed to demonstrate:

- Research architecture
- Data workflow
- Python module structure
- Allocation and dashboard logic
- Public-safe project documentation
- Portfolio-ready technical explanation

The following items are intentionally excluded or kept private:

- Private trading parameters
- Full live trading rules
- Sensitive option-timing details
- Live position details
- Real-time discretionary trade notes
- Broker API credentials
- Private backtesting outputs
- Local Power BI `.pbix` files unless separately reviewed
- Any files containing sensitive execution thresholds or private decision rules

This boundary helps the project remain useful for portfolio demonstration while protecting trading logic and private research details.

---

## 7. Alignment With Resume Positioning

This architecture aligns with the resume positioning:

- Completed Python MVP:
  - macro regime monitoring
  - market-structure classification
  - allocation scoring
  - CSV export
  - Power BI dashboard visualization

- Current operational support:
  - spreadsheet-based option-timing review
  - pullback-signal evaluation
  - continuation confirmation
  - staged risk-management workflows
  - ETF and selected-equity execution monitoring

- Future extensions:
  - automated option / execution-data ingestion
  - Python-based execution-signal integration
  - historical backtesting
  - walk-forward validation
  - Monte Carlo robustness analysis

The architecture avoids presenting planned or partially migrated modules as completed production automation.

---

## 8. Design Principles

The framework follows these design principles:

- Separate macro context from execution decisions
- Separate public architecture from private trading parameters
- Use Python for repeatable research workflows
- Use CSV exports as a simple and auditable bridge to Power BI
- Use Power BI for portfolio-ready visualization
- Keep live execution discretionary until sufficient validation is completed
- Avoid overstating unvalidated alpha or incomplete automation
- Prioritize risk control and explainability over black-box complexity

---

## 9. Research Philosophy

The framework prioritizes tradable execution quality and risk control over full-market narrative prediction.

It focuses on:

- Understanding macro environment risk
- Interpreting market structure
- Comparing relative strength across asset categories
- Reviewing execution quality before deployment
- Managing staged exposure
- Evaluating risk-adjusted performance over time

The system is not designed to predict exact market tops or bottoms.

It is designed to support disciplined decision-making under changing macro and market-structure conditions.

---

## 10. Disclaimer

This repository is for research, educational, and demonstration purposes only.

It does not constitute investment advice, financial advice, or a recommendation to buy or sell any security.

The framework is not a production trading system and should not be used for live trading without independent validation, risk review, and compliance consideration.
