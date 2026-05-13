# Macro-Aware CTA Execution Framework Architecture

This repository follows a layered macro-aware CTA execution workflow:

Macro Environment Filter
→ Trend / Flow Selection
→ Dashboard Relative Strength
→ Pullback Continuation Entry
→ Position & Risk Management
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
- Broad macro environment filtering

---

## dashboard/

Purpose:
Relative-strength monitoring and tradable structure visualization.

Examples:

Growth vs Commodity comparison
Strongest-asset monitoring
Capital-restriction deployment logic
Dashboard trade suggestions
Breadth visualization
Relative-strength structure monitoring

---

## allocation/

Purpose:
Dashboard-based deployment preference and strongest-asset selection logic.

Examples:

- Strongest-asset selection
- Capital-restriction deployment logic
- Dashboard-based allocation preference
- Exposure scaling

---

## execution/

Purpose:
CTA-style trend-following execution and pullback continuation-entry workflows.

Examples:

- Pullback continuation confirmation
- Breakout vs pullback entry logic
- Execution-condition scoring
- Trend continuation monitoring
- Add-position workflows
- Entry-quality refinement

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
Basic research analytics and execution evaluation.

Examples:

- Sharpe ratio
- Maximum drawdown
- Recovery factor
- Trade logging
- Risk-adjusted performance evaluation
- Basic backtesting workflows

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
Dashboard visualization and reporting.

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

The framework prioritizes:

- tradable execution quality
- trend continuation
- staged exposure management
- pullback refinement
- risk-controlled deployment

The framework focuses more on:

- handling markets

rather than:

- fully explaining markets

Macro signals are treated as broad environment filters rather than full-market prediction engines.

---

# Disclaimer

This repository is for research, educational, and demonstration purposes only and does not constitute investment advice.
