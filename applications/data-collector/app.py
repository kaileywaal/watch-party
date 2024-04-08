from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

# https://open-meteo.com/en/docs/historical-weather-api/#start_date=2024-01-01&end_date=2024-04-08&hourly=sunshine_duration&daily=temperature_2m_max,temperature_2m_min,daylight_duration,sunshine_duration,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours&location_mode=csv_coordinates&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


SUPERIOR_CO_LATITUDE = 52.52
SUPERIOR_CO_LONGITUDE = 13.41
API_URL = (
    "https://archive-api.open-meteo.com/v1/archive?latitude="
    + str(SUPERIOR_CO_LATITUDE)
    + "&longitude="
    + str(SUPERIOR_CO_LONGITUDE)
    + "&start_date=2024-01-01&end_date=2024-04-08&daily=sunshine_duration&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.Numeric(precision=100, scale=2))
    latitude = db.Column(db.Numeric(precision=100, scale=2))


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    date = db.Column(db.String, nullable=False)
    sunshine_duration = db.Column(db.Numeric(precision=10000, scale=2))


# Create the table(s) in the database (if they don't already exist)
with app.app_context():
    db.create_all()


@app.route("/test")
def test_app():
    response = requests.get(API_URL).json()

    result_count = len(response["daily"]["time"])
    location_id = get_location_id_by_coordinates(
        response["latitude"], response["longitude"]
    )

    if not location_id:
        # add the locaiton here because the weather API slightly alters the latitude and longitude values once called
        location_id = add_location(
            location_name="Superior, CO",
            longitude=response["latitude"],
            latitude=response["longitude"],
        )

    for result in range(result_count):
        date = response["daily"]["time"][result]
        sunshine_duration = response["daily"]["sunshine_duration"][result]

        new_weather = Weather(
            date=date, sunshine_duration=sunshine_duration, location_id=location_id
        )
        db.session.add(new_weather)
        db.session.commit()
        print(new_weather)

    return response


def add_location(latitude, longitude, location_name):
    """Add a location value to the database by latitude and longitude"""
    new_location = Location(
        location_name=location_name, longitude=longitude, latitude=latitude
    )
    db.session.add(new_location)
    db.session.commit()
    return new_location.id


def get_location_id_by_coordinates(latitude, longitude):
    """Query the Location table for the record with matching latitude and longitude"""
    location = (
        db.session.query(Location)
        .filter_by(latitude=latitude, longitude=longitude)
        .first()
    )

    if location:
        return location.id
    else:
        return None


@app.route("/getWeatherData")
def get_weather():
    weather = Weather.query.all()
    return jsonify(
        [
            {
                "id": item.id,
                "location_id": item.location_id,
                "date": item.date,
                "sunshine_duration": item.sunshine_duration,
            }
            for item in weather
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)
