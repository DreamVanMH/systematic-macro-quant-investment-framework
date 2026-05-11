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
    Calculate macro scores for one row of macro daily returns.
    Score weights are loaded from private macro rule config.
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
            scores[score_name] += value

    # VIX level rule
    vix_level = row.get("VIX", 0)

    if vix_level < VIX_RISK_ON_LEVEL:
        scores["risk_on_score"] += 1
    elif vix_level > VIX_PANIC_LEVEL:
        scores["risk_off_score"] += 1

    # Cross-asset score rules
    for indicator, rule in MACRO_SCORE_RULES.items():
        value = row.get(indicator, 0)

        if value > 0:
            apply_score(rule.get("positive", {}))
        elif value < 0:
            apply_score(rule.get("negative", {}))

    return scores


def classify_regime(vix_level: float, scores: dict) -> str:
    """
    Classify macro regime using private regime parameters.
    """

    risk_on = scores["risk_on_score"]
    risk_off = scores["risk_off_score"]
    inflation = scores["inflation_score"]
    rate_pressure = scores["rate_pressure_score"]
    usd_liquidity = scores["usd_liquidity_score"]

    inflation_buffer = REGIME_RULES["inflation_buffer"]
    macro_pressure_buffer = REGIME_RULES["macro_pressure_buffer"]
    risk_on_buffer = REGIME_RULES["risk_on_buffer"]
    supported_risk_on_threshold = REGIME_RULES["supported_risk_on_threshold"]

    if (
        vix_level > VIX_PANIC_LEVEL
        and risk_off >= max(risk_on, inflation, rate_pressure, usd_liquidity)
    ):
        return REGIME_NAMES["panic_risk_off"]

    if inflation >= max(risk_on, risk_off, rate_pressure, usd_liquidity) + inflation_buffer:
        return REGIME_NAMES["inflation_pressure"]

    if (
        risk_off >= max(risk_on, inflation, rate_pressure, usd_liquidity) + macro_pressure_buffer
        and vix_level <= VIX_PANIC_LEVEL
    ):
        return REGIME_NAMES["macro_pressure"]

    if risk_on >= max(risk_off, inflation, rate_pressure, usd_liquidity) + risk_on_buffer:
        return REGIME_NAMES["liquidity_risk_on"]

    if risk_on >= supported_risk_on_threshold:
        return REGIME_NAMES["supported_risk_on"]

    return REGIME_NAMES["mixed"]


def get_trade_bias(regime: str) -> str:
    """
    Map macro regime to trade bias using private mapping.
    """

    return TRADE_BIAS_MAP.get(
        regime,
        TRADE_BIAS_MAP[REGIME_NAMES["mixed"]]
    )