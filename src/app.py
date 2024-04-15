from flask import Flask, request, render_template
from data_analyzer import analyze_weather_data
from data_collector import collect_weather_data_for_location
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from components.LocationDataGateway import LocationDataGateway
from components.WeatherDataGateway import WeatherDataGateway
from components.SunshineRatioDataGateway import SunshineRatioDataGateway


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
    collect_weather_data_for_location(location_1_id, get_formatted_date())
    location_1_analyzed_weather = (
        sunshine_ratio_gateway.get_sunshine_ratio_data_by_location(location_1_id)
    )

    location_2_id = request.form["location2"]
    # TODO: automate data collection apart from this request
    collect_weather_data_for_location(location_2_id, get_formatted_date())
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
