from flask import Flask, request, render_template
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from src.data_collector import WeatherCollector
from src.components.LocationDataGateway import LocationDataGateway
from src.components.WeatherDataGateway import WeatherDataGateway
from src.components.SunshineRatioDataGateway import SunshineRatioDataGateway


load_dotenv()

app = Flask(__name__)
location_gateway = LocationDataGateway(os.getenv("DB_PATH"))
weather_gateway = WeatherDataGateway(os.getenv("DB_PATH"))
sunshine_ratio_gateway = SunshineRatioDataGateway(os.getenv("DB_PATH"))


@app.route("/")
def main():
    return render_template("index.html", locations=location_gateway.get_location_list())


@app.route("/get-weather-data", methods=["POST"])
def get_data_for_location():
    location_1_id = request.form["location1"]

    # TODO: automate data collection apart from this request
    collector = WeatherCollector(
        location_gateway, weather_gateway, "2024-01-01", get_formatted_date()
    )
    collector.collect_weather_data_for_location(location_1_id)
    location_1_analyzed_weather = (
        sunshine_ratio_gateway.get_sunshine_ratio_data_by_location(location_1_id)
    )

    location_2_id = request.form["location2"]
    # TODO: automate data collection apart from this request
    collector.collect_weather_data_for_location(location_2_id)
    location_2_analyzed_weather = (
        sunshine_ratio_gateway.get_sunshine_ratio_data_by_location(location_2_id)
    )

    return render_template(
        "weather-data.html",
        location_1_analyzed_weather=location_1_analyzed_weather,
        location_2_analyzed_weather=location_2_analyzed_weather,
    )


def get_formatted_date():
    """Get date of two days ago formatted as "YYYY-MM-DD" (API has delayed data)"""
    return (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")


if __name__ == "__main__":
    app.run(debug=True)
