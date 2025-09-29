from main import *
import unittest
import unittest.mock as mock
import socket
import requests


class TestCases(unittest.TestCase):
    @mock.patch("socket.gethostbyname")
    @mock.patch("requests.get")
    def test_valid_host(self, mock_get, mock_gethostbyname):
        # Simulates a valid response scenario.
        mock_gethostbyname.return_value = "8.8.8.8"
        mock_get.return_value = mock.Mock(
            status_code=200, json=lambda: {"city": "Mountain View", "country": "US"}
        )
        result = task_func("google.com")
        self.assertIn("ip_address", result)
        self.assertIn("geolocation", result)
        self.assertEqual(result["ip_address"], "8.8.8.8")
        self.assertEqual(
            result["geolocation"], {"city": "Mountain View", "country": "US"}
        )

    def test_invalid_host(self):
        # Checks for handling of empty strings as host.
        with self.assertRaises(ValueError):
            task_func("")

    def test_invalid_host_none(self):
        # Checks for handling None as host.
        with self.assertRaises(ValueError):
            task_func(None)

    @mock.patch("socket.gethostbyname")
    def test_connection_error(self, mock_gethostbyname):
        # Simulates a DNS resolution error.
        mock_gethostbyname.side_effect = socket.gaierror
        with self.assertRaises(ConnectionError):
            task_func("invalidhost.com")

    @mock.patch("socket.gethostbyname")
    @mock.patch("requests.get")
    def test_http_error(self, mock_get, mock_gethostbyname):
        # Simulates an HTTP error from the geolocation service.
        mock_gethostbyname.return_value = "8.8.8.8"
        mock_get.return_value = mock.Mock(status_code=500)
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError
        with self.assertRaises(ConnectionError):
            task_func("example.com")

    @mock.patch("socket.gethostbyname")
    @mock.patch("requests.get")
    def test_nonexistent_host(self, mock_get, mock_gethostbyname):
        # Simulates a DNS error for a nonexistent domain.
        mock_gethostbyname.side_effect = socket.gaierror
        with self.assertRaises(ConnectionError):
            task_func("nonexistentdomain.com")


if __name__ == "__main__":
    unittest.main()
