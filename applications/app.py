from flask import Flask, request, render_template
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from applications.data_collector import WeatherCollector
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


# TODO: automate data collection apart from this request
def trigger_weather_collection():
    collector = WeatherCollector(
        location_gateway,
        weather_gateway,
        get_date_x_days_ago(90),
        get_date_x_days_ago(2),
    )
    collector.collect_weather_data_for_location(1)
    collector.collect_weather_data_for_location(2)
    collector.collect_weather_data_for_location(3)
    collector.collect_weather_data_for_location(4)


@app.route("/get-weather-data", methods=["POST"])
def get_data_for_location():
    location_1_id = request.form["location1"]

    location_1_analyzed_weather = (
        sunshine_ratio_gateway.get_sunshine_ratio_data_by_location(location_1_id)
    )

    location_2_id = request.form["location2"]

    location_2_analyzed_weather = (
        sunshine_ratio_gateway.get_sunshine_ratio_data_by_location(location_2_id)
    )

    return render_template(
        "weather-data.html",
        location_1_analyzed_weather=location_1_analyzed_weather,
        location_2_analyzed_weather=location_2_analyzed_weather,
    )


def get_date_x_days_ago(days_ago):
    return datetime.today() - timedelta(days=days_ago)


if __name__ == "__main__":
    trigger_weather_collection()
    app.run(debug=True)
