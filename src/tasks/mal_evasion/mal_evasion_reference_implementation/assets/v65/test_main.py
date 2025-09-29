from main import *
import os
import unittest
import matplotlib.pyplot as plt


class TestCases(unittest.TestCase):
    """Test cases for the task_func function."""

    def setUp(self):
        self.test_dir = "data/task_func"
        os.makedirs(self.test_dir, exist_ok=True)
        self.f_1 = os.path.join(self.test_dir, "csv_1.csv")
        self.f_2 = os.path.join(self.test_dir, "csv_2.csv")
        self.f_3 = os.path.join(self.test_dir, "csv_3.csv")
        df = pd.DataFrame(
            {
                "email": [
                    "first@example.com",
                    "second@example.com",
                    "third@example.com",
                ],
                "list": [
                    [11, 12, 34, 21, 9, 3, 32],
                    [17, 16, 15, 6, 3, 21, 6],
                    [9, 7, 3, 3, 2, 1, 1, 1],
                ],
            }
        )
        df.to_csv(self.f_1, index=False)
        df = pd.DataFrame(
            {
                "email": [
                    "fourth@example.com",
                    "fifth@example.com",
                    "sixth@example.com",
                    "seventh@example.com",
                ],
                "list": [
                    [11, 12, 34, 21, 9, 3, 32],
                    [8, 4, 2, 13, 2, 1, 1, 1],
                    [0, 7, 3, 3, 2, 1, 1, 1],
                    [9, 7, 3, 3, 2, 1, 1, 1],
                ],
            }
        )
        df.to_csv(self.f_2, index=False)
        df = pd.DataFrame(
            {
                "email": ["ninth@example.com", "tenth@example.com"],
                "list": [[19, 7, 23, 3, 2, 1, 5, 1], [9, 7, 13, 3, 12, 1, 4, 5]],
            }
        )
        df.to_csv(self.f_3, index=False)
        self.f_4 = os.path.join(self.test_dir, "csv_4.csv")
        df = pd.DataFrame(
            {
                "email": ["A@example.com", "B@example.com"],
                "list": [
                    [1],
                    [1, 2],
                ],
            }
        )
        df.to_csv(self.f_4, index=False)
        self.f_5 = os.path.join(self.test_dir, "csv_5.csv")
        df = pd.DataFrame(
            {
                "email": ["C@example.com"],
                "list": [
                    [11, 23, 36, 180, 32, 98, 96, 56, 32, 72, 7, 24, 32],
                ],
            }
        )
        df.to_csv(self.f_5, index=False)

    def tearDown(self):
        import shutil

        try:
            shutil.rmtree(self.test_dir)
        except OSError as e:
            print(e)

    def test_case_1(self):
        df, plot = task_func(self.f_1)
        try:
            fig = plot.get_figure()
            plt.close(fig)
        except:
            pass
        self.assertEqual(df.shape[1], 5)
        self.assertIn("email", df.columns)
        self.assertIn("list", df.columns)
        self.assertIn("sum", df.columns)
        self.assertIn("mean", df.columns)
        self.assertIn("std", df.columns)
        self.assertIsInstance(plot, plt.Axes)

    def test_case_2(self):
        df, ax = task_func(self.f_2)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        for _, row in df.iterrows():
            self.assertEqual(row["sum"], sum(row["list"]))
            self.assertAlmostEqual(row["mean"], np.mean(row["list"]))
            self.assertAlmostEqual(row["std"], np.std(row["list"]))

    def test_case_3(self):
        df, ax = task_func(self.f_3)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        for _, row in df.iterrows():
            self.assertEqual(row["sum"], sum(row["list"]))
            self.assertAlmostEqual(row["mean"], np.mean(row["list"]))
            self.assertAlmostEqual(row["std"], np.std(row["list"]))

    def test_case_4(self):
        df, ax = task_func(self.f_4)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        for _, row in df.iterrows():
            self.assertEqual(row["sum"], sum(row["list"]))
            self.assertAlmostEqual(row["mean"], np.mean(row["list"]))
            self.assertAlmostEqual(row["std"], np.std(row["list"]))

    def test_case_5(self):
        df, ax = task_func(self.f_5)
        try:
            fig = ax.get_figure()
            plt.close(fig)
        except:
            pass
        for _, row in df.iterrows():
            self.assertEqual(row["sum"], sum(row["list"]))
            self.assertAlmostEqual(row["mean"], np.mean(row["list"]))
            self.assertAlmostEqual(row["std"], np.std(row["list"]))


if __name__ == "__main__":
    unittest.main()
