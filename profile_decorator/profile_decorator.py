import datetime
import fnmatch
import os
import site
import tracemalloc
import typing
from functools import wraps
from pathlib import Path

import psutil

from .report import report

site_packages_path = str(Path(site.getsitepackages()[0]).parent.absolute())


def init():
    """Starts tracing Python memory allocations"""
    tracemalloc.start()


def profile_memory(f):
    """Reports line-level memory usage statistics

    Uses `tracemalloc` to get memory stats using `tracemalloc.StatisticDiff`
    on a line-by-line level to report total and difference of allocated memory

    See https://docs.python.org/3/library/tracemalloc.html#tracemalloc.StatisticDiff  # noqa: E501

    Parameters
    ----------
    f : Callable
        The function being wrapped

    Returns
    -------
    Callable
        The wrapped function
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        profile = {}
        profile["function"] = f.__name__
        profile["file"] = f.__globals__["__file__"]
        profile["filename"] = os.path.basename(profile["file"])
        profile["start_time"] = datetime.datetime.isoformat(
            datetime.datetime.now()
        )
        profile["uss_memory_before"] = psutil.Process().memory_full_info().uss
        snapshot_before = tracemalloc.take_snapshot()
        result = f(*args, **kwds)
        profile["end_time"] = datetime.datetime.isoformat(
            datetime.datetime.now()
        )
        snapshot_after = tracemalloc.take_snapshot()
        profile["uss_memory_after"] = psutil.Process().memory_full_info().uss
        snapshot_after = snapshot_after.filter_traces(
            (
                tracemalloc.Filter(False, __file__),
                tracemalloc.Filter(False, tracemalloc.__file__),
            )
        )
        lines = []
        comparison: typing.List[
            tracemalloc.StatisticDiff
        ] = snapshot_after.compare_to(snapshot_before, "lineno")
        for stat_diff in comparison:
            frames: tracemalloc.Frame = stat_diff.traceback._frames
            for frame in frames:
                filename = frame[0]
                if not filename.startswith(
                    site_packages_path
                ) and not fnmatch.fnmatch(filename, "<*>"):
                    lines.append(
                        {
                            "filename": filename,
                            "lineno": frame[1],
                            "size": stat_diff.size,
                            "size_diff": stat_diff.size_diff,
                        }
                    )
        profile["lines"] = lines
        report(profile)
        return result

    return wrapper
