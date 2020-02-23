import time
import unittest

from .context import busybee


#
# Test cases
#

class CorrectnessTestSuite(unittest.TestCase):

    def test_list_WHEN_empty_list_THEN_empty_list(self):
        actual = busybee.map(func_add_one, [], stdout=NullStdout())
        self.assertListEqual(actual, [])

    def test_list_WHEN_executed_one_core_THEN_in_order_and_applied(self):
        actual = busybee.map(
            func=func_add_one,
            data=list(range(0, 1000)),
            processes=1,
            stdout=NullStdout(),
        )
        self.assertListEqual(actual, list(range(1, 1001)))

    def test_list_WHEN_executed_many_processes_THEN_in_order_and_applied(self):
        actual = busybee.map(
            func=func_add_one,
            data=list(range(0, 1000)),
            processes=8,
            stdout=NullStdout(),
        )
        self.assertListEqual(actual, list(range(1, 1001)))

    def test_list_WHEN_executed_all_processes_THEN_in_order_and_applied(self):
        actual = busybee.map(
            func=func_add_one,
            data=list(range(0, 1000)),
            processes='n',
            stdout=NullStdout(),
        )
        self.assertListEqual(actual, list(range(1, 1001)))


class OutputTestSuite(unittest.TestCase):

    def test_list_WHEN_empty_list_THEN_warning_output(self):
        recorder = RecordingStdout()
        busybee.map(None, [], stdout=recorder)

        self.assertIn("skipping because of empty input", recorder.output)

    def test_list_WHEN_quiet_on_THEN_no_output(self):
        recorder = RecordingStdout()
        busybee.map(
            func=func_add_one,
            data=[1, 2, 3],
            quiet=True,
            stdout=recorder,
        )

        self.assertEqual("", recorder.output)

    def test_list_WHEN_executing_THEN_outputs_core_information(self):
        recorder = RecordingStdout()

        # Note: func_add_one_slow takes ~10ms. Therefore this finishes in
        # no less than 0.5s with processes=2.
        busybee.map(
            func=func_add_one_slow,
            data=list(range(0, 100)),
            processes='2',
            stdout=recorder,
        )

        self.assertIn("Start processing 100 items", recorder.output)
        self.assertIn("2 processes", recorder.output)

        self.assertIn("50/100, 50.0%", recorder.output)
        self.assertIn("avg: 5ms,", recorder.output)

        self.assertIn("Finished processing 100 items", recorder.output)
        self.assertIn("(avg: 5ms)", recorder.output)


#
# Helpers
#


class RecordingStdout():
    """Matches the `write` method of sys.stdout and appends all
    data to an internal `output` string.
    """

    def __init__(self):
        self.output = ""

    def write(self, string):
        self.output += string


class NullStdout():
    """Matches the `write` method of sys.stdout and ignores all calls."""

    def write(self, _):
        pass


def func_add_one(x):
    """Returns x + 1."""
    return x + 1


def func_add_one_slow(x):
    """Waits 10ms and returns x + 1."""
    time.sleep(10 / 1000)
    return x + 1
