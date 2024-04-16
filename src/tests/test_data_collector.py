import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.data_collector import WeatherCollector


class TestWeatherCollector(unittest.TestCase):
    def setUp(self):
        self.location_gateway = MagicMock()
        self.weather_gateway = MagicMock()
        self.start_date = datetime(2024, 1, 1)
        self.end_date = datetime(2024, 1, 5)
        self.collector = WeatherCollector(
            self.location_gateway, self.weather_gateway, self.start_date, self.end_date
        )

    @patch("requests.get")
    def test_collect_weather_data_for_location(self, mock_requests_get):
        location_id = 1
        mock_location = {
            "location_name": "Test Location",
            "latitude": 40.0,
            "longitude": -75.0,
        }
        mock_weather_data = {
            "daily": {
                "time": ["2024-01-01", "2024-01-02"],
                "sunshine_duration": [25500, 17000],
                "daylight_duration": [34000, 34000],
            }
        }
        mock_requests_get.return_value.json.return_value = mock_weather_data
        self.location_gateway.get_location_by_id.return_value = mock_location

        self.collector.collect_weather_data_for_location(location_id)

        # Check that weather data is added to the gateway
        self.weather_gateway.add_data.assert_any_call(
            "2024-01-01", 25500, location_id, 34000
        )
        self.weather_gateway.add_data.assert_any_call(
            "2024-01-02", 17000, location_id, 34000
        )

        # Check that analyze_weather_data is called
        self.weather_gateway.get_weather_data_by_location.assert_called_with(
            location_id
        )

    def test__build_api_url(self):
        location = {"latitude": 40.0, "longitude": -75.0}
        expected_url = "https://archive-api.open-meteo.com/v1/archive?latitude=40.0&longitude=-75.0&start_date=2024-01-01&end_date=2024-01-05&daily=sunshine_duration,daylight_duration&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
        api_url = self.collector._build_api_url(location)
        self.assertEqual(api_url, expected_url)


if __name__ == "__main__":
    unittest.main()
