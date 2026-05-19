"""
Market structure public wrapper.

The actual market-structure rules, private group mapping,
thresholds, and classification logic are stored in:

config/market_structure_private.py

This file only exposes a clean interface for scripts and dashboard export.
"""

from config.market_structure_private import (
    generate_market_structure_snapshot,
    build_market_structure_rows_from_market_data,
)


def build_market_structure_rows(market_data):
    """
    Build market-structure rows from standardized market_data.
    """

    return build_market_structure_rows_from_market_data(market_data)


def run_market_structure(asset_rows, vix_level=None):
    """
    Run market-structure calculation using private rules.
    """

    return generate_market_structure_snapshot(
        asset_rows=asset_rows,
        vix_level=vix_level,
    )