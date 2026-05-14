import pandas as pd

from config.macro_rules_private import (
    VIX_RISK_ON_LEVEL,
    VIX_PANIC_LEVEL,
    REGIME_RULES,
    MACRO_SCORE_RULES,
    REGIME_NAMES,
    TRADE_BIAS_MAP,
)


def calculate_macro_scores(row: pd.Series) -> dict:
    """
    Calculate macro environment scores for one row of macro data.

    The macro layer acts as an environment filter only.
    It does not directly determine the final tradable asset.
    """

    scores = {
        "risk_on_score": 0,
        "risk_off_score": 0,
        "inflation_score": 0,
        "rate_pressure_score": 0,
        "usd_liquidity_score": 0,
    }

    def apply_score(score_dict: dict):
        for score_name, value in score_dict.items():
            if score_name in scores:
                scores[score_name] += value

    # VIX level rule
    vix_level = row.get("VIX", 0)

    if vix_level < VIX_RISK_ON_LEVEL:
        apply_score(MACRO_SCORE_RULES.get("VIX", {}).get("low", {}))
    elif vix_level > VIX_PANIC_LEVEL:
        apply_score(MACRO_SCORE_RULES.get("VIX", {}).get("high", {}))
    else:
        apply_score(MACRO_SCORE_RULES.get("VIX", {}).get("mid", {}))

    # Cross-asset score rules
    for indicator, rule in MACRO_SCORE_RULES.items():
        if indicator == "VIX":
            continue

        value = row.get(indicator, 0)

        if value > 0:
            apply_score(rule.get("positive", {}))
        elif value < 0:
            apply_score(rule.get("negative", {}))

    return scores


def classify_regime(vix_level: float, scores: dict) -> str:
    """
    Classify macro regime using cumulative score dominance.

    Priority:
    1. Panic Risk-off
    2. Inflation Risk-off
    3. Liquidity Risk-on
    4. Liquidity Tightening
    """

    risk_on = scores["risk_on_score"]
    risk_off = scores["risk_off_score"]
    inflation = scores["inflation_score"]

    inflation_buffer = REGIME_RULES["inflation_dominance_buffer"]
    risk_on_buffer = REGIME_RULES["risk_on_dominance_buffer"]

    # 1. Panic Risk-off
    # VIX panic must be confirmed by risk-off dominance.
    if vix_level > VIX_PANIC_LEVEL and risk_off >= risk_on:
        return REGIME_NAMES["panic_risk_off"]

    # 2. Inflation Risk-off
    # Inflation must be dominant, not merely positive.
    if (
        inflation >= risk_on + inflation_buffer
        and inflation >= risk_off + inflation_buffer
    ):
        return REGIME_NAMES["inflation_risk_off"]

    # 3. Liquidity Risk-on
    # Risk-on must clearly dominate both risk-off and inflation pressure.
    if (
        risk_on >= risk_off + risk_on_buffer
        and risk_on >= inflation + risk_on_buffer
    ):
        return REGIME_NAMES["liquidity_risk_on"]

    # 4. Default
    return REGIME_NAMES["liquidity_tightening"]


def get_trade_bias(regime: str) -> str:
    """
    Map macro regime to broad trade bias.

    Final tradable asset selection should still be handled by
    dashboard relative strength and allocation logic.
    """

    return TRADE_BIAS_MAP.get(
        regime,
        TRADE_BIAS_MAP[REGIME_NAMES["liquidity_tightening"]],
    )