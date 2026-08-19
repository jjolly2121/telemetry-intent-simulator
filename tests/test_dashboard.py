import unittest

from mission_control import app


class DashboardTests(unittest.TestCase):
    def test_dashboard_route_is_available(self):
        response = app.test_client().get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mission Control Dashboard", response.data)


if __name__ == "__main__":
    unittest.main()
