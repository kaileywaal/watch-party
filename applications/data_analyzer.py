import os
from components.WeatherDataGateway import WeatherDataGateway
from components.SunshineRatioDataGateway import SunshineRatioDataGateway
from components.WeatherDataGateway import WeatherDataGateway


class WeatherAnalyzer:
    def __init__(self, weather_gateway, sunshine_ratio_gateway):
        self.weather_gateway = weather_gateway
        self.sunshine_ratio_gateway = sunshine_ratio_gateway

    def analyze_weather_data(self):
        weather_data_without_sunshine_ratio = (
            self.weather_gateway.get_unprocessed_weather()
        )

        for weather in weather_data_without_sunshine_ratio:
            sunshine_ratio = self.calculate_sunshine_to_daylight_ratio(weather)
            self.sunshine_ratio_gateway.add_data(weather["id"], sunshine_ratio)

    def calculate_sunshine_to_daylight_ratio(self, weather):
        return weather["sunshine_duration"] / weather["daylight_duration"]


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    db_path = os.getenv("DB_PATH")
    weather_gateway = WeatherDataGateway(db_path)
    sunshine_ratio_gateway = SunshineRatioDataGateway(db_path)

    analyzer = WeatherAnalyzer(weather_gateway, sunshine_ratio_gateway)
    print("Running analysis")
    analyzer.analyze_weather_data()
