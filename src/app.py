from flask import Flask, request, render_template
from data_analyzer import analyze_weather_data_for_location
import json
import os
from components.LocationDataGateway import LocationDataGateway
from components.WeatherDataGateway import WeatherDataGateway
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
location_gateway = LocationDataGateway(os.getenv("DB_PATH"))
weather_gateway = WeatherDataGateway(os.getenv("DB_PATH"))


@app.route("/")
def main():

    # locations_file_path = os.path.join("src", "data", "locations.json")
    # with open(locations_file_path, "r") as f:
    #     locations = json.load(f)

    print(location_gateway.get_location_list())

    return render_template("index.html", locations=location_gateway.get_location_list())

    # if request.method == "GET":
    #     return analyze_weather_data_for_location("Superior, CO")


@app.route("/get-weather-data", methods=["POST"])
def get_data_for_location():
    location_id = request.form["location"]
    weather = weather_gateway.get_weather_data_by_location(location_id)
    return weather


if __name__ == "__main__":
    app.run(debug=True)
