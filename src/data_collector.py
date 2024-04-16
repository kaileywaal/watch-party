import datetime
import requests
from dotenv import load_dotenv
import os
from src.components.LocationDataGateway import LocationDataGateway, Location
from src.components.WeatherDataGateway import WeatherDataGateway
from src.data_analyzer import analyze_weather_data


load_dotenv()


class WeatherCollector:
    def __init__(
        self,
        location_gateway: LocationDataGateway,
        weather_gateway: WeatherDataGateway,
        start_date: datetime,
        end_date: datetime,
    ):
        self.location_gateway = location_gateway
        self.weather_gateway = weather_gateway
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def format_date(date: datetime):
        return date.strftime("%Y-%m-%d")

    def collect_weather_data_for_location(self, location_id):
        """Collect weather data from the API and store it in the database"""
        location = self.location_gateway.get_location_by_id(location_id)
        print("Collecting data for " + location["location_name"])

        api_url = self._build_api_url(location)

        try:
            response = requests.get(api_url).json()
            result_count = len(response["daily"]["time"])

            for result in range(result_count):
                date = response["daily"]["time"][result]
                sunshine_duration = response["daily"]["sunshine_duration"][result]
                daylight_duration = response["daily"]["daylight_duration"][result]

                self.weather_gateway.add_data(
                    date, sunshine_duration, location_id, daylight_duration
                )

            ## TODO: Call data analyzer here - eventually using RabbitMQ
            analyze_weather_data()

            return self.weather_gateway.get_weather_data_by_location(location_id)
        except Exception as e:
            print("Error collecting data:", e)

    def _build_api_url(self, location):
        return (
            "https://archive-api.open-meteo.com/v1/archive?latitude="
            + str(location["latitude"])
            + "&longitude="
            + str(location["longitude"])
            + "&start_date="
            + self.format_date(self.start_date)
            + "&end_date="
            + self.format_date(self.end_date)
            + "&daily=sunshine_duration,daylight_duration&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
        )


if __name__ == "__main__":
    location_gateway = LocationDataGateway(os.getenv("DB_PATH"))
    weather_gateway = WeatherDataGateway(os.getenv("DB_PATH"))

    # collector = WeatherCollector(location_gateway, weather_gateway)
    print("Collecting Data")
