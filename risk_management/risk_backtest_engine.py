"""
Risk-management replay engine.

This module provides two replay layers:

1. Close-only replay
   - Uses Date + Close
   - Validates staged position-risk behavior after a given entry

2. OHLC replay
   - Uses Date + Open + High + Low + Close
   - Adds intraday stop-touch detection using daily Low
   - Supports standard OHLC CSV and yfinance multi-header CSV

Important boundary:
This is not a full strategy backtest.
It does not generate entry signals, option timing signals, or intraday execution order.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
import inspect
from typing import Any

from risk_management.position_risk_engine import (
    PositionInput,
    PositionTier,
    evaluate_position_risk,
)


# ---------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------


@dataclass
class RiskBacktestConfig:
    """
    Configuration for replaying risk-management behavior after entry.
    """

    asset: str
    entry_date: str
    entry_price: float
    initial_position_tier: PositionTier
    anchor_price: float | None = None
    entry_type: str = "pullback"


# ---------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------


def _enum_name(value: Any) -> str | None:
    """
    Safely return enum name if value is Enum-like.
    Otherwise return string value.
    """

    if value is None:
        return None

    return getattr(value, "name", str(value))


def _get_attr(obj: Any, names: list[str], default: Any = None) -> Any:
    """
    Safely read the first existing attribute from an object.

    This makes the replay engine more tolerant when RiskOutput field names
    differ slightly across development versions.
    """

    for name in names:
        if hasattr(obj, name):
            return getattr(obj, name)

    return default


def _build_position_input(**kwargs) -> PositionInput:
    """
    Build PositionInput while only passing supported fields.

    This prevents errors when PositionInput does not support fields such as:
    trailing_started.
    """

    signature = inspect.signature(PositionInput)
    allowed_keys = set(signature.parameters.keys())

    filtered_kwargs = {
        key: value
        for key, value in kwargs.items()
        if key in allowed_keys
    }

    return PositionInput(**filtered_kwargs)


def _classify_intraday_stop_type(result: Any) -> str | None:
    """
    Classify stop type for OHLC replay interpretation.

    This helper does not replace position_risk_engine logic.
    It only labels the stop level.
    """

    trailing_stop_price = _get_attr(result, ["trailing_stop_price"], None)
    active_stop_price = _get_attr(result, ["active_stop_price"], None)
    stage = _get_attr(result, ["stage"], None)
    stage_name = _enum_name(stage)

    if trailing_stop_price is not None:
        return "trailing_stop"

    if active_stop_price is not None:
        if stage_name in {"ADD_BE", "FULL_BE"}:
            return "breakeven_stop"
        return "active_stop"

    return None


def _update_tier_from_action(current_tier: PositionTier, risk_action: Any) -> PositionTier:
    """
    Update position tier based on risk action when RiskOutput does not
    return position_tier directly.
    """

    action_name = _enum_name(risk_action)

    if action_name == "ADD_TO_MID":
        return PositionTier.MID

    if action_name == "ADD_TO_HIGH":
        return PositionTier.HIGH

    if action_name == "REDUCE_TO_MID":
        return PositionTier.MID

    if action_name == "REDUCE_TO_LOW":
        return PositionTier.LOW

    if action_name in {"EXIT_ALL", "STOP_OUT", "STOP_OUT_BE"}:
        return PositionTier.NONE

    return current_tier


def _get_effective_stop_price(result: Any) -> float | None:
    """
    Read effective stop if available.
    Otherwise reconstruct from trailing_stop_price / active_stop_price.
    """

    effective_stop_price = _get_attr(result, ["effective_stop_price"], None)

    if effective_stop_price is not None:
        return effective_stop_price

    trailing_stop_price = _get_attr(result, ["trailing_stop_price"], None)
    active_stop_price = _get_attr(result, ["active_stop_price"], None)

    if trailing_stop_price is not None:
        return trailing_stop_price

    return active_stop_price


def _get_updated_peak_price(result: Any, fallback_peak: float) -> float:
    """
    Safely read updated peak price.
    """

    updated_peak_price = _get_attr(result, ["updated_peak_price", "peak_price"], None)

    if updated_peak_price is None:
        return fallback_peak

    return float(updated_peak_price)


def _to_float_or_none(value: Any) -> float | None:
    """
    Convert numeric value safely.
    """

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------
# Close-only replay
# ---------------------------------------------------------------------


def run_risk_replay(
    price_rows: list[dict],
    config: RiskBacktestConfig,
    trade_rule,
) -> list[dict]:
    """
    Run close-price-based risk-management replay.

    Expected price_rows columns:
    - Date
    - Close

    This preserves the original close-only replay behavior:
    - use Close as current price
    - update peak using Close
    - run evaluate_position_risk()
    - update tier from result or action
    """

    replay_rows: list[dict] = []

    current_tier = config.initial_position_tier
    peak_price = config.entry_price
    trailing_started = False

    anchor_price = config.anchor_price
    if anchor_price is None:
        anchor_price = config.entry_price

    for row in price_rows:
        date = row["Date"]
        close_price = float(row["Close"])

        updated_peak_price = max(peak_price, close_price)

        position_input = _build_position_input(
            asset=config.asset,
            current_price=close_price,
            entry_price=config.entry_price,
            anchor_price=anchor_price,
            position_tier=current_tier,
            peak_price=updated_peak_price,
            entry_type=config.entry_type,
            trailing_started=trailing_started,
        )

        result = evaluate_position_risk(
            position=position_input,
            rule=trade_rule,
        )

        risk_action = _get_attr(result, ["risk_action", "action"], None)
        stage = _get_attr(result, ["stage"], None)
        result_position_tier = _get_attr(result, ["position_tier"], None)
        # Close-entry replay rule:
        # On the entry date, the position is assumed to be opened at the close.
        # Therefore, do not allow same-day close-based stop-out actions.
        if is_entry_date:
            risk_action = "HOLD"

        output_tier = (
            result_position_tier
            if result_position_tier is not None
            else current_tier
        )

        effective_stop_price = _get_effective_stop_price(result)
        output_peak_price = _get_updated_peak_price(result, updated_peak_price)

        replay_rows.append(
            {
                "date": date,
                "asset": config.asset,
                "close": close_price,
                "entry_price": config.entry_price,
                "anchor_price": anchor_price,
                "position_tier": _enum_name(output_tier),
                "stage": _enum_name(stage),
                "risk_action": _enum_name(risk_action),
                "trailing_started": _get_attr(
                    result,
                    ["trailing_started"],
                    trailing_started,
                ),
                "return_pct": _get_attr(result, ["return_pct"], None),
                "peak_drawdown_pct": _get_attr(result, ["peak_drawdown_pct"], None),
                "active_stop_price": _get_attr(result, ["active_stop_price"], None),
                "trailing_stop_price": _get_attr(result, ["trailing_stop_price"], None),
                "effective_stop_price": effective_stop_price,
                "profit_threshold_price": _get_attr(result, ["profit_threshold_price"], None),
                "next_add_trigger_price": _get_attr(result, ["next_add_trigger_price"], None),
                "updated_peak_price": output_peak_price,
            }
        )

        if result_position_tier is not None:
            current_tier = result_position_tier
        else:
            current_tier = _update_tier_from_action(current_tier, risk_action)

        peak_price = output_peak_price
        trailing_started = _get_attr(result, ["trailing_started"], trailing_started)

        if current_tier == PositionTier.NONE:
            break

    return replay_rows


def run_risk_replay_from_csv(
    csv_path: str,
    config: RiskBacktestConfig,
    trade_rule,
) -> list[dict]:
    """
    Load close-only price CSV and run close-only replay.

    Supported columns:
    - Date / date / Datetime / datetime / Timestamp / timestamp / Unnamed: 0
    - Close
    """

    price_rows: list[dict] = []

    possible_date_columns = [
        "Date",
        "date",
        "Datetime",
        "datetime",
        "Timestamp",
        "timestamp",
        "Unnamed: 0",
    ]

    with open(csv_path, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"CSV file has no header: {csv_path}")

        fieldnames = set(reader.fieldnames)

        if "Close" not in fieldnames:
            raise ValueError(
                "Close-only replay requires Close column. "
                f"Available columns: {reader.fieldnames}"
            )

        date_column = None
        for candidate in possible_date_columns:
            if candidate in fieldnames:
                date_column = candidate
                break

        if date_column is None:
            raise ValueError(
                "Close-only replay requires a date column. "
                f"Accepted date columns: {possible_date_columns}. "
                f"Available columns: {reader.fieldnames}"
            )

        for row in reader:
            price_rows.append(
                {
                    "Date": row[date_column],
                    "Close": float(row["Close"]),
                }
            )

    return run_risk_replay(
        price_rows=price_rows,
        config=config,
        trade_rule=trade_rule,
    )


def format_replay_output(replay_rows: list[dict]) -> list[dict]:
    """
    Format close-only replay rows for CSV export or terminal review.
    """

    formatted_rows: list[dict] = []

    for row in replay_rows:
        formatted_rows.append(
            {
                "date": row.get("date"),
                "asset": row.get("asset"),
                "close": row.get("close"),
                "entry_price": row.get("entry_price"),
                "anchor_price": row.get("anchor_price"),
                "position_tier": row.get("position_tier"),
                "stage": row.get("stage"),
                "risk_action": row.get("risk_action"),
                "trailing_started": row.get("trailing_started"),
                "return_pct": row.get("return_pct"),
                "peak_drawdown_pct": row.get("peak_drawdown_pct"),
                "active_stop_price": row.get("active_stop_price"),
                "trailing_stop_price": row.get("trailing_stop_price"),
                "effective_stop_price": row.get("effective_stop_price"),
                "profit_threshold_price": row.get("profit_threshold_price"),
                "next_add_trigger_price": row.get("next_add_trigger_price"),
                "updated_peak_price": row.get("updated_peak_price"),
            }
        )

    return formatted_rows


# ---------------------------------------------------------------------
# OHLC replay
# ---------------------------------------------------------------------


def run_risk_replay_ohlc(
    price_rows: list[dict],
    config: RiskBacktestConfig,
    trade_rule,
) -> list[dict]:
    """
    Run OHLC-based risk-management replay.

    Expected price_rows columns:
    - Date
    - Open
    - High
    - Low
    - Close

    Boundary:
    - This is not a full intraday backtest.
    - OHLC cannot know whether high or low happened first.
    - If Low touches effective stop, this function stops replay
      conservatively after that row.

    Important:
    - Replay starts from config.entry_date.
    """

    replay_rows: list[dict] = []

    current_tier = config.initial_position_tier
    peak_price = config.entry_price
    trailing_started = False

    anchor_price = config.anchor_price
    if anchor_price is None:
        anchor_price = config.entry_price

    # Only replay rows on or after entry_date.
    filtered_price_rows = [
        row for row in price_rows
        if str(row["Date"]) >= str(config.entry_date)
    ]

    if not filtered_price_rows:
        raise ValueError(
            f"No price rows found on or after entry_date={config.entry_date}"
        )

    for row in filtered_price_rows:
        date = row["Date"]

        open_price = float(row["Open"])
        high_price = float(row["High"])
        low_price = float(row["Low"])
        close_price = float(row["Close"])
        is_entry_date = str(date) == str(config.entry_date)

        # OHLC replay uses daily high to update peak.
        # This is more realistic than close-only replay,
        # but sequence remains unknown at daily resolution.
        updated_peak_price = max(peak_price, high_price)

        position_input = _build_position_input(
            asset=config.asset,
            current_price=close_price,
            entry_price=config.entry_price,
            anchor_price=anchor_price,
            position_tier=current_tier,
            peak_price=updated_peak_price,
            entry_type=config.entry_type,
            trailing_started=trailing_started,
        )

        result = evaluate_position_risk(
            position=position_input,
            rule=trade_rule,
        )

        risk_action = _get_attr(result, ["risk_action", "action"], None)
        stage = _get_attr(result, ["stage"], None)
        result_position_tier = _get_attr(result, ["position_tier"], None)
        # Close-entry replay rule for OHLC replay:
        # On the entry date, the position is assumed to be opened at the close.
        # Therefore, do not allow same-day close-based stop-out actions.
        risk_action_name = getattr(risk_action, "value", risk_action)

        if is_entry_date and str(risk_action_name).startswith("STOP_OUT"):
            risk_action = "HOLD"
            result_position_tier = current_tier


        output_tier = (
            result_position_tier
            if result_position_tier is not None
            else current_tier
        )

        effective_stop_price = _get_effective_stop_price(result)
        profit_threshold_price = _get_attr(result, ["profit_threshold_price"], None)
        output_peak_price = _get_updated_peak_price(result, updated_peak_price)

        intraday_stop_touched = False
        intraday_exit_price = None
        intraday_stop_type = None
        ohlc_warning = None

        if (
            not is_entry_date
            and effective_stop_price is not None
            and low_price <= float(effective_stop_price)
        ):
            intraday_stop_touched = True
            intraday_exit_price = effective_stop_price
            intraday_stop_type = _classify_intraday_stop_type(result)

        if (
            not is_entry_date
            and profit_threshold_price is not None
            and high_price >= float(profit_threshold_price)
            and effective_stop_price is not None
            and low_price <= float(effective_stop_price)
        ):
            ohlc_warning = "daily_ohlc_sequence_unknown"

        replay_rows.append(
            {
                "date": date,
                "asset": config.asset,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "entry_price": config.entry_price,
                "anchor_price": anchor_price,
                "position_tier": _enum_name(output_tier),
                "stage": _enum_name(stage),
                "risk_action": _enum_name(risk_action),
                "trailing_started": _get_attr(
                    result,
                    ["trailing_started"],
                    trailing_started,
                ),
                "return_pct": _get_attr(result, ["return_pct"], None),
                "peak_drawdown_pct": _get_attr(result, ["peak_drawdown_pct"], None),
                "active_stop_price": _get_attr(result, ["active_stop_price"], None),
                "trailing_stop_price": _get_attr(result, ["trailing_stop_price"], None),
                "effective_stop_price": effective_stop_price,
                "profit_threshold_price": profit_threshold_price,
                "next_add_trigger_price": _get_attr(result, ["next_add_trigger_price"], None),
                "updated_peak_price": output_peak_price,
                "intraday_stop_touched": intraday_stop_touched,
                "intraday_exit_price": intraday_exit_price,
                "intraday_stop_type": intraday_stop_type,
                "ohlc_warning": ohlc_warning,
            }
        )

        if result_position_tier is not None:
            current_tier = result_position_tier
        else:
            current_tier = _update_tier_from_action(current_tier, risk_action)

        peak_price = output_peak_price
        trailing_started = _get_attr(result, ["trailing_started"], trailing_started)

        # Conservative OHLC assumption:
        # if daily low touches effective stop, stop the replay.
        if intraday_stop_touched:
            break

        if current_tier == PositionTier.NONE:
            break

    return replay_rows


def run_risk_replay_ohlc_from_csv(
    csv_path: str,
    config: RiskBacktestConfig,
    trade_rule,
) -> list[dict]:
    """
    Load OHLC historical prices from CSV and run OHLC replay.

    Supported formats:

    1. Standard OHLC CSV:
       Date,Open,High,Low,Close

    2. yfinance multi-header CSV:
       Price,Close,High,Low,Open,Volume
       Ticker,SOXL,SOXL,SOXL,SOXL,SOXL
       Date,,,,,
       2015-01-02,...
    """

    price_rows: list[dict] = []

    with open(csv_path, mode="r", newline="", encoding="utf-8-sig") as file:
        raw_rows = list(csv.reader(file))

    if not raw_rows:
        raise ValueError(f"CSV file is empty: {csv_path}")

    first_row = raw_rows[0]

    # ------------------------------------------------------------
    # Case 1: yfinance multi-header format
    # ------------------------------------------------------------
    if first_row and first_row[0] == "Price":
        header = first_row

        required_columns = {"Close", "High", "Low", "Open"}
        missing_columns = required_columns - set(header)

        if missing_columns:
            raise ValueError(
                "OHLC replay requires yfinance columns: "
                f"{sorted(required_columns)}. "
                f"Missing columns: {sorted(missing_columns)}. "
                f"Available columns: {header}"
            )

        close_idx = header.index("Close")
        high_idx = header.index("High")
        low_idx = header.index("Low")
        open_idx = header.index("Open")

        # yfinance rows:
        # row 0 = Price header
        # row 1 = Ticker row
        # row 2 = Date row
        # row 3+ = actual price data
        for row in raw_rows[3:]:
            if not row or not row[0]:
                continue

            try:
                price_rows.append(
                    {
                        "Date": row[0],
                        "Open": float(row[open_idx]),
                        "High": float(row[high_idx]),
                        "Low": float(row[low_idx]),
                        "Close": float(row[close_idx]),
                    }
                )
            except (ValueError, IndexError) as exc:
                raise ValueError(
                    f"Invalid OHLC row in {csv_path}: {row}"
                ) from exc

        return run_risk_replay_ohlc(
            price_rows=price_rows,
            config=config,
            trade_rule=trade_rule,
        )

    # ------------------------------------------------------------
    # Case 2: standard CSV format
    # ------------------------------------------------------------
    required_price_columns = {"Open", "High", "Low", "Close"}
    possible_date_columns = [
        "Date",
        "date",
        "Datetime",
        "datetime",
        "Timestamp",
        "timestamp",
        "Unnamed: 0",
    ]

    header = first_row
    fieldnames = set(header)

    missing_price_columns = required_price_columns - fieldnames

    if missing_price_columns:
        raise ValueError(
            "OHLC replay requires price columns: "
            f"{sorted(required_price_columns)}. "
            f"Missing columns: {sorted(missing_price_columns)}. "
            f"Available columns: {header}"
        )

    date_column = None
    for candidate in possible_date_columns:
        if candidate in fieldnames:
            date_column = candidate
            break

    if date_column is None:
        raise ValueError(
            "OHLC replay requires a date column. "
            f"Accepted date columns: {possible_date_columns}. "
            f"Available columns: {header}"
        )

    date_idx = header.index(date_column)
    open_idx = header.index("Open")
    high_idx = header.index("High")
    low_idx = header.index("Low")
    close_idx = header.index("Close")

    for row in raw_rows[1:]:
        if not row or not row[date_idx]:
            continue

        try:
            price_rows.append(
                {
                    "Date": row[date_idx],
                    "Open": float(row[open_idx]),
                    "High": float(row[high_idx]),
                    "Low": float(row[low_idx]),
                    "Close": float(row[close_idx]),
                }
            )
        except (ValueError, IndexError) as exc:
            raise ValueError(
                f"Invalid OHLC row in {csv_path}: {row}"
            ) from exc

    return run_risk_replay_ohlc(
        price_rows=price_rows,
        config=config,
        trade_rule=trade_rule,
    )


def format_ohlc_replay_output(replay_rows: list[dict]) -> list[dict]:
    """
    Format OHLC replay rows for CSV export or terminal review.
    """

    formatted_rows: list[dict] = []

    for row in replay_rows:
        formatted_rows.append(
            {
                "date": row.get("date"),
                "asset": row.get("asset"),
                "open": row.get("open"),
                "high": row.get("high"),
                "low": row.get("low"),
                "close": row.get("close"),
                "entry_price": row.get("entry_price"),
                "anchor_price": row.get("anchor_price"),
                "position_tier": row.get("position_tier"),
                "stage": row.get("stage"),
                "risk_action": row.get("risk_action"),
                "trailing_started": row.get("trailing_started"),
                "return_pct": row.get("return_pct"),
                "peak_drawdown_pct": row.get("peak_drawdown_pct"),
                "active_stop_price": row.get("active_stop_price"),
                "trailing_stop_price": row.get("trailing_stop_price"),
                "effective_stop_price": row.get("effective_stop_price"),
                "profit_threshold_price": row.get("profit_threshold_price"),
                "next_add_trigger_price": row.get("next_add_trigger_price"),
                "updated_peak_price": row.get("updated_peak_price"),
                "intraday_stop_touched": row.get("intraday_stop_touched"),
                "intraday_exit_price": row.get("intraday_exit_price"),
                "intraday_stop_type": row.get("intraday_stop_type"),
                "ohlc_warning": row.get("ohlc_warning"),
            }
        )

    return formatted_rows