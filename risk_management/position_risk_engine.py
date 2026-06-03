"""
Public-safe position risk-management engine.

This module converts position state and private rule configuration into
generic risk-management outputs.

It intentionally avoids hardcoding:
- real assets
- real position sizes
- staged reduction percentages
- private trading thresholds

Private parameters are loaded from config/trade_rules_config.csv through
risk_rule_loader.py. The config folder is ignored by Git.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from risk_management.risk_rule_loader import TradeRule


class PositionTier(str, Enum):
    """
    Generic position exposure tier.

    The mapping from real holding size to these tiers should remain private
    and should be handled under config/.
    """

    NONE = "NONE"
    LOW = "LOW"
    MID = "MID"
    HIGH = "HIGH"


class PositionStage(str, Enum):
    """
    Generic position management stage.
    """

    FLAT = "FLAT"
    WAIT_PRICE = "WAIT_PRICE"
    BUILD = "BUILD"
    ADD_BE = "ADD_BE"
    FULL_BE = "FULL_BE"
    POST_PROFIT_TRAIL = "POST_PROFIT_TRAIL"
    FINAL_TRAIL = "FINAL_TRAIL"
    CASH_HOLD = "CASH_HOLD"
    WATCH_NOT_ACTIVE = "WATCH_NOT_ACTIVE"


class RiskAction(str, Enum):
    """
    Generic risk-management action.

    Action names avoid exposing private position-size levels.
    """

    NO_POSITION = "NO_POSITION"
    WAIT_PRICE = "WAIT_PRICE"

    HOLD_LOW = "HOLD_LOW"
    HOLD_MID = "HOLD_MID"
    HOLD_HIGH = "HOLD_HIGH"

    ADD_TO_MID = "ADD_TO_MID"
    ADD_TO_HIGH = "ADD_TO_HIGH"

    REDUCE_TO_MID = "REDUCE_TO_MID"
    REDUCE_TO_LOW = "REDUCE_TO_LOW"

    EXIT_ALL = "EXIT_ALL"
    STOP_OUT = "STOP_OUT"
    STOP_OUT_BE = "STOP_OUT_BE"

    HOLD_CASH = "HOLD_CASH"
    WATCH_NOT_ACTIVE = "WATCH_NOT_ACTIVE"


@dataclass(frozen=True)
class PositionInput:
    """
    Current position state.

    position_tier should be generated from a private local mapping.
    Public code does not define real position-size thresholds.

    trailing_started is not provided as input.
    It is automatically determined by:

        updated_peak_price >= profit_threshold_price
    """

    asset: str
    position_tier: PositionTier
    entry_price: float | None
    anchor_price: float | None
    current_price: float | None
    peak_price: float | None
    entry_type: str = ""


@dataclass(frozen=True)
class RiskOutput:
    """
    Risk-management calculation result.
    """

    asset: str
    stage: PositionStage
    action: RiskAction
    trailing_started: bool
    return_pct: float | None
    peak_drawdown_pct: float | None
    active_stop_price: float | None
    trailing_stop_price: float | None
    profit_threshold_price: float | None
    next_add_trigger_price: float | None
    updated_peak_price: float | None


def _has_missing_price(*values: float | None) -> bool:
    """
    Return True if any required price input is missing.
    """
    return any(value is None for value in values)


def calculate_return_pct(
    entry_price: float | None,
    current_price: float | None,
) -> float | None:
    """
    Calculate current return from entry price.

    Formula:
        current_price / entry_price - 1
    """
    if _has_missing_price(entry_price, current_price):
        return None

    if entry_price == 0:
        return None

    return current_price / entry_price - 1


def calculate_updated_peak_price(
    current_price: float | None,
    peak_price: float | None,
) -> float | None:
    """
    Update peak price using the latest current price.

    If no previous peak exists, current price becomes the first peak.

    Note:
        This function only calculates the updated peak price.
        It does not write the value back to any CSV, spreadsheet, or database.
    """
    if current_price is None:
        return peak_price

    if peak_price is None:
        return current_price

    return max(current_price, peak_price)


def calculate_peak_drawdown_pct(
    current_price: float | None,
    peak_price: float | None,
) -> float | None:
    """
    Calculate drawdown from the current peak.

    The result is negative when current price is below peak price.

    Example:
        current_price = 94
        peak_price = 100
        peak_drawdown_pct = -0.06

    This matches the private rule config where trailing drawdown thresholds
    are also stored as negative values.
    """
    if _has_missing_price(current_price, peak_price):
        return None

    if peak_price == 0:
        return None

    return current_price / peak_price - 1


def calculate_active_stop_price(
    position_tier: PositionTier,
    entry_price: float | None,
    rule: TradeRule,
) -> float | None:
    """
    Calculate active stop price before trailing starts.

    Before trailing starts:
    - LOW tier uses initial stop loss.
    - MID and HIGH tiers use breakeven-style protection.
    """
    if entry_price is None:
        return None

    if position_tier == PositionTier.LOW:
        return entry_price * (1 + rule.initial_stop_loss)

    if position_tier in {PositionTier.MID, PositionTier.HIGH}:
        return entry_price

    return None


def calculate_profit_threshold_price(
    entry_price: float | None,
    rule: TradeRule,
) -> float | None:
    """
    Calculate the price level where trailing logic may begin.

    Formula:
        entry_price * (1 + profit_trigger)
    """
    if entry_price is None:
        return None

    return entry_price * (1 + rule.profit_trigger)


def determine_trailing_started(
    peak_price: float | None,
    profit_threshold_price: float | None,
) -> bool:
    """
    Determine whether trailing logic should start.

    Trailing starts once the updated peak price reaches or exceeds the
    profit threshold price.

    Formula:
        updated_peak_price >= profit_threshold_price
    """
    if peak_price is None or profit_threshold_price is None:
        return False

    return peak_price >= profit_threshold_price


def calculate_next_add_trigger_price(
    position_tier: PositionTier,
    anchor_price: float | None,
    rule: TradeRule,
) -> float | None:
    """
    Calculate the next add trigger using generic position tiers.

    Real position-size mapping remains private.
    """
    if anchor_price is None:
        return None

    if position_tier == PositionTier.LOW:
        return anchor_price * (1 + rule.add_step)

    if position_tier == PositionTier.MID:
        return anchor_price * (1 + rule.add_step * 2)

    if position_tier == PositionTier.HIGH:
        return None

    return None


def calculate_trailing_stop_price(
    position_tier: PositionTier,
    peak_price: float | None,
    trailing_started: bool,
    rule: TradeRule,
) -> float | None:
    """
    Calculate trailing stop price using generic tier-based logic.

    Before trailing starts:
    - No peak-based trailing stop is applied.
    - LOW / MID / HIGH use active stop logic instead.

    After trailing starts:
    - HIGH / MID / LOW use peak-based trailing logic.

    The trailing rule values are expected to be negative values in config.
    """
    if not trailing_started:
        return None

    if peak_price is None:
        return None

    if position_tier == PositionTier.HIGH:
        return peak_price * (1 + rule.trail_high_to_mid)

    if position_tier == PositionTier.MID:
        return peak_price * (1 + rule.trail_mid_to_low)

    if position_tier == PositionTier.LOW:
        return peak_price * (1 + rule.trail_low_exit)

    return None


def determine_stage(
    position: PositionInput,
    trailing_started: bool,
    rule: TradeRule,
) -> PositionStage:
    """
    Determine current risk-management stage.

    This function uses generic position tiers instead of real position sizes.
    """
    asset = position.asset.strip().upper()

    if asset == "":
        return PositionStage.WAIT_PRICE

    if asset == "CASH":
        return PositionStage.CASH_HOLD

    if rule.status != "TRADE_READY":
        return PositionStage.WATCH_NOT_ACTIVE

    if position.position_tier == PositionTier.NONE:
        return PositionStage.FLAT

    if position.entry_price is None or position.current_price is None:
        return PositionStage.WAIT_PRICE

    if trailing_started:
        if position.position_tier == PositionTier.LOW:
            return PositionStage.FINAL_TRAIL

        return PositionStage.POST_PROFIT_TRAIL

    if position.position_tier == PositionTier.HIGH:
        return PositionStage.FULL_BE

    if position.position_tier == PositionTier.MID:
        return PositionStage.ADD_BE

    return PositionStage.BUILD


def generate_risk_action(
    position: PositionInput,
    stage: PositionStage,
    trailing_started: bool,
    current_price: float | None,
    active_stop_price: float | None,
    next_add_trigger_price: float | None,
    peak_drawdown_pct: float | None,
    rule: TradeRule,
) -> RiskAction:
    """
    Generate generic risk-management action.

    Before trailing starts:
    - LOW uses initial stop and next-add trigger.
    - MID uses breakeven stop and next-add trigger.
    - HIGH uses breakeven stop and hold logic.

    After trailing starts:
    - HIGH / MID / LOW use negative peak-drawdown logic.
    """
    if stage == PositionStage.CASH_HOLD:
        return RiskAction.HOLD_CASH

    if stage == PositionStage.WATCH_NOT_ACTIVE:
        return RiskAction.WATCH_NOT_ACTIVE

    if stage == PositionStage.FLAT:
        return RiskAction.NO_POSITION

    if stage == PositionStage.WAIT_PRICE:
        return RiskAction.WAIT_PRICE

    if current_price is None:
        return RiskAction.WAIT_PRICE

    # Before trailing starts: use SL / BE / add-trigger logic.
    if not trailing_started:
        if position.position_tier == PositionTier.LOW:
            if active_stop_price is not None and current_price <= active_stop_price:
                return RiskAction.STOP_OUT

            if (
                next_add_trigger_price is not None
                and current_price >= next_add_trigger_price
            ):
                return RiskAction.ADD_TO_MID

            return RiskAction.HOLD_LOW

        if position.position_tier == PositionTier.MID:
            if active_stop_price is not None and current_price <= active_stop_price:
                return RiskAction.STOP_OUT_BE

            if (
                next_add_trigger_price is not None
                and current_price >= next_add_trigger_price
            ):
                return RiskAction.ADD_TO_HIGH

            return RiskAction.HOLD_MID

        if position.position_tier == PositionTier.HIGH:
            if active_stop_price is not None and current_price <= active_stop_price:
                return RiskAction.STOP_OUT_BE

            return RiskAction.HOLD_HIGH

    # After trailing starts: use peak-based trailing logic.
    if trailing_started:
        if peak_drawdown_pct is None:
            return RiskAction.WAIT_PRICE

        if position.position_tier == PositionTier.HIGH:
            if peak_drawdown_pct <= rule.trail_high_to_mid:
                return RiskAction.REDUCE_TO_MID

            return RiskAction.HOLD_HIGH

        if position.position_tier == PositionTier.MID:
            if peak_drawdown_pct <= rule.trail_mid_to_low:
                return RiskAction.REDUCE_TO_LOW

            return RiskAction.HOLD_MID

        if position.position_tier == PositionTier.LOW:
            if peak_drawdown_pct <= rule.trail_low_exit:
                return RiskAction.EXIT_ALL

            return RiskAction.HOLD_LOW

    return RiskAction.WAIT_PRICE


def evaluate_position_risk(
    position: PositionInput,
    rule: TradeRule,
) -> RiskOutput:
    """
    Evaluate one position using public-safe risk-management logic.

    Main flow:
    1. Update peak price.
    2. Calculate return.
    3. Calculate negative peak drawdown.
    4. Calculate active stop.
    5. Calculate profit threshold.
    6. Determine whether trailing has started.
    7. Calculate trailing stop if trailing has started.
    8. Calculate next add trigger.
    9. Determine stage.
    10. Generate action.
    """
    updated_peak_price = calculate_updated_peak_price(
        current_price=position.current_price,
        peak_price=position.peak_price,
    )

    return_pct = calculate_return_pct(
        entry_price=position.entry_price,
        current_price=position.current_price,
    )

    peak_drawdown_pct = calculate_peak_drawdown_pct(
        current_price=position.current_price,
        peak_price=updated_peak_price,
    )

    active_stop_price = calculate_active_stop_price(
        position_tier=position.position_tier,
        entry_price=position.entry_price,
        rule=rule,
    )

    profit_threshold_price = calculate_profit_threshold_price(
        entry_price=position.entry_price,
        rule=rule,
    )

    trailing_started = determine_trailing_started(
        peak_price=updated_peak_price,
        profit_threshold_price=profit_threshold_price,
    )

    trailing_stop_price = calculate_trailing_stop_price(
        position_tier=position.position_tier,
        peak_price=updated_peak_price,
        trailing_started=trailing_started,
        rule=rule,
    )

    next_add_trigger_price = calculate_next_add_trigger_price(
        position_tier=position.position_tier,
        anchor_price=position.anchor_price,
        rule=rule,
    )

    stage = determine_stage(
        position=position,
        trailing_started=trailing_started,
        rule=rule,
    )

    action = generate_risk_action(
        position=position,
        stage=stage,
        trailing_started=trailing_started,
        current_price=position.current_price,
        active_stop_price=active_stop_price,
        next_add_trigger_price=next_add_trigger_price,
        peak_drawdown_pct=peak_drawdown_pct,
        rule=rule,
    )

    return RiskOutput(
        asset=position.asset.upper().strip(),
        stage=stage,
        action=action,
        trailing_started=trailing_started,
        return_pct=return_pct,
        peak_drawdown_pct=peak_drawdown_pct,
        active_stop_price=active_stop_price,
        trailing_stop_price=trailing_stop_price,
        profit_threshold_price=profit_threshold_price,
        next_add_trigger_price=next_add_trigger_price,
        updated_peak_price=updated_peak_price,
    )