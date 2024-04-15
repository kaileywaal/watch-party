from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from components.WeatherDataGateway import WeatherDataGateway
from components.LocationDataGateway import Location
from components.SunshineRatioDataGateway import SunshineRatioDataGateway
from components.WeatherDataGateway import WeatherDataGateway, Weather
import os

# Create an engine to connect to the SQLite database
engine = create_engine(os.getenv("DB_PATH"))

# Define a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

sunshine_ratio_gateway = SunshineRatioDataGateway(os.getenv("DB_PATH"))
weather_gateway = WeatherDataGateway(os.getenv("DB_PATH"))

# def get_sunshine_to_daylight_ratio(weather_data: Weather):
#     ''' Get an object with dates and their respective sunshine-to-daylight ratios'''
#     sunshine_to_daylight_ratio = {}

#     for weather in weather_data:
#         date = weather.date
#         sunshine_duration = float(weather.sunshine_duration)
#         daylight_duration = float(weather.daylight_duration)
#         # Avoid division by zero
#         if daylight_duration != 0:
#             ratio = sunshine_duration / daylight_duration
#             sunshine_to_daylight_ratio[date] = ratio

#     return sunshine_to_daylight_ratio


def analyze_weather_data():
    weather_data_without_sunshine_ratio = weather_gateway.get_unprocessed_weather()
    print(weather_data_without_sunshine_ratio)
    for weather in weather_data_without_sunshine_ratio:
        sunshine_ratio_gateway.add_data(
            weather["id"], get_sunshine_to_daylight_ratio(weather)
        )


def get_sunshine_to_daylight_ratio(weather):
    return weather["sunshine_duration"] / weather["daylight_duration"]

    # return [
    #     {
    #         "date": item["date"],
    #         "percent_sunny_of_possible_time": item["sunshine_duration"]
    #         / item["daylight_duration"],
    #     }
    #     for item in weather_data
    # ]


if __name__ == "__main__":
    print("Running analysis")
