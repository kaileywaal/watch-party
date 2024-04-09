from flask import Flask, request, render_template
from data_analyzer import analyze_weather_data_for_location

app = Flask(__name__)


@app.route("/")
def main():
    if request.method == "GET":
        return analyze_weather_data_for_location("Superior, CO")


if __name__ == "__main__":
    app.run(debug=True)
