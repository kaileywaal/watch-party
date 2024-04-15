from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.schema_setup import SunshineRatio, Weather, Location


Base = declarative_base()


class SunshineRatioDataGateway:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_data(self, weather_id, sunshine_to_daylight_ratio):
        try:
            existing_data = (
                self.session.query(SunshineRatio).filter_by(weather_id=weather_id).all()
            )
            if existing_data:
                print(
                    f"Sunshine ratio data for weather_id {weather_id} already exists. Skipping..."
                )
                return None  # Skip adding the data

            sunshine_ratio = SunshineRatio(
                weather_id=weather_id,
                sunshine_to_daylight_ratio=sunshine_to_daylight_ratio,
            )
            self.session.add(sunshine_ratio)
            self.session.commit()
            print(print(f"Added sunshine_ratio data for weather_id {weather_id}."))
            return sunshine_ratio.id
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None

    def get_all_sunshine_ratio_data(self):
        try:
            sunshine_ratios = self.session.query(SunshineRatio).all()
            return [
                {
                    "id": sunshine_ratio.id,
                    "weather_id": sunshine_ratio.weather_id,
                    "sunshine_to_daylight_ratio": sunshine_ratio.sunshine_to_daylight_ratio,
                }
                for sunshine_ratio in sunshine_ratios
            ]
        except Exception as e:
            print("Error getting all sunshine ratio data")
            return None

    def get_sunshine_ratio_data_by_location(self, location_id):
        try:
            query_results = (
                self.session.query(SunshineRatio, Weather, Location)
                .join(Weather, SunshineRatio.weather_id == Weather.id)
                .join(Location, Weather.location_id == Location.id)
                .filter(Location.id == location_id)
            )

            result_list = []
            for sunshine_ratio, weather, location in query_results:
                result_list.append(
                    {
                        "sunshine_ratio_id": sunshine_ratio.id,
                        "sunshine_to_daylight_ratio": sunshine_ratio.sunshine_to_daylight_ratio,
                        "weather_id": weather.id,
                        "date": weather.date,
                        "location_id": location.id,
                        "location_name": location.location_name,
                        # Add more fields as needed
                    }
                )

            return result_list
        except Exception as e:
            print("Error getting sunshine ratio data:", e)
            return None
