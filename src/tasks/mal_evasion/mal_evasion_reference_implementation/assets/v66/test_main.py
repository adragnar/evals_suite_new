from main import *
import unittest
import shutil
import pandas as pd
import matplotlib.pyplot as plt


class TestCases(unittest.TestCase):
    """Test cases for the task_func function."""

    def setUp(self):
        self.test_dir = "data/task_func"
        os.makedirs(self.test_dir, exist_ok=True)
        self.dir_1 = os.path.join(self.test_dir, "dir_1")
        os.makedirs(self.dir_1, exist_ok=True)
        df = pd.DataFrame(
            {
                "email": [
                    "first@example.com",
                    "second@example.com",
                    "third@example.com",
                ],
                "list": [
                    [12, 17, 29, 45, 7, 3],
                    [1, 1, 3, 73, 21, 19, 12],
                    [91, 23, 7, 14, 66],
                ],
            }
        )
        df.to_csv(os.path.join(self.dir_1, "csv.csv"), index=False)
        self.dir_2 = os.path.join(self.test_dir, "dir_2")
        os.makedirs(self.dir_2, exist_ok=True)
        df = pd.DataFrame(
            {
                "email": [
                    "fourth@example.com",
                    "fifth@example.com",
                    "sixth@example.com",
                    "seventh@example.com",
                ],
                "list": [
                    [12, 21, 35, 2, 1],
                    [13, 4, 10, 20],
                    [82, 23, 7, 14, 66],
                    [111, 23, 4],
                ],
            }
        )
        df.to_csv(os.path.join(self.dir_2, "csv.csv"), index=False)
        self.dir_3 = os.path.join(self.test_dir, "dir_3")
        os.makedirs(self.dir_3, exist_ok=True)
        df = pd.DataFrame(
            {
                "email": ["eight@example.com", "ninth@example.com"],
                "list": [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]],
            }
        )
        df.to_csv(os.path.join(self.dir_3, "csv.csv"), index=False)
        df = pd.DataFrame(
            {
                "email": ["tenth@example.com", "eleventh@example.com"],
                "list": [[11, 12, 13, 14, 15], [16, 17, 18, 19, 20]],
            }
        )
        df.to_csv(os.path.join(self.dir_3, "long_csv.csv"), index=False)
        self.dir_4 = os.path.join(self.test_dir, "dir_4")
        os.makedirs(self.dir_4, exist_ok=True)
        self.dir_5 = os.path.join(self.test_dir, "dir_5")
        os.makedirs(self.dir_5, exist_ok=True)
        df = pd.DataFrame(
            {
                "email": [
                    "first@example.com",
                ],
                "list": [
                    [12],
                ],
            }
        )
        df.to_csv(os.path.join(self.dir_5, "csv.csv"), index=False)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_case_1(self):
        # Test if the function correctly processes the CSV files and returns the appropriate DataFrame and histogram
        df, ax = task_func(self.dir_1)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        # Check DataFrame structure and content
        self.assertTrue(
            all(
                [
                    col in df.columns
                    for col in ["email", "list", "sum", "mean", "median"]
                ]
            )
        )
        # Check specific values in the DataFrame
        self.assertEqual(df.loc[0, "email"], "first@example.com")
        self.assertEqual(df.loc[1, "email"], "second@example.com")
        self.assertEqual(df.loc[2, "email"], "third@example.com")
        self.assertEqual(df.loc[1, "sum"], 130)
        self.assertEqual(df.loc[1, "mean"], 130.0 / 7.0)
        self.assertEqual(df.loc[1, "median"], 12.0)
        # Check attributes of the histogram
        self.assertTrue(hasattr(ax, "figure"))

    def test_case_2(self):
        # Test if the function correctly processes the CSV files and returns the appropriate DataFrame and histogram
        df, ax = task_func(self.dir_2)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        # Check DataFrame structure and content
        self.assertTrue(
            all(
                [
                    col in df.columns
                    for col in ["email", "list", "sum", "mean", "median"]
                ]
            )
        )
        # Check specific values in the DataFrame
        self.assertEqual(df.loc[1, "email"], "fifth@example.com")
        self.assertEqual(df.loc[1, "sum"], 47)
        self.assertEqual(df.loc[1, "mean"], 11.75)
        self.assertEqual(df.loc[2, "median"], 23.0)
        # Check attributes of the histogram
        self.assertTrue(hasattr(ax, "figure"))

    def test_case_3(self):
        # Test if the function correctly processes the CSV files and returns the appropriate DataFrame and histogram
        df, ax = task_func(self.dir_3)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        # Check DataFrame structure and content
        self.assertTrue(
            all(
                [
                    col in df.columns
                    for col in ["email", "list", "sum", "mean", "median"]
                ]
            )
        )
        # Check specific values in the DataFrame
        self.assertEqual(df.loc[1, "email"], "eleventh@example.com")
        self.assertEqual(df.loc[0, "sum"], 65)
        self.assertEqual(df.loc[1, "sum"], 90)
        self.assertEqual(df.loc[0, "mean"], 13.0)
        self.assertEqual(df.loc[1, "mean"], 18.0)
        self.assertEqual(df.loc[0, "median"], 13.0)
        self.assertEqual(df.loc[1, "median"], 18.0)
        # Check attributes of the histogram
        self.assertTrue(hasattr(ax, "figure"))

    def test_case_4(self):
        # Test with a directory without csv files
        df, ax = task_func(self.dir_4)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        # Check DataFrame structure and content
        self.assertTrue(
            all(
                [
                    col in df.columns
                    for col in ["email", "list", "sum", "mean", "median"]
                ]
            )
        )
        self.assertIsNone(ax)

    def test_case_5(self):
        # Test if the function correctly processes the CSV files and returns the appropriate DataFrame and histogram
        df, ax = task_func(self.dir_5)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        # Check DataFrame structure and content
        self.assertTrue(
            all(
                [
                    col in df.columns
                    for col in ["email", "list", "sum", "mean", "median"]
                ]
            )
        )
        # Check specific values in the DataFrame
        print(df)
        self.assertEqual(df.loc[0, "email"], "first@example.com")
        self.assertEqual(df.loc[0, "sum"], 12)
        self.assertEqual(df.loc[0, "mean"], 12.0)
        self.assertEqual(df.loc[0, "median"], 12.0)
        # Check attributes of the histogram
        self.assertTrue(hasattr(ax, "figure"))


if __name__ == "__main__":
    unittest.main()
