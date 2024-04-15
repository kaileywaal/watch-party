import unittest
from src.data_analyzer import get_sunshine_to_daylight_ratio


class TestDataAnalyzer(unittest.TestCase):
    def test_get_sunshine_to_daylight_ratio(self):
        mock_weather = {
            "id": 1,
            "location_id": 1,
            "date": "2024-01-01",
            "sunshine_duration": 0.40,
            "daylight_duration": 0.80,
        }

        mock_weather_2 = {
            "id": 2,
            "location_id": 2,
            "date": "2024-01-01",
            "sunshine_duration": 0,
            "daylight_duration": 0.80,
        }

        self.assertEqual(get_sunshine_to_daylight_ratio(mock_weather), 0.5)
        self.assertEqual(get_sunshine_to_daylight_ratio(mock_weather_2), 0)


if __name__ == "__main__":
    unittest.main()
