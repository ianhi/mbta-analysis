from __future__ import annotations

import pandas as pd

from ._util import direction_shorthand, to_min


def travel_time(
    df: pd.DataFrame, route: str | int, direction: str, start: str, end: str
):
    """
    Create a dataframe containing the actual travel times between two stops

    Parameters
    ----------
    df : DataFrame
    route : int or str
        The route number. For 1 digit routes it will be automatically prepended with 0s
    direction : str
        'Inbound' or 'Outbound', or shorthands 'in' or 'out'
    start : str
        The origin stop
    end : str
        The stop to end at

    Returns
    -------
    DataFrame
        A dataframe containing the time between the specified stops
    """
    route = str(route).zfill(2)
    direction = direction_shorthand(direction)
    fd = df.loc[route, direction]
    fd = fd[(fd["time_point_id"] == start) | (fd["time_point_id"] == end)]
    return fd.groupby("half_trip_id")["actual"].diff().dropna()


def plot_travel_times_by_chunked_departure(
    df: pd.DataFrame,
    quantiles: tuple[float, float] = (0.25, 0.75),
    *,
    ax=None,
    **kwargs
):
    """
    Plot the median travel time vs the departure time (chunked)

    Parameters
    ----------
    df : DataFrame
    ax : matplotlib axis, optional
    **kwargs:
        Pass on to plot call
    """
    import matplotlib.pyplot as plt

    if ax is None:
        ax = plt.gca()
    median = df.groupby("scheduled-chunked").median()
    max_ = df.groupby("scheduled-chunked").quantile(0.75)
    min_ = df.groupby("scheduled-chunked").quantile(0.25)
    ax.fill_between(median.index, to_min(min_), to_min(max_), alpha=0.2)
    ax.plot(median.index, to_min(median), marker=kwargs.pop("marker", "o"), **kwargs)
