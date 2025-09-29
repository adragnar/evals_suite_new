from main import *
import unittest
import pandas as pd


class TestCases(unittest.TestCase):
    def setUp(self):
        # Setup common to all tests: A product dictionary
        self.product_dict = {
            "Apple": [100, 2.5],
            "Orange": [80, 3.5],
            "Banana": [120, 1.5],
        }

    def test_case_1(self):
        # Test with a single product
        product_keys = ["Apple"]
        report, ax = task_func(self.product_dict, product_keys)
        self.assertEqual(len(report), 1)  # Should return 1 row
        self.assertIn("Apple", report["Product"].values)
        self.assertAlmostEqual(report["Average Price"].iloc[0], 2.5)
        self.assertAlmostEqual(report["Average Profit"].iloc[0], 250.0)

    def test_case_2(self):
        # Test with multiple products
        product_keys = ["Apple", "Orange"]
        report, ax = task_func(self.product_dict, product_keys)
        self.assertEqual(len(report), 2)  # Should return 2 rows
        self.assertTrue(
            all(item in ["Apple", "Orange"] for item in report["Product"].values)
        )
        expected_avg_price = (2.5 + 3.5) / 2
        expected_avg_profit = (250.0 + 280.0) / 2
        self.assertTrue(all(report["Average Price"] == expected_avg_price))
        self.assertTrue(all(report["Average Profit"] == expected_avg_profit))

    def test_case_3(self):
        # Test with no products
        product_keys = []
        report, ax = task_func(self.product_dict, product_keys)
        self.assertTrue(report.empty)  # Should return an empty DataFrame

    def test_case_4(self):
        # Test with a product that doesn't exist in the dictionary
        product_keys = ["Mango"]  # Mango is not in product_dict
        with self.assertRaises(KeyError):
            task_func(self.product_dict, product_keys)

    def test_case_5(self):
        # Test the DataFrame structure
        product_keys = ["Apple", "Banana"]
        report, ax = task_func(self.product_dict, product_keys)
        expected_columns = [
            "Product",
            "Quantity",
            "Price",
            "Profit",
            "Average Price",
            "Average Profit",
        ]
        self.assertEqual(list(report.columns), expected_columns)
        for col in ["Quantity", "Price", "Profit", "Average Price", "Average Profit"]:
            self.assertTrue(
                pd.api.types.is_numeric_dtype(report[col]),
                f"{col} should be numeric type",
            )


if __name__ == "__main__":
    unittest.main()
