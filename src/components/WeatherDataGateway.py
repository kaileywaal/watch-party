from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from schema_setup import Weather


Base = declarative_base()


class WeatherDataGateway:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_data(self, date, sunshine_duration, location_id, daylight_duration):
        try:
            weather = Weather(
                date=date,
                sunshine_duration=sunshine_duration,
                location_id=location_id,
                daylight_duration=daylight_duration,
            )
            self.session.add(weather)
            self.session.commit()
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

    # def get_location_list(self):
    #     try:
    #         locations = self.session.query(Location).all()
    #         if locations:
    #             return [
    #                 {
    #                     "id": location.id,
    #                     "location_name": location.location_name,
    #                     "longitude": location.longitude,
    #                     "latitude": location.latitude,
    #                 }
    #                 for location in locations
    #             ]

    #     except Exception as e:
    #         print("Error:", e)
    #         return None

    # def get_location_by_id(self, location_id):
    #     try:
    #         location = (
    #             self.session.query(Location).filter(Location.id == location_id).first()
    #         )
    #         if location:
    #             return {
    #                 "id": location.id,
    #                 "location_name": location.location_name,
    #                 "longitude": location.longitude,
    #                 "latitude": location.latitude,
    #             }
    #         else:
    #             return None
    #     except Exception as e:
    #         print("Error:", e)
    #         return None

    # def get_location_id_by_coordinates(self, latitude, longitude):
    #     """Query the Location table for the record with matching latitude and longitude"""
    #     location = (
    #         self.session.query(Location)
    #         .filter_by(latitude=latitude, longitude=longitude)
    #         .first()
    #     )

    #     if location:
    #         return location.id
    #     else:
    #         return None
