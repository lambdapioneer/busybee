"""This file provides methods to generate the strings that are output
during the BusyBee execution."""

import math
import time


def _relative_time_string(time_seconds, no_ms=False):
    """Converts the given `time_seconds` into a relative, human-readable
    string representation.

    Args:
        time_seconds (int or float): The relative time to convert
        no_ms (bool): If set the `999ms` style representation is not chosen

    Returns:
        String: The string representation is chosen on the value of
                seconds to be either of the form `999ms`, `99.9s`,
                `59:59m`, or `99:59:59h`. If `None` is supplied, `-`
                is returned.
    """
    if time_seconds == None:
        return "-"

    milliseconds = int(time_seconds * 1000.0)
    if abs(milliseconds) < 1000 and not no_ms:
        return "%dms" % milliseconds

    seconds = time_seconds
    if abs(seconds) < 100.0:
        return "%.1fs" % (seconds)

    minutes = int(seconds / 60)
    seconds = abs(seconds - minutes * 60)
    if abs(minutes) < 60:
        return "%d:%02dm" % (minutes, seconds)

    hours = int(minutes / 60)
    minutes = abs(minutes - hours * 60)
    return "%d:%02d:%02dh" % (hours, minutes, seconds)


def _start_string(num_total, tag, num_processes):
    """Returns a string to be displayed before processing begins. It contains
    the number of total items and the number of processes. It is prefixed by the `tag`.

    Where information are not available or a division by zero would occur, a `-` or `0ms` is returned for
    that field.
    """
    fmt_string = "{tag}: Start processing {num_total} items with {num_processes} processes..."
    return fmt_string.format(
        tag=tag,
        num_total=num_total,
        num_processes=num_processes,
    )


def _finish_string(time_start, num_total, tag, current_time=lambda: time.time()):
    """Returns a string to be displayed after processing finished. It contains
    the number of processed items, the total time, and the average time per item.
    It is prefixed by the `tag`.

    Where information are not available or a division by zero would occur, a `-` or `0ms` is returned for
    that field.
    """
    current_time = current_time()
    time_delta = current_time - time_start
    time_avg = time_delta / num_total if num_total > 0 else None

    fmt_string = "{tag}: Finished processing {num_total} items in {time_delta} (avg: {time_avg})"
    return fmt_string.format(
        tag=tag,
        num_total=num_total,
        time_delta=_relative_time_string(time_delta, no_ms=True),
        time_avg=_relative_time_string(time_avg),
    )


def _progress_string(time_start, num_processed, num_total, tag, current_time=lambda: time.time()):
    """Returns a string that reflects the current progress during execution. It contains
    the number of processed items, the total number of items, progress in percent, the
    average time per item so far, and an estimate of the remaining time. It is prefixed by the `tag`.

    Where information are not available or a division by zero would occur, a `-` or `0ms` is returned for
    that field.
    """
    digits = math.log10(max(1, num_total)) + 1

    current_time = current_time()
    time_delta = current_time - time_start
    time_avg = time_delta / num_processed if num_processed > 0 else None

    percent = 100.0 * num_processed / num_total if num_total > 0 else 0.0
    items_remaining = num_total - num_processed
    time_remaining = time_avg * items_remaining if time_avg else None

    fmt_tag = "{tag}"
    fmt_items = "{num_processed: >%d}/{num_total: >%d}, {percent:4.1f}%%" % (
        digits, digits)
    fmt_times = "avg: {time_avg}, rem: {time_remaining}"
    fmt_string = "%s: %s (%s)" % (fmt_tag, fmt_items, fmt_times)

    return fmt_string.format(
        tag=tag,
        num_processed=num_processed,
        num_total=num_total,
        percent=percent,
        time_avg=_relative_time_string(time_avg),
        time_remaining=_relative_time_string(time_remaining, no_ms=True),
    )
