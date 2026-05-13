import pandas as pd

from scripts.regime_engine import (
    calculate_macro_scores,
    classify_regime,
    get_trade_bias,
)


def get_latest_close(market_data, ticker):
    """
    Get latest closing price for one ticker.
    """

    if ticker not in market_data:
        return None

    df = market_data[ticker]

    if df.empty:
        return None

    return float(df["Close"].iloc[-1])


def get_daily_change_pct(market_data, ticker):
    """
    Calculate latest daily percentage change.
    """

    if ticker not in market_data:
        return None

    df = market_data[ticker]

    if len(df) < 2:
        return None

    latest_close = float(df["Close"].iloc[-1])
    previous_close = float(df["Close"].iloc[-2])

    return ((latest_close - previous_close) / previous_close) * 100


def generate_macro_snapshot(market_data):
    """
    Generate macro environment filter snapshot.

    This layer provides:
    - macro environment filtering
    - regime classification
    - broad trade bias

    It does NOT determine the final tradable asset.
    """

    macro_universe = {
        "VIX": "VIX",
        "DXY": "UUP",
        "TNX": "TNX",
        "US02Y": "US02Y",
        "NQ1": "NQ1",
        "QQQ": "QQQ",
        "BNO": "BNO",
        "DBC": "DBC",
        "GLD": "GLD",
        "USDCNY": "USDCNY=X",
        "USDCAD": "CAD=X",
        "BTC": "BTC-USD",
        "SHY": "SHY",
    }

    snapshot_rows = []

    score_input = {}

    for indicator, ticker in macro_universe.items():

        latest_close = get_latest_close(market_data, ticker)
        daily_change_pct = get_daily_change_pct(market_data, ticker)

        if indicator == "VIX":
            score_input[indicator] = latest_close or 0
        else:
            score_input[indicator] = daily_change_pct or 0

        snapshot_rows.append({
            "Indicator": indicator,
            "Ticker": ticker,
            "Latest Close": latest_close,
            "Daily Change %": daily_change_pct,
        })

    snapshot_df = pd.DataFrame(snapshot_rows)

    score_series = pd.Series(score_input)

    scores = calculate_macro_scores(score_series)

    regime = classify_regime(
        vix_level=score_input.get("VIX", 0),
        scores=scores,
    )

    trade_bias = get_trade_bias(regime)

    summary_df = pd.DataFrame([
        {
            "Macro Regime": regime,
            "Trade Bias": trade_bias,
            **scores,
        }
    ])

    return {
        "snapshot": snapshot_df,
        "summary": summary_df,
    }