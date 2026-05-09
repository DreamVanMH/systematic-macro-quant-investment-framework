import pandas as pd


def get_latest_close(market_data, ticker):
    """
    Get the latest closing price for one ticker.
    """

    if ticker not in market_data:
        return None

    df = market_data[ticker]

    if df.empty:
        return None

    latest_close = df["Close"].iloc[-1]

    return latest_close


def get_daily_change_pct(market_data, ticker):
    """
    Calculate latest daily percentage change for one ticker.
    """

    if ticker not in market_data:
        return None

    df = market_data[ticker]

    if len(df) < 2:
        return None

    latest_close = float(df["Close"].iloc[-1])
    previous_close = float(df["Close"].iloc[-2])

    daily_change_pct = ((latest_close - previous_close) / previous_close) * 100

    return daily_change_pct


def generate_macro_snapshot(market_data):
    """
    Generate a simple macro monitoring snapshot.
    """

    macro_universe = {
        "VIX": "VIX",
        "TNX": "TNX",
        "DXY Proxy": "UUP",
        "USDCAD": "CAD=X",
        "USDCNY": "USDCNY=X",
        "BTC": "BTC-USD",
        "GLD": "GLD",
        "DBC": "DBC",
        "BNO": "BNO",
        "QQQ": "QQQ",
        "TQQQ": "TQQQ",
        "SQQQ": "SQQQ"
    }

    snapshot = []

    for indicator, ticker in macro_universe.items():

        latest_close = get_latest_close(market_data, ticker)
        daily_change_pct = get_daily_change_pct(market_data, ticker)

        snapshot.append({
            "Indicator": indicator,
            "Ticker": ticker,
            "Latest Close": latest_close,
            "Daily Change %": daily_change_pct
        })

    snapshot_df = pd.DataFrame(snapshot)

    return snapshot_df