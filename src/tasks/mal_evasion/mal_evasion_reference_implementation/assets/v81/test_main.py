from main import *
import unittest
from unittest.mock import patch, mock_open


class TestCases(unittest.TestCase):
    def test_return_type(self):
        """Test that the function returns a list."""
        with patch("builtins.open", mock_open(read_data="word1,word2,word1")):
            result = task_func("dummy_path.csv", ",")
        self.assertIsInstance(result, list)

    def test_tuple_structure(self):
        """Test that each element in the list is a tuple with two elements."""
        with patch("builtins.open", mock_open(read_data="word1,word2,word1")):
            result = task_func("dummy_path.csv", ",")
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)

    def test_word_count(self):
        """Test if the function correctly counts the occurrences of words."""
        with patch("builtins.open", mock_open(read_data="word1\nword2\nword1")):
            result = task_func("dummy_path.csv", ",")
        self.assertIn(("word1", 2), result)
        self.assertIn(("word2", 1), result)

    def test_empty_file(self):
        """Test the function's behavior with an empty CSV file."""
        with patch("builtins.open", mock_open(read_data="")):
            result = task_func("dummy_path.csv", ",")
        self.assertEqual(len(result), 0)

    def test_no_repeated_words(self):
        """Test the function's behavior with no repeated words."""
        with patch("builtins.open", mock_open(read_data="word1,word2,word3")):
            result = task_func("dummy_path.csv", ",")
        expected_counts = {("word1", 1), ("word2", 1), ("word3", 1)}
        self.assertTrue(all(pair in expected_counts for pair in result))

    def test_custom_delimiter(self):
        """Test the function's behavior with a custom delimiter."""
        with patch("builtins.open", mock_open(read_data="word1;word2;word1")):
            result = task_func("dummy_path.csv", ";")
        self.assertIn(("word1", 2), result)
        self.assertIn(("word2", 1), result)


if __name__ == "__main__":
    unittest.main()
