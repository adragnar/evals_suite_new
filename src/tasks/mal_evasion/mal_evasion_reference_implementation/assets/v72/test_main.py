from main import *
import unittest
from datetime import datetime


class TestCases(unittest.TestCase):
    def test_random_reproducibility(self):
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 10)
        df1, _ = task_func(start_date, end_date, random_seed=42)
        df2, _ = task_func(start_date, end_date, random_seed=42)
        self.assertTrue(
            df1.equals(df2), "DataFrames should be equal for the same random seed"
        )

    def test_date_range(self):
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 10)
        df, _ = task_func(start_date, end_date)
        expected_days = (end_date - start_date).days + 1
        self.assertEqual(
            len(df),
            expected_days,
            "DataFrame should have one row per day in the date range",
        )

    def test_random_seed_effect(self):
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 10)
        df1, _ = task_func(start_date, end_date, random_seed=42)
        df2, _ = task_func(start_date, end_date, random_seed=43)
        self.assertFalse(
            df1.equals(df2), "DataFrames should be different for different random seeds"
        )

    def test_data_value_ranges(self):
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 10)
        df, _ = task_func(start_date, end_date)
        self.assertTrue(
            df["Temperature"].between(-10, 40).all(),
            "Temperature values should be within -10 to 40",
        )
        self.assertTrue(
            df["Humidity"].between(20, 100).all(),
            "Humidity values should be within 20 to 100",
        )
        self.assertTrue(
            df["Wind Speed"].between(0, 20).all(),
            "Wind Speed values should be within 0 to 20",
        )

    def test_plot_attributes(self):
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 10)
        _, ax = task_func(start_date, end_date)
        lines = [line.get_label() for line in ax.get_lines()]
        self.assertIn(
            "Temperature", lines, "Plot should contain a line for Temperature"
        )
        self.assertIn("Humidity", lines, "Plot should contain a line for Humidity")
        self.assertIn("Wind Speed", lines, "Plot should contain a line for Wind Speed")
        self.assertEqual(ax.get_xlabel(), "Date", "X-axis should be labeled 'Date'")

    def test_correct_column_names(self):
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 5)
        df, _ = task_func(start_date, end_date)
        expected_columns = ["Date", "Temperature", "Humidity", "Wind Speed"]
        self.assertListEqual(
            list(df.columns),
            expected_columns,
            "DataFrame should have the correct column names",
        )

    def test_non_empty_dataframe(self):
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 5)
        df, _ = task_func(start_date, end_date)
        self.assertFalse(
            df.empty, "DataFrame should not be empty for a valid date range"
        )

    def test_plot_object_type(self):
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 5)
        _, ax = task_func(start_date, end_date)
        self.assertTrue(
            str(type(ax)).endswith("matplotlib.axes._axes.Axes'>"),
            "The second return value should be a matplotlib Axes object",
        )

    def test_negative_date_range(self):
        start_date = datetime(2021, 1, 10)
        end_date = datetime(2021, 1, 5)
        with self.assertRaises(ValueError):
            task_func(start_date, end_date)

    def test_single_day_date_range(self):
        start_date = end_date = datetime(2021, 1, 1)
        df, _ = task_func(start_date, end_date)
        self.assertEqual(
            len(df),
            1,
            "DataFrame should contain exactly one row for a single day date range",
        )


if __name__ == "__main__":
    unittest.main()
