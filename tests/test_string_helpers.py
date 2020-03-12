import multiprocessing as mp
import random
import unittest

from .context import _string_helpers as _sh


class RelativeTimeStringTestSuite(unittest.TestCase):

    def test_rel_time_string_WHEN_zero_THEN_zero_ms(self):
        self.assertEqual("0ms", _sh._relative_time_string(0.0))
        self.assertEqual("0ms", _sh._relative_time_string(-0.0))

    def test_rel_time_string_WHEN_none_THEN_dash(self):
        self.assertEqual("-", _sh._relative_time_string(None))

    def test_rel_time_string_WHEN_in_ms_area_THEN_ms_string(self):
        self.assertEqual("100ms", _sh._relative_time_string(0.1))
        self.assertEqual("999ms", _sh._relative_time_string(0.999))
        self.assertEqual("-50ms", _sh._relative_time_string(-0.05))

    def test_rel_time_string_WHEN_in_seconds_area_THEN_seconds_string(self):
        self.assertEqual("1.0s", _sh._relative_time_string(1.0))
        self.assertEqual("60.2s", _sh._relative_time_string(60.2))
        self.assertEqual("-5.0s", _sh._relative_time_string(-5))

    def test_rel_time_string_WHEN_in_minutes_area_THEN_minutes_string(self):
        self.assertEqual("2:02m", _sh._relative_time_string(120 + 2))
        self.assertEqual("-2:05m", _sh._relative_time_string(-120 - 5))
        self.assertEqual("5:00m", _sh._relative_time_string(5*60))

    def test_rel_time_string_WHEN_in_hours_area_THEN_hours_string(self):
        self.assertEqual("1:00:00h", _sh._relative_time_string(3600))
        self.assertEqual(
            "1:23:45h",
            _sh._relative_time_string(3600 + 23*60 + 45))
        self.assertEqual(
            "-11:23:45h",
            _sh._relative_time_string(-11*3600 - 23*60 - 45))


class StartStringTestSuite(unittest.TestCase):

    def test_start_string_WHEN_given_info_THEN_all_in_output(self):
        actual = _sh._start_string(100, "tag", 8)
        self.assertIn("tag:", actual)
        self.assertIn("100 items", actual)
        self.assertIn("8 processes", actual)


class FinishStringTestSuite(unittest.TestCase):

    def test_finish_string_WHEN_given_info_THEN_all_in_output(self):
        actual = _sh._finish_string(
            time_start=0.0,
            total_cpu_time=4.2,
            num_total=100,
            tag="tag",
            current_time=lambda: 4.2
        )
        self.assertIn("tag:", actual)
        self.assertIn("100 items", actual)
        self.assertIn("in 4.2s", actual)
        self.assertIn("avg: 42ms", actual)

    def test_finish_string_WHEN_given_zeros_THEN_output_valid(self):
        actual = _sh._finish_string(
            time_start=0.0,
            total_cpu_time=0.0,
            num_total=0,
            tag="tag",
            current_time=lambda: 0.0
        )
        self.assertIn("tag:", actual)
        self.assertIn("0 items", actual)
        self.assertIn("in 0.0s", actual)
        self.assertIn("avg: -", actual)


class ProgressStringTestSuite(unittest.TestCase):

    def test_progress_string_WHEN_given_info_THEN_all_in_output(self):
        actual = _sh._progress_string(
            total_cpu_time=42.0,
            num_processed=42,
            num_total=100,
            num_processes=2,
            tag="tag",
        )
        self.assertIn("tag:", actual)
        self.assertIn("42/100", actual)
        self.assertIn("42.0%", actual)
        self.assertIn("avg: 1.0s cpu", actual)
        self.assertIn("rem: 29.0s", actual)

    def test_progress_string_WHEN_given_zeros_THEN_output_valid(self):
        actual = _sh._progress_string(
            total_cpu_time=0.0,
            num_processed=0,
            num_total=0,
            num_processes=2,
            tag="tag",
        )
        self.assertIn("tag:", actual)
        self.assertIn("0/0", actual)
        self.assertIn("0%", actual)
        self.assertIn("avg: - cpu", actual)
        self.assertIn("rem: -", actual)
