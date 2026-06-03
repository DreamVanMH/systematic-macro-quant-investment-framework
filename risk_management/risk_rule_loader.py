"""
Load private trade risk-management rules.

The real configuration file is expected to stay under:

    config/trade_rules_config.csv

The config folder is ignored by Git, so private assets, position rules,
risk thresholds, and strategy parameters are not committed to the public
repository.

This module contains only public-safe loading logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


DEFAULT_CONFIG_PATH = Path("config/trade_rules_config.csv")


REQUIRED_COLUMNS = [
    "asset",
    "status",
    "rule_profile",
    "add_step",
    "initial_stop_loss",
    "be_trigger",
    "profit_trigger",
    "early_protection_dd",
    "trail_high_to_mid",
    "trail_mid_to_low",
    "trail_low_exit",
    "asset_class",
    "category",
    "theme",
]


@dataclass(frozen=True)
class TradeRule:
    """
    Risk-management configuration for one tradable asset.

    Field names are intentionally generic and do not expose private position
    sizing rules, staged reduction details, or live trading parameters.
    """

    asset: str
    status: str
    rule_profile: str
    add_step: float
    initial_stop_loss: float
    be_trigger: float
    profit_trigger: float
    early_protection_dd: float
    trail_high_to_mid: float
    trail_mid_to_low: float
    trail_low_exit: float
    asset_class: str
    category: str
    theme: str


def _normalize_column_name(column_name: str) -> str:
    """
    Normalize config column names into Python-friendly names.

    The private config file should already use public-safe column names.
    This function only handles basic formatting differences.
    """
    return (
        str(column_name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("%", "")
        .replace("__", "_")
    )


def _to_float(value, default: float = 0.0) -> float:
    """
    Convert a config value into float.

    Supports:
    - numeric values
    - percentage strings
    - blank or missing values
    """
    if pd.isna(value):
        return default

    if isinstance(value, str):
        cleaned = value.strip()

        if cleaned == "":
            return default

        if cleaned.endswith("%"):
            return float(cleaned.replace("%", "")) / 100

        return float(cleaned)

    return float(value)


def _to_text(value, default: str = "") -> str:
    """
    Convert a config value into clean text.
    """
    if pd.isna(value):
        return default

    return str(value).strip()


def load_trade_rules(config_path: Path = DEFAULT_CONFIG_PATH) -> pd.DataFrame:
    """
    Load the private trade rules config CSV.

    Returns:
        A DataFrame indexed by asset.
    """
    if not config_path.exists():
        raise FileNotFoundError(
            f"Trade rules config not found: {config_path}\n"
            "Please place the private config file under config/."
        )

    rules_df = pd.read_csv(config_path)

    rules_df.columns = [_normalize_column_name(col) for col in rules_df.columns]

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in rules_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "The private trade rules config is missing required columns: "
            f"{missing_columns}"
        )

    rules_df["asset"] = (
        rules_df["asset"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    rules_df = rules_df.set_index("asset", drop=False)

    return rules_df


def get_trade_rule(asset: str, config_path: Path = DEFAULT_CONFIG_PATH) -> TradeRule:
    """
    Return trade rule configuration for one asset.

    The asset value should come from private config or private runtime input.
    No real asset example is hardcoded in this public module.
    """
    requested_asset = asset.upper().strip()

    rules_df = load_trade_rules(config_path)

    if requested_asset not in rules_df.index:
        raise KeyError("No trade rule found for the requested asset.")

    row = rules_df.loc[requested_asset]

    return TradeRule(
        asset=_to_text(row["asset"]).upper(),
        status=_to_text(row["status"]).upper(),
        rule_profile=_to_text(row["rule_profile"]),
        add_step=_to_float(row["add_step"]),
        initial_stop_loss=_to_float(row["initial_stop_loss"]),
        be_trigger=_to_float(row["be_trigger"]),
        profit_trigger=_to_float(row["profit_trigger"]),
        early_protection_dd=_to_float(row["early_protection_dd"]),
        trail_high_to_mid=_to_float(row["trail_high_to_mid"]),
        trail_mid_to_low=_to_float(row["trail_mid_to_low"]),
        trail_low_exit=_to_float(row["trail_low_exit"]),
        asset_class=_to_text(row["asset_class"]),
        category=_to_text(row["category"]),
        theme=_to_text(row["theme"]),
    )


def get_active_trade_rules(config_path: Path = DEFAULT_CONFIG_PATH) -> list[TradeRule]:
    """
    Return all active trade rules.

    A rule is considered active when its status is marked as trade-ready in the
    private config file.
    """
    rules_df = load_trade_rules(config_path)

    active_rules: list[TradeRule] = []

    for asset in rules_df.index:
        rule = get_trade_rule(asset, config_path)

        if rule.status == "TRADE_READY":
            active_rules.append(rule)

    return active_rules