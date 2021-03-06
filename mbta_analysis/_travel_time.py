from __future__ import annotations

import numpy as np
import pandas as pd

from ._util import direction_shorthand, to_min


def travel_time(
    df: pd.DataFrame,
    routes: str | int | list[str | int],
    stops: tuple[str] | list[tuple[str]],
    direction: str = None,
    dropna: bool = True,
):
    """
    Create a dataframe containing the actual travel times between two stops

    Parameters
    ----------
    df : DataFrame
    route : int or str or list thereof
        The route number. For 1 digit routes it will be automatically prepended with 0s
    stops : (str, str) or list of (str, str)
        The origin and end stops respectively. If multiple routes are given then there
        must be an equal number of starts and ends
    direction : str, optional
        'Inbound' or 'Outbound', or shorthands 'in' or 'out'. If not given both
        directions will be computed.
    dropna : bool, default True
        Whether to call dropna

    Returns
    -------
    DataFrame
        A dataframe containing the time between the specified stops
    """
    routes = [str(r).zfill(2) for r in np.atleast_1d(routes)]
    stops_ = np.atleast_2d(stops)  # redefine to appease mypy
    if stops_.shape[1] != 2 or stops_.shape[0] != len(routes):
        raise ValueError(
            "Invalid shape for stops. Must have shape "
            "(N, 2) where N is the number of routes"
        )

    if direction is not None:
        direction = direction_shorthand(direction)
        fd = df.loc[routes, direction]
    else:
        fd = df.loc[routes]
    fd = fd[fd["time_point_id"].isin(stops_.ravel())]
    out = fd.groupby("half_trip_id")["actual"].diff()
    if dropna:
        return out.dropna()
    return out


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
    max_ = df.groupby("scheduled-chunked").quantile(max(quantiles))
    min_ = df.groupby("scheduled-chunked").quantile(min(quantiles))
    ax.fill_between(median.index, to_min(min_), to_min(max_), alpha=0.2)
    ax.plot(median.index, to_min(median), marker=kwargs.pop("marker", "o"), **kwargs)
