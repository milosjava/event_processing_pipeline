from unittest import TestCase
from event_validation import _time_delta_to_HH_MM, validate
from datetime import datetime, timedelta
import pandas as pd


class TestEventValidation(TestCase):

    def test_validate(self):
        # call validate with test files as given in task
        df = validate(
            "tests/files/serving_events_test.csv",
            "tests/files/user_events_test.csv")

        # load expected output as given in task
        result = pd.read_csv("tests/files/validated_events_test.csv")

        # check number of rows
        self.assertEqual(len(result), len(df))

        # check column names
        self.assertEqual(str(result.columns.values), str(df.columns.values))

        # data frames are identical, just make sure that indices are reset
        self.assertTrue(
            df.reset_index(
                drop=True).equals(
                result.reset_index(
                    drop=True)))

    def test__time_delta_to_hh_mm(self):
        td = timedelta(days=0, hours=10, minutes=20)
        time_str = _time_delta_to_HH_MM(td)
        self.assertEqual("10:20", time_str)

        td = timedelta(days=0, hours=10, minutes=5)
        time_str = _time_delta_to_HH_MM(td)
        self.assertEqual("10:05", time_str)
