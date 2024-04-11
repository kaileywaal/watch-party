from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from components.WeatherDataGateway import Weather
from components.LocationDataGateway import Location
import os

# Create an engine to connect to the SQLite database
engine = create_engine(os.getenv("DB_PATH"))

# Define a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


def analyze_weather_data(weather_data: Weather):
    return [
        {
            "date": item["date"],
            "percent_sunny_of_possible_time": item["sunshine_duration"]
            / item["daylight_duration"],
        }
        for item in weather_data
    ]


if __name__ == "__main__":
    print("Running analysis")
