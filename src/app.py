from flask import Flask, request, render_template
from data_analyzer import analyze_weather_data_for_location
import json
import os

app = Flask(__name__)


@app.route("/")
def main():
    locations_file_path = os.path.join("src", "data", "locations.json")
    with open(locations_file_path, "r") as f:
        locations = json.load(f)

    return render_template("index.html", locations=locations)

    # if request.method == "GET":
    #     return analyze_weather_data_for_location("Superior, CO")


@app.route("/get-weather-data", methods=["POST"])
def get_data_for_location():
    location = request.form["location"]
    return location


if __name__ == "__main__":
    app.run(debug=True)
