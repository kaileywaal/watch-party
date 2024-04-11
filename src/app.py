from flask import Flask, request, render_template
import json
import os
from components.LocationDataGateway import LocationDataGateway
from components.WeatherDataGateway import WeatherDataGateway
from data_analyzer import analyze_weather_data
from data_collector import collect_weather_data_for_location
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
location_gateway = LocationDataGateway(os.getenv("DB_PATH"))
weather_gateway = WeatherDataGateway(os.getenv("DB_PATH"))


@app.route("/")
def main():
    return render_template("index.html", locations=location_gateway.get_location_list())


@app.route("/get-weather-data", methods=["POST"])
def get_data_for_location():
    location_id = request.form["location"]
    collect_weather_data_for_location(location_id)

    weather = weather_gateway.get_weather_data_by_location(location_id)
    return analyze_weather_data(weather)


if __name__ == "__main__":
    app.run(debug=True)
