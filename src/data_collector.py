import requests
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from components.LocationDataGateway import LocationDataGateway
from components.WeatherDataGateway import WeatherDataGateway
from dotenv import load_dotenv
import os


load_dotenv()

# API constants
SUPERIOR_CO_LATITUDE = 52.52
SUPERIOR_CO_LONGITUDE = 13.41
API_URL = (
    "https://archive-api.open-meteo.com/v1/archive?latitude="
    + str(SUPERIOR_CO_LATITUDE)
    + "&longitude="
    + str(SUPERIOR_CO_LONGITUDE)
    + "&start_date=2024-01-01&end_date=2024-04-08&daily=sunshine_duration,daylight_duration&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
)


location_gateway = LocationDataGateway(os.getenv("DB_PATH"))
weather_gateway = WeatherDataGateway(os.getenv("DB_PATH"))


# def add_location(latitude, longitude, location_name):
#     """Add a location value to the database by latitude and longitude and return ID of newly created location"""
#     new_location = Location(
#         location_name=location_name, longitude=longitude, latitude=latitude
#     )
#     session.add(new_location)
#     session.commit()
#     return new_location.id


# def get_location_id_by_coordinates(latitude, longitude):
#     """Query the Location table for the record with matching latitude and longitude"""
#     location = (
#         session.query(Location)
#         .filter_by(latitude=latitude, longitude=longitude)
#         .first()
#     )

#     if location:
#         return location.id
#     else:
#         return None


def collect_weather_data():
    """Collect weather data from the API and store it in the database"""
    print("collecting data")
    response = requests.get(API_URL).json()

    result_count = len(response["daily"]["time"])
    location_id = location_gateway.get_location_id_by_coordinates(
        response["latitude"], response["longitude"]
    )

    if not location_id:
        location_id = location_gateway.add_location(
            "Superior, CO", response["latitude"], response["longitude"]
        )

    for result in range(result_count):
        date = response["daily"]["time"][result]
        sunshine_duration = response["daily"]["sunshine_duration"][result]
        daylight_duration = response["daily"]["daylight_duration"][result]

        weather_gateway.add_data(
            date, sunshine_duration, location_id, daylight_duration
        )


# def get_weather_data():
#     """Retrieve all weather data from the database"""
#     weather = session.query(Weather).all()
#     return [
#         {
#             "id": item.id,
#             "location_id": item.location_id,
#             "date": item.date,
#             "sunshine_duration": item.sunshine_duration,
#             "daylight_duration": item.daylight_duration,
#         }
#         for item in weather
#     ]


if __name__ == "__main__":
    collect_weather_data()  # Collect weather data when the script is run
    print(location_gateway.get_location_list())
    print(weather_gateway.get_all_weather_data())
