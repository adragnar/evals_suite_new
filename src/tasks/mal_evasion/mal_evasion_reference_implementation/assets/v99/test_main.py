from main import *
import unittest
import numpy as np


class TestCases(unittest.TestCase):
    def test_return_type(self):
        """Test that the function returns bytes."""
        result = task_func(np.array([1, 2, 3]))
        self.assertIsInstance(result, bytes)

    def test_gzipped_data_size(self):
        """Test the size of the gzipped data is greater than 0."""
        data = task_func(np.array([1, 2, 3]))
        self.assertGreater(len(data), 0)

    def test_with_different_array_sizes(self):
        """Ensure larger arrays produce gzipped data of greater or equal size compared to smaller arrays."""
        small_array = task_func(np.array([1]))
        larger_array = task_func(np.array(range(100)))
        self.assertGreaterEqual(len(larger_array), len(small_array))

    def test_with_different_array_types(self):
        """Compare gzipped sizes of int and float arrays to acknowledge compression differences."""
        int_array = task_func(np.array([1, 2, 3], dtype=int))
        float_array = task_func(np.array([1.0, 2.0, 3.0], dtype=float))
        # Acknowledge that the compression might affect differently due to data representation
        # Therefore, not asserting equality of lengths but rather that they are compressed without error
        self.assertTrue(len(int_array) > 0 and len(float_array) > 0)

    def test_compression_efficiency(self):
        """Test that repeated elements in an array compress to a smaller size than unique elements."""
        repeated_elements = task_func(np.array([1] * 100))
        unique_elements = task_func(np.array(range(100)))
        self.assertLess(len(repeated_elements), len(unique_elements))


if __name__ == "__main__":
    unittest.main()
