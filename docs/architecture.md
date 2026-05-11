# Institutional Macro Quant Research Framework Architecture

This repository follows a layered institutional-style investment research workflow:

Macro Signals
→ Regime Classification
→ Trade Bias
→ Structure Analysis
→ Allocation
→ Execution
→ Risk Management
→ Analytics
→ Dashboard Visualization

---

# Repository Structure

## macro/

Purpose:
Cross-asset macro monitoring and signal generation.

Examples:

- VIX regime analysis
- USD liquidity tracking
- Treasury yield monitoring
- Commodity inflation pressure
- AI-chain macro leadership

---

## regime/

Purpose:
Market regime classification engine.

Examples:

- Risk-on
- Risk-off
- Inflationary pressure
- Liquidity tightening
- Defensive rotation

---

## trade_bias/

Purpose:
Translate macro regime into directional portfolio bias.

Examples:

- Growth overweight
- Hedge activation
- Commodity preference
- Defensive positioning

---

## structure/

Purpose:
Technical and structural confirmation layer.

Examples:

- Breakout confirmation
- Pullback scoring
- Relative strength comparison
- Cross-asset structure alignment
- Support / resistance framework

---

## allocation/

Purpose:
Portfolio allocation and capital distribution logic.

Examples:

- ETF weighting
- Selected asset engine
- Single-asset prioritization
- Exposure scaling
- Allocation rotation

---

## execution/

Purpose:
Trade execution workflow and position-state management.

Examples:

- Entry engine
- Add-position logic
- Break-even protection
- Trailing-profit management
- Position-state transitions

---

## risk_management/

Purpose:
Portfolio and position-level risk controls.

Examples:

- Stop-loss management
- Drawdown control
- Exposure protection
- Volatility-aware sizing
- Capital preservation logic

---

## analytics/

Purpose:
Research analytics and robustness evaluation.

Examples:

- Sharpe ratio
- Maximum drawdown
- Recovery factor
- Walk-forward analysis
- Monte Carlo testing
- Risk-adjusted performance evaluation

---

## dashboard_export/

Purpose:
Intermediate export layer between Python research modules and visualization systems.

Examples:

- CSV exports
- Signal snapshots
- Allocation summaries
- Position-state exports

---

## powerbi/

Purpose:
Institutional-style dashboard visualization and reporting.

Examples:

- Macro dashboard
- Allocation dashboard
- Risk dashboard
- Position tracking
- Presentation-ready charts

---

## docs/

Purpose:
Research framework documentation and architecture references.

Examples:

- Workflow explanation
- Architecture diagrams
- Research notes
- Framework mapping

---

# Research Philosophy

This framework is designed around institutional-style multi-layer investment decision workflows rather than single-indicator trading systems.

Core philosophy:

Macro
→ Regime
→ Bias
→ Structure
→ Allocation
→ Execution
→ Risk Management

The framework prioritizes:

- Cross-asset confirmation
- Layered signal validation
- Risk-adjusted positioning
- Staged exposure management
- Institutional-style portfolio thinking

---

# Disclaimer

This repository is for research, educational, and demonstration purposes only and does not constitute investment advice.
