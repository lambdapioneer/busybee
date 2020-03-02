"""The internal implementation of the busybee module. The `_map` method is
exported on module level through __init__.py."""

import math
import multiprocessing as mp
import time
import os
import sys

from ._string_helpers import _start_string, _progress_string, _finish_string

__VALUE_ERROR_INVALID_CORE_SPEC = ValueError(
    "Invalid core_spec! Try: `1`, `8`, `n/2`, `n-1`")

__VALUE_ERROR_INVALID_REL_CORE_SPEC = ValueError(
    "Invalid relative core_spec! Try: `n`, `n/2`, `n-1`")


def _parse_core_spec(core_spec, core_count=lambda: mp.cpu_count()):
    """Parses a `core_spec` that expresses the number of intended processes for execution
    of one of the high-level API calls. The core specification can be of two types.

    Type I is explicit by providing the number of processes to use.

    Type II is implicit by providing a value relative to the number of logical CPUs `n`.
    For Type II both simple division and substraction are allowed in the forms `n/c`
    and `n-c` where `c` is an integer. The result will increased if it is below 1.

    Examples for both types: `1`, `8`, `n-1`, `n/2`, `n/4`.

    Args:
        core_spec (String): The core specification to parse
        core_count (lambda: () -> int): A function to return the actual number of
                                        logical CPUs. Defaults to the number returned
                                        by the multiprocessing package

    Raises:
        ValueError: When given an invalid core spec

    Returns:
        int: The number of processes to use. Guaranteed to be >= 1
    """
    if not core_spec:
        raise __VALUE_ERROR_INVALID_CORE_SPEC

    # Type II: `core_spec` is a string with a simple formula
    if isinstance(core_spec, str) and len(core_spec) >= 1 and core_spec[0] == 'n':
        n = core_count()

        if len(core_spec) == 1:
            return n

        operator = core_spec[1]
        if len(core_spec) < 3 or operator not in "-/":
            raise __VALUE_ERROR_INVALID_REL_CORE_SPEC

        try:
            operand = int(core_spec[2:])
        except ValueError:
            raise __VALUE_ERROR_INVALID_REL_CORE_SPEC

        if operator == '-':
            return max(n - operand, 1)
        elif operator == '/':
            return max(int(n / operand), 1)
        else:  # pragma: no cover
            raise AssertionError()

    # Type I: `core_spec` is a number
    try:
        n = int(core_spec)
    except:
        raise __VALUE_ERROR_INVALID_CORE_SPEC

    if n <= 0:
        raise ValueError("If processes is a number it must be positive")

    return n


class _ProgressUpdateLimit():
    """Evaluates the progress state and indicates whether a progress update should
    be provided to the user.
    """

    def __init__(self, time_start, num_total, every_n_seconds=5, every_n_percent=50):
        self.time_start = time_start
        self.num_total = num_total

        self.time_last_update = time_start
        self.every_n_seconds = every_n_seconds

        self.percent_last_update = 0.0
        self.every_n_percent = every_n_percent

    def should_print(self, num_processed, current_time=None):
        """Returns `True` if an output should be provided to the user. Updates
        the internal state to track the most recent output.
        """
        if num_processed == self.num_total:
            # Do not print the 100% update as the finish message will follow directly afterwards
            return False

        if self.every_n_seconds:
            current_time = current_time() if current_time else time.time()
            if current_time - self.time_last_update >= self.every_n_seconds:
                self.time_last_update = current_time
                return True

        if self.every_n_percent:
            current_percent = 100.0 * num_processed / self.num_total
            if current_percent - self.percent_last_update >= self.every_n_percent:
                self.percent_last_update = current_percent
                return True

        return False


def _meta_func(args):
    """Takes args in the form `(func, data)` and calls `func(data)`."""
    func, data = args
    return func(data)


def _map(
    func,
    data,
    quiet=False,
    processes="n",
    tag="BusyBee",
    stdout=sys.stdout,
    update_every_n_seconds=5,
    update_every_n_percent=50,
):
    """Applies the given `func` to every item in `data` using up to the number of processes
    specified by `processes`. Interactive updates are provided via `stdout` following the limits
    provided by the `update_every_n_*` arguments.

    Args:
        func: The function that will be applied to the `data` items. It needs to be pickleable and
            therefore it must not be a lambda expression.

        data (list): The data that is processed by `func`. This must provide random access and `len()` support.
                     Ideally this is a simple list.

        quiet (bool): If `True`, no output is generated

        processes (int or string): A number of processes to use (e.g. 1, 8) or a simple formula expressing
                                the number of processes relative to the number of logical cores (e.g. `n`,
                                `n/2`, `n-1). Only simple substraction and division are supported.

        tag (string): A tag to be prefixed to the output. Helpful when chaining `map` operations.

        stdout: An object providing a `write` method as in `sys.stdout`.

        update_every_n_seconds (int or float): Produce a progress update every `n` seconds but not faster than
                                            the actual processing rate. Set to `None` to deactivate.

        update_every_n_percent (int or float): Produce a progress update every `n` percent of completion but
                                            not faster than the actual processing rate. Set to `None` to
                                            deactivate.

    Raises:
        ValueError: If an invalid specification is provided to the `processes` argument

    Returns:
        The processed list with items following the order of the original list.
    """
    # internal wrapper for output
    def println(string):
        if quiet:
            return
        stdout.write(string + os.linesep)

    # do not even try anything when having an empty input
    if len(data) == 0:
        println("%s: skipping because of empty input" % tag)
        return []

    # setup: multiprocessing
    num_processes = _parse_core_spec(processes)
    pool = mp.Pool(processes=num_processes)

    # setup: internal state
    num_total = len(data)
    chunksize = max(1, num_total // 1000)
    time_start = time.time()

    # setup: the update_limit decides when to print progress update messages
    update_limit = _ProgressUpdateLimit(
        time_start=time_start,
        num_total=num_total,
        every_n_seconds=update_every_n_seconds,
        every_n_percent=update_every_n_percent
    )

    # before execution
    println(_start_string(num_total, tag, num_processes))

    # actual execution
    result = []
    meta_args = [(func, d) for d in data]
    for idx, r in enumerate(pool.imap(_meta_func, meta_args, chunksize=chunksize)):
        result.append(r)

        num_processed = idx + 1
        if update_limit.should_print(num_processed):
            println(_progress_string(time_start, num_processed, num_total, tag))

    # after execution
    println(_finish_string(time_start, num_total, tag))

    # clean up! See: https://bugs.python.org/issue34172 - Python
    # does NOT terminate the background pool processes by default even
    # though the documentation claims it does so when being GCed.
    pool.close()

    return result


def _filter(
    func,
    data,
    quiet=False,
    processes="n",
    tag="BusyBee",
    stdout=sys.stdout,
    update_every_n_seconds=5,
    update_every_n_percent=50,
):
    """Applies the given `func` to every item in `data` using up to the number of processes
    specified by `processes`. Returns all `data` items where `func` evaluates `True`.

    Args:
        func: The function that will be applied to the `data` items. It needs to be pickleable and
            therefore it must not be a lambda expression.

        data (list): The data that is processed by `func`. This must provide random access and `len()` support.
                     Ideally this is a simple list.

        For the other arguments see the map(...) function.

    Returns:
        The filterred items following the order of the original list.
    """
    is_included = _map(
        func=func,
        data=data,
        quiet=quiet,
        processes=processes,
        tag=tag,
        stdout=stdout,
        update_every_n_seconds=update_every_n_seconds,
        update_every_n_percent=update_every_n_percent,
    )

    result = [item for idx, item in enumerate(data) if is_included[idx]]
    return result


def _mk_dict(
    func,
    keys,
    quiet=False,
    processes="n",
    tag="BusyBee",
    stdout=sys.stdout,
    update_every_n_seconds=5,
    update_every_n_percent=50,
):
    """Creates a new dictionary with the given `keys` and values as the application of `func`
    to the individual key.

    Args:
        func: The function that will be applied to the `keys` items to derive the respective values.
              It needs to be pickleable and therefore it must not be a lambda expression.

        keys (list): The keys of the new dictionary. This must provide random access and `len()` support.
                     Ideally this is a simple list.

        For the other arguments see the map(...) function.

    Returns:
        The a new dictionary with the given `keys` and values as `func(keys)`.
    """

    # Remove duplicates before processing; convert to list to ensure order
    unique_keys = list(set(keys))

    values = _map(
        func=func,
        data=unique_keys,
        quiet=quiet,
        processes=processes,
        tag=tag,
        stdout=stdout,
        update_every_n_seconds=update_every_n_seconds,
        update_every_n_percent=update_every_n_percent,
    )

    return dict(zip(unique_keys, values))
