from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from src.components.WeatherDataGateway import WeatherDataGateway
from src.components.SunshineRatioDataGateway import SunshineRatioDataGateway
from src.components.WeatherDataGateway import WeatherDataGateway


sunshine_ratio_gateway = SunshineRatioDataGateway(os.getenv("DB_PATH"))
weather_gateway = WeatherDataGateway(os.getenv("DB_PATH"))


def analyze_weather_data():
    weather_data_without_sunshine_ratio = weather_gateway.get_unprocessed_weather()

    for weather in weather_data_without_sunshine_ratio:
        sunshine_ratio_gateway.add_data(
            weather["id"], get_sunshine_to_daylight_ratio(weather)
        )


def get_sunshine_to_daylight_ratio(weather):
    return weather["sunshine_duration"] / weather["daylight_duration"]


if __name__ == "__main__":
    print("Running analysis")
    analyze_weather_data()
