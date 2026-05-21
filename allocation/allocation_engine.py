"""
Allocation public wrapper.

Private allocation rules are stored in:

config/allocation_private.py

This file only exposes a clean interface for scripts and dashboard export.
"""

from config.allocation_private import (
    generate_allocation_snapshot,
    generate_category_scores_from_group_summary,
)


def build_category_scores(group_summary):
    """
    Build allocation category scores using private rules.
    """

    return generate_category_scores_from_group_summary(
        group_summary=group_summary,
    )


def run_allocation(category_scores, macro_regime, vix_level=None):
    """
    Run allocation calculation using private rules.
    """

    return generate_allocation_snapshot(
        category_scores=category_scores,
        macro_regime=macro_regime,
        vix_level=vix_level,
    )