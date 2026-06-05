"""
Public-safe risk-management backtest / replay engine.

This module replays historical price data through position_risk_engine.py.

Purpose:
- Feed historical prices into the existing position risk engine.
- Track daily position stage, risk action, peak price, trailing status,
  stop level, add trigger, and drawdown.
- Provide a foundation for later daily OHLC and minute-level backtesting.

Important boundary:
- This is NOT a full strategy backtest yet.
- It does not generate entry signals.
- It does not ingest private option-timing rules.
- It does not execute real trades.
- It only replays risk-management logic after a given entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from risk_management.position_risk_engine import (
    PositionInput,
    PositionTier,
    RiskAction,
    evaluate_position_risk,
)
from risk_management.risk_rule_loader import TradeRule


@dataclass(frozen=True)
class RiskBacktestConfig:
    """
    Configuration for one risk-management replay.

    asset:
        Ticker or asset name.

    entry_date:
        First date from which the replay should start.
        The price dataframe must contain this date or later dates.

    entry_price:
        Actual entry price used for return, stop, breakeven,
        profit threshold, and trailing calculations.

    initial_position_tier:
        Starting generic position tier: LOW, MID, or HIGH.

    anchor_price:
        Optional anchor price for add-step logic.
        If None, entry_price will be used.

    entry_type:
        Optional label such as pullback, breakout, continuation.
        Current risk engine accepts this field but does not expose
        private signal logic.
    """

    asset: str
    entry_date: str
    entry_price: float
    initial_position_tier: PositionTier
    anchor_price: float | None = None
    entry_type: str = ""


def _normalize_position_tier(position_tier: PositionTier | str) -> PositionTier:
    """
    Convert string or PositionTier into PositionTier enum.
    """
    if isinstance(position_tier, PositionTier):
        return position_tier

    text = str(position_tier).strip().upper()

    try:
        return PositionTier[text]
    except KeyError as exc:
        valid_values = ", ".join(tier.name for tier in PositionTier)
        raise ValueError(
            f"Invalid position tier: {position_tier}. "
            f"Valid values are: {valid_values}"
        ) from exc


def _prepare_price_data(
    price_data: pd.DataFrame,
    entry_date: str,
) -> pd.DataFrame:
    """
    Prepare price dataframe for risk replay.

    Required columns:
        Date
        Close

    The dataframe is filtered to dates >= entry_date and sorted ascending.
    """
    required_columns = {"Date", "Close"}
    missing_columns = required_columns - set(price_data.columns)

    if missing_columns:
        raise ValueError(
            f"Price data is missing required columns: {sorted(missing_columns)}"
        )

    df = price_data.copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])
    df = df.sort_values("Date").reset_index(drop=True)

    start_date = pd.to_datetime(entry_date)
    df = df[df["Date"] >= start_date].reset_index(drop=True)

    if df.empty:
        raise ValueError(
            "No price rows found on or after entry_date. "
            f"entry_date={entry_date}"
        )

    return df


def _enum_value(value: object) -> object:
    """
    Convert enum values to strings for dataframe output.
    """
    if hasattr(value, "value"):
        return value.value

    return value


def _should_stop_replay(action: RiskAction) -> bool:
    """
    Decide whether replay should stop after a risk action.

    For the first version:
    - STOP_OUT
    - STOP_OUT_BE
    - EXIT_ALL

    stop the replay.

    REDUCE_TO_MID and REDUCE_TO_LOW do not stop the replay.
    They update the position tier and continue.
    """
    return action in {
        RiskAction.STOP_OUT,
        RiskAction.STOP_OUT_BE,
        RiskAction.EXIT_ALL,
    }


def _update_position_tier_after_action(
    current_tier: PositionTier,
    action: RiskAction,
) -> PositionTier:
    """
    Update generic position tier after add / reduce / exit action.

    This remains public-safe because it only uses generic tiers.
    It does not expose real position percentages.
    """
    if action == RiskAction.ADD_TO_MID:
        return PositionTier.MID

    if action == RiskAction.ADD_TO_HIGH:
        return PositionTier.HIGH

    if action == RiskAction.REDUCE_TO_MID:
        return PositionTier.MID

    if action == RiskAction.REDUCE_TO_LOW:
        return PositionTier.LOW

    if action in {
        RiskAction.STOP_OUT,
        RiskAction.STOP_OUT_BE,
        RiskAction.EXIT_ALL,
    }:
        return PositionTier.NONE

    return current_tier


def run_risk_replay(
    price_data: pd.DataFrame,
    rule: TradeRule,
    config: RiskBacktestConfig,
) -> pd.DataFrame:
    """
    Replay risk-management logic over historical daily close data.

    Parameters
    ----------
    price_data:
        DataFrame with columns:
            Date
            Close

    rule:
        TradeRule loaded from private config/trade_rules_config.csv.

    config:
        RiskBacktestConfig for one asset and one entry.

    Returns
    -------
    pd.DataFrame
        One row per replay date.

    Notes
    -----
    This first version uses Close price only.
    Later versions can add:
        Open
        High
        Low
        intraday stop trigger
        minute-level Polygon data
    """
    df = _prepare_price_data(
        price_data=price_data,
        entry_date=config.entry_date,
    )

    current_tier = _normalize_position_tier(config.initial_position_tier)
    anchor_price = config.anchor_price or config.entry_price
    peak_price: float | None = None

    rows: list[dict[str, object]] = []

    for _, row in df.iterrows():
        current_date = row["Date"]
        current_price = float(row["Close"])

        position = PositionInput(
            asset=config.asset,
            position_tier=current_tier,
            entry_price=config.entry_price,
            anchor_price=anchor_price,
            current_price=current_price,
            peak_price=peak_price,
            entry_type=config.entry_type,
        )

        result = evaluate_position_risk(
            position=position,
            rule=rule,
        )

        rows.append(
            {
                "date": current_date.date().isoformat(),
                "asset": result.asset,
                "close": current_price,
                "entry_price": config.entry_price,
                "anchor_price": anchor_price,
                "position_tier": current_tier.value,
                "stage": _enum_value(result.stage),
                "risk_action": _enum_value(result.action),
                "trailing_started": result.trailing_started,
                "return_pct": result.return_pct,
                "peak_drawdown_pct": result.peak_drawdown_pct,
                "active_stop_price": result.active_stop_price,
                "trailing_stop_price": result.trailing_stop_price,
                "effective_stop_price": (
                    result.trailing_stop_price
                    if result.trailing_stop_price is not None
                    else result.active_stop_price
                ),
                "profit_threshold_price": result.profit_threshold_price,                                            
                "next_add_trigger_price": result.next_add_trigger_price,
                "updated_peak_price": result.updated_peak_price,
            }
        )

        peak_price = result.updated_peak_price

        current_tier = _update_position_tier_after_action(
            current_tier=current_tier,
            action=result.action,
        )

        if _should_stop_replay(result.action):
            break

    return pd.DataFrame(rows)


def run_risk_replay_from_csv(
    price_csv_path: str,
    rule: TradeRule,
    config: RiskBacktestConfig,
) -> pd.DataFrame:
    """
    Load historical price data from CSV and run risk replay.

    CSV must contain:
        Date
        Close
    """
    price_data = pd.read_csv(price_csv_path)

    return run_risk_replay(
        price_data=price_data,
        rule=rule,
        config=config,
    )


def format_replay_output(
    replay_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a human-readable copy of replay output.

    Calculation columns remain decimals in the raw replay result.
    This formatter converts percentage fields into percent-style strings
    for local inspection only.
    """
    df = replay_df.copy()

    percent_columns: Iterable[str] = [
        "return_pct",
        "peak_drawdown_pct",
    ]

    for column in percent_columns:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda value: ""
                if pd.isna(value)
                else f"{value:.2%}"
            )

    price_columns: Iterable[str] = [
        "close",
        "entry_price",
        "anchor_price",
        "active_stop_price",
        "trailing_stop_price",
        "effective_stop_price",
        "profit_threshold_price",
        "next_add_trigger_price",
        "updated_peak_price",
    ]

    for column in price_columns:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda value: ""
                if pd.isna(value)
                else f"{value:.2f}"
            )

    return df