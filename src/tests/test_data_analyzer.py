import unittest
from unittest.mock import MagicMock
from src.data_analyzer import WeatherAnalyzer


class TestWeatherAnalyzer(unittest.TestCase):
    def test_calculate_sunshine_to_daylight_ratio(self):
        weather = {"sunshine_duration": 0.3, "daylight_duration": 0.6}
        analyzer = WeatherAnalyzer(None, None)
        ratio = analyzer.calculate_sunshine_to_daylight_ratio(weather)
        self.assertEqual(ratio, 0.5)

    def test_analyze_weather_data(self):
        mock_weather_gateway = MagicMock()
        mock_sunshine_ratio_gateway = MagicMock()

        mock_weather_data = [
            {"id": 1, "sunshine_duration": 25500, "daylight_duration": 34000},
            {"id": 2, "sunshine_duration": 0, "daylight_duration": 34000},
            {"id": 3, "sunshine_duration": 17000, "daylight_duration": 34000},
        ]
        mock_weather_gateway.get_unprocessed_weather.return_value = mock_weather_data

        analyzer = WeatherAnalyzer(mock_weather_gateway, mock_sunshine_ratio_gateway)
        analyzer.analyze_weather_data()

        # Ensure add_data method is called for each weather entry
        mock_sunshine_ratio_gateway.add_data.assert_any_call(1, 0.75)
        mock_sunshine_ratio_gateway.add_data.assert_any_call(2, 0.0)
        mock_sunshine_ratio_gateway.add_data.assert_any_call(3, 0.5)


if __name__ == "__main__":
    unittest.main()
