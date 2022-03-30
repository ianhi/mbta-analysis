try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
__author__ = "Ian Hunt-Isaak"
__email__ = "ianhuntisaak@gmail.com"

from ._loading import load_month
from ._travel_time import plot_travel_times_by_chunked_departure, travel_time

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "travel_time",
    "plot_travel_times_by_chunked_departure",
    "load_month",
]
