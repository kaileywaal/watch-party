from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from components.WeatherDataGateway import Weather
from components.LocationDataGateway import Location

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///weather.db")

# Define a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


def analyze_weather_data_for_location(location_name: str):
    data = get_weather_data_by_location_name(location_name)
    print(data)
    return [
        {
            "date": item["date"],
            "percent_sunny_of_possible_time": item["sunshine_duration"]
            / item["daylight_duration"],
        }
        for item in data
    ]


def get_weather_data_by_location_name(location_name: str):
    """Retrieve weather data by the latitude and longitude"""
    location_id = get_location_id_by_name(location_name)

    weather = session.query(Weather).filter_by(location_id=location_id)
    return [
        {
            "id": item.id,
            "location_id": item.location_id,
            "date": item.date,
            "sunshine_duration": item.sunshine_duration,
            "daylight_duration": item.daylight_duration,
        }
        for item in weather
    ]


def get_location_id_by_name(location_name):
    """Retrieve location data from the database by ID"""
    location = session.query(Location).filter_by(location_name=location_name).first()
    if location:
        return location.id
    else:
        return None


if __name__ == "__main__":
    print(analyze_weather_data_for_location("Superior, CO"))
