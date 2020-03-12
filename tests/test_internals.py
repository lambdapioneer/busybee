import multiprocessing as mp
import random
import unittest

from .context import _busybee


class processespecParsingTestSuite(unittest.TestCase):

    def test_core_spec_parser_WHEN_number_THEN_number(self):
        self.assertEqual(1, _busybee._parse_core_spec(1))
        self.assertEqual(1, _busybee._parse_core_spec("1"))
        self.assertEqual(8, _busybee._parse_core_spec(8.8))

    def test_core_spec_parser_WHEN_illegal_number_THEN_throws(self):
        illegal_number = [-1, "0", -0.5, 0]

        for spec in illegal_number:
            with self.assertRaises(ValueError):
                _busybee._parse_core_spec(spec)

    def test_core_spec_parser_WHEN_none_like_value_THEN_throws(self):
        with self.assertRaises(ValueError):
            _busybee._parse_core_spec("")

        with self.assertRaises(ValueError):
            _busybee._parse_core_spec(None)

    def test_core_spec_parser_WHEN_just_n_THEN_processes_returned(self):
        n = 8
        self.assertEqual(
            n,
            _busybee._parse_core_spec("n", core_count=lambda: n))

    def test_core_spec_parser_WHEN_n_formula_THEN_calculated_processes_returned(self):
        for n in (4, 6, 8, 32):
            self.assertEqual(
                n-2,
                _busybee._parse_core_spec("n-2", core_count=lambda: n))
            self.assertEqual(
                n//2,
                _busybee._parse_core_spec("n/2", core_count=lambda: n))

    def test_core_spec_parser_WHEN_floating_n_formula_THEN_rounded_down(self):
        self.assertEqual(
            1,
            _busybee._parse_core_spec("n/2", core_count=lambda: 3))

    def test_core_spec_parser_WHEN_n_formula_goes_too_low_THEN_calculated_processes_always_positive(self):
        n = 8
        self.assertEqual(
            1,
            _busybee._parse_core_spec("n-999", core_count=lambda: n))
        self.assertEqual(
            1,
            _busybee._parse_core_spec("n/999", core_count=lambda: n))

    def test_core_spec_parser_WHEN_illegal_n_formula_THEN_throws(self):
        illegal_statements = [
            "n+1",
            "m-1",
            "1-n",
            "****",
            "n-n",
            "n-"
        ]

        for stmt in illegal_statements:
            with self.assertRaises(ValueError):
                _busybee._parse_core_spec(stmt)


class MetaFuncTestSuite(unittest.TestCase):

    def test_meta_func_WHEN_called_THEN_func_executed_on_data(self):
        func, data = lambda x: x+1, 1
        args = (func, data)

        actual = _busybee._meta_func(args)
        self.assertEqual(2, actual[0])


class ProgressUpdateLimitTestSuite(unittest.TestCase):

    def test_progress_update_limit_WHEN_time_passes_THEN_issues_correct_updates(self):
        pul = _busybee._ProgressUpdateLimit(
            time_start=0.0,
            num_total=100,
            every_n_seconds=5,
            every_n_percent=None,
        )

        self.assertEqual(False, pul.should_print(0, lambda: 1.0))
        self.assertEqual(True, pul.should_print(0, lambda: 5.0))
        self.assertEqual(False, pul.should_print(0, lambda: 5.0))
        self.assertEqual(False, pul.should_print(0, lambda: 9.9999))
        self.assertEqual(True, pul.should_print(0, lambda: 20))
        self.assertEqual(False, pul.should_print(0, lambda: 20))

    def test_progress_update_limit_WHEN_percent_passes_THEN_issues_correct_updates(self):
        pul = _busybee._ProgressUpdateLimit(
            time_start=0.0,
            num_total=100,
            every_n_seconds=None,
            every_n_percent=25,
        )

        self.assertEqual(False, pul.should_print(0))
        self.assertEqual(False, pul.should_print(24))
        self.assertEqual(True, pul.should_print(25))
        self.assertEqual(False, pul.should_print(25))
        self.assertEqual(True, pul.should_print(80))
        self.assertEqual(False, pul.should_print(80))

    def test_progress_update_limit_WHEN_all_off_THEN_no_updates(self):
        pul = _busybee._ProgressUpdateLimit(
            time_start=0.0,
            num_total=100,
            every_n_seconds=None,
            every_n_percent=None,
        )

        self.assertEqual(False, pul.should_print(0, lambda: 20))
        self.assertEqual(False, pul.should_print(10, lambda: 200))
        self.assertEqual(False, pul.should_print(100, lambda: 2000))

    def test_progress_update_limit_WHEN_100_percent_THEN_no_update(self):
        pul = _busybee._ProgressUpdateLimit(
            time_start=0.0,
            num_total=100,
            every_n_seconds=1,
            every_n_percent=1,
        )

        self.assertEqual(False, pul.should_print(100, lambda: 100))
