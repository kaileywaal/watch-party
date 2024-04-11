from flask import Flask, request, render_template
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
    location_1_id = request.form["location1"]
    location_1_name = location_gateway.get_location_by_id(location_1_id)[
        "location_name"
    ]
    location_1_weather = collect_weather_data_for_location(location_1_id)
    location_1_analyzed_weather = analyze_weather_data(location_1_weather)

    location_2_id = request.form["location2"]
    location_2_name = location_gateway.get_location_by_id(location_2_id)[
        "location_name"
    ]
    location_2_weather = collect_weather_data_for_location(location_2_id)
    location_2_analyzed_weather = analyze_weather_data(location_2_weather)

    return render_template(
        "weather-data.html",
        location_1_name=location_1_name,
        location_1_analyzed_weather=location_1_analyzed_weather,
        location_2_name=location_2_name,
        location_2_analyzed_weather=location_2_analyzed_weather,
    )


if __name__ == "__main__":
    app.run(debug=True)
