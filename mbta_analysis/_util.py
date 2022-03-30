from __future__ import annotations

__all__ = [
    "to_min",
    "direction_shorthand",
]
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def to_min(series: pd.Series) -> pd.Series:
    """
    Convert a series of timedeltas to a series of minutes
    """
    return series.apply(lambda x: x.total_seconds() / 60)


def direction_shorthand(direction: str):
    """
    Process direction shorthand (e.g. out-> Outbound)
    """
    if direction.lower() in ["out", "outbound"]:
        return "Outbound"
    elif direction.lower() in ["in", "inbound"]:
        return "Inbound"
