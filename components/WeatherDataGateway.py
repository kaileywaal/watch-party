from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from applications.schema_setup import Weather, SunshineRatio


Base = declarative_base()


class WeatherDataGateway:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_data(self, date, sunshine_duration, location_id, daylight_duration):
        try:
            existing_data = (
                self.session.query(Weather)
                .filter_by(date=date, location_id=location_id)
                .first()
            )
            if existing_data:
                print(
                    f"Data for location {location_id} on date {date} already exists. Skipping..."
                )
                return None  # Skip adding the data

            weather = Weather(
                date=date,
                sunshine_duration=sunshine_duration,
                location_id=location_id,
                daylight_duration=daylight_duration,
            )
            self.session.add(weather)
            self.session.commit()
            print(
                print(f"Added weather data for location {location_id} on date {date}.")
            )
            return weather.id
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None

    def get_all_weather_data(self):
        try:
            weather = self.session.query(Weather).all()
            return [
                {
                    "id": item.id,
                    "location_id": item.location_id,
                    "date": item.date,
                    "sunshine_duration": item.sunshine_duration,
                    "daylight_duration": item.daylight_duration,
                }
                for item in weather
            ]
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None

    def get_weather_data_by_location(self, location_id):
        try:
            weather = self.session.query(Weather).filter_by(location_id=location_id)
            return [
                {
                    "id": item.id,
                    "location_id": item.location_id,
                    "date": item.date,
                    "sunshine_duration": item.sunshine_duration,
                    "daylight_duration": item.daylight_duration,
                }
                for item in weather
            ]
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None

    def get_unprocessed_weather(self):
        """Get weather items that have not yet been analyzed"""
        try:
            unprocessed_weather = (
                self.session.query(Weather)
                .outerjoin(SunshineRatio, SunshineRatio.weather_id == Weather.id)
                .filter(
                    SunshineRatio.id.is_(None)
                )  # Filter for rows where SunshineRatio object is None
                .all()
            )

            return [
                {
                    "id": item.id,
                    "location_id": item.location_id,
                    "date": item.date,
                    "sunshine_duration": item.sunshine_duration,
                    "daylight_duration": item.daylight_duration,
                }
                for item in unprocessed_weather
            ]
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None
