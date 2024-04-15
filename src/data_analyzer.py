from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from components.WeatherDataGateway import WeatherDataGateway
from components.SunshineRatioDataGateway import SunshineRatioDataGateway
from components.WeatherDataGateway import WeatherDataGateway
import os

# Create an engine to connect to the SQLite databasex
engine = create_engine(os.getenv("DB_PATH"))

# Define a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

sunshine_ratio_gateway = SunshineRatioDataGateway(os.getenv("DB_PATH"))
weather_gateway = WeatherDataGateway(os.getenv("DB_PATH"))


def analyze_weather_data():
    weather_data_without_sunshine_ratio = weather_gateway.get_unprocessed_weather()
    print(weather_data_without_sunshine_ratio)
    for weather in weather_data_without_sunshine_ratio:
        sunshine_ratio_gateway.add_data(
            weather["id"], get_sunshine_to_daylight_ratio(weather)
        )


def get_sunshine_to_daylight_ratio(weather):
    return weather["sunshine_duration"] / weather["daylight_duration"]


if __name__ == "__main__":
    print("Running analysis")
