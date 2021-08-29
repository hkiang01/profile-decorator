import datetime
import tracemalloc
import typing
from functools import wraps


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
        profile["start_time"] = datetime.datetime.isoformat(
            datetime.datetime.now()
        )
        tracemalloc.start()
        snapshot_before = tracemalloc.take_snapshot()
        result = f(*args, **kwds)
        snapshot_after = tracemalloc.take_snapshot()
        tracemalloc.stop()
        profile["end_time"] = datetime.datetime.isoformat(
            datetime.datetime.now()
        )
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
                lines.append(
                    {
                        "filename": frame[0],
                        "lineno": frame[1],
                        "size": stat_diff.size,
                        "size_diff": stat_diff.size_diff,
                    }
                )
        profile["lines"] = lines
        return result

    return wrapper
