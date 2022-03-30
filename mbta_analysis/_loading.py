from __future__ import annotations

__all__ = [
    "load_months",
]
from os import PathLike

import numpy as np
import pandas as pd


def load_months(fnames: PathLike | list[PathLike]):
    """
    Load and process a month's csv - setting up approriate multiindex etc.

    Note
    ----
    At the end of the month for routes after midnight the service date
    will be the previous day, and the schedulded time will +1 day.
    that's where the 25.5 in the scheduled-chunked index come from
    """
    df = pd.concat([pd.read_csv(f) for f in np.atleast_1d(fnames)])
    df["actual"] = pd.to_datetime(df["actual"])
    df["scheduled"] = pd.to_datetime(df["scheduled"])
    df["service_date"] = pd.to_datetime(df["service_date"])
    date_rng = pd.date_range("1900-01-01 0:00:00", periods=52, freq="30min")
    labels = date_rng[1:]

    df["scheduled-chunked"] = pd.cut(
        df["scheduled"], bins=date_rng, labels=labels, right=False
    ).apply(lambda x: (x.day - 1) * 24 + x.hour + x.minute / 60)
    multi_index_cols = ["route_id", "direction_id", "service_date", "scheduled-chunked"]
    df = df.set_index(pd.MultiIndex.from_frame(df[multi_index_cols]))
    df = df.drop(multi_index_cols, axis="columns").sort_index()
    return df
