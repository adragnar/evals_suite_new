from main import *
import unittest
import pandas as pd


class TestCases(unittest.TestCase):
    def test_case_1(self):
        # Testing basic functionality
        result = task_func(["A", "B", "C", "A", "D", "E", "B", "C"])
        expected = pd.DataFrame(
            {
                "Category": ["A", "B", "C", "A", "D", "E", "B", "C"],
                "Encoded": [0, 1, 2, 0, 3, 4, 1, 2],
            }
        )
        pd.testing.assert_frame_equal(result, expected)

    def test_case_2(self):
        # Testing with a single unique category
        result = task_func(["A", "A", "A"])
        expected = pd.DataFrame({"Category": ["A", "A", "A"], "Encoded": [0, 0, 0]})
        pd.testing.assert_frame_equal(result, expected)

    def test_case_3(self):
        # Testing with an empty list
        result = task_func([])
        expected = pd.DataFrame({"Category": [], "Encoded": []})
        pd.testing.assert_frame_equal(result, expected, check_dtype=False)

    def test_case_4(self):
        # Testing with multiple unique categories but in a different order
        result = task_func(["E", "D", "C", "B", "A"])
        expected = pd.DataFrame(
            {"Category": ["E", "D", "C", "B", "A"], "Encoded": [4, 3, 2, 1, 0]}
        )
        pd.testing.assert_frame_equal(result, expected)

    def test_case_5(self):
        # Testing with a list containing a single different category
        result = task_func(["Z"])
        expected = pd.DataFrame({"Category": ["Z"], "Encoded": [0]})
        pd.testing.assert_frame_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
