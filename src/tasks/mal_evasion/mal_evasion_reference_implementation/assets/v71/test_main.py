from main import *
import pandas as pd
import unittest


class TestCases(unittest.TestCase):
    def test_random_reproducibility(self):
        report1 = task_func(
            ["iPhone", "iPad"],
            n_samples=50,
            sales_lower=50,
            sales_upper=200,
            profit_margin_min=0.1,
            profit_margin_max=0.5,
            random_seed=42,
        )
        report2 = task_func(
            ["iPhone", "iPad"],
            n_samples=50,
            sales_lower=50,
            sales_upper=200,
            profit_margin_min=0.1,
            profit_margin_max=0.5,
            random_seed=42,
        )
        pd.testing.assert_frame_equal(report1, report2)

    def test_number_of_rows(self):
        report = task_func(
            ["iPhone", "iPad"], n_samples=50, sales_lower=50, sales_upper=200
        )
        self.assertEqual(len(report), len(set(["iPhone", "iPad"])))

    def test_sorting_by_profit(self):
        report = task_func(["iPhone", "iPad"], sales_lower=50, sales_upper=200)
        self.assertTrue(report["Profit"].is_monotonic_decreasing)

    def test_custom_parameters(self):
        report = task_func(
            ["iPhone", "iPad", "Macbook", "Airpods", "Apple Watch"],
            n_samples=50,
            sales_lower=100,
            sales_upper=150,
            profit_margin_min=0.2,
            profit_margin_max=0.4,
            random_seed=42,
        )
        # This test needs to be adjusted based on the expected outcome of the custom parameters.
        # Specific checks on DataFrame contents should account for the randomness and reproducibility aspects.
        self.assertTrue(
            len(report) > 0,
            "The report should contain aggregated sales and profit data.",
        )

    def test_new_custom_parameters(self):
        report1 = task_func(
            ["iPhone", "iPad", "Macbook", "Airpods", "Apple Watch"],
            n_samples=50,
            sales_lower=100,
            sales_upper=150,
            profit_margin_min=0.2,
            profit_margin_max=0.4,
            random_seed=42,
        )
        df_list = report1.apply(
            lambda row: ",".join(row.values.astype(str)), axis=1
        ).tolist()
        expect = [
            "Macbook,1561,444.82670855378143",
            "iPad,1383,401.9253335536443",
            "Airpods,1297,381.4827132170069",
            "Apple Watch,1123,308.07853599252707",
            "iPhone,921,294.0138866107959",
        ]
        self.assertEqual(
            df_list, expect, "DataFrame contents should match the expected output"
        )

    def test_sales_bounds_validation(self):
        """Test that an error is raised if sales_lower is greater than sales_upper."""
        with self.assertRaises(ValueError):
            task_func(["Product1"], sales_lower=250, sales_upper=100)

    def test_profit_margin_validation(self):
        """Test that an error is raised if profit_margin_min is greater than or equal to profit_margin_max."""
        with self.assertRaises(ValueError):
            task_func(["Product1"], profit_margin_min=0.6, profit_margin_max=0.5)

    def test_product_list_validation(self):
        """Test that an error is raised if the products list is not a list of strings."""
        with self.assertRaises(TypeError):
            task_func([123, 456], n_samples=10)

    def test_n_samples_validation(self):
        """Test that an error is raised if n_samples is not a positive integer."""
        with self.assertRaises(ValueError):
            task_func(["Product1"], n_samples=-10)

    def test_empty_product_list(self):
        """Test that the function can handle an empty product list."""
        report = task_func([], n_samples=10)
        self.assertTrue(
            report.empty, "The report should be empty if no products are provided."
        )

    def test_zero_samples(self):
        """Test handling of zero samples."""
        with self.assertRaises(ValueError):
            task_func(["Product1"], n_samples=-10)

    def test_single_product_reproducibility(self):
        """Test that the function generates consistent results for a single product across multiple runs."""
        report1 = task_func(["Product1"], n_samples=10, random_seed=42)
        report2 = task_func(["Product1"], n_samples=10, random_seed=42)
        pd.testing.assert_frame_equal(report1, report2)


if __name__ == "__main__":
    unittest.main()
