from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os, json


load_dotenv()

engine = create_engine(os.getenv("DB_PATH"))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# SQLAlchemy models
class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False)
    longitude = Column(Numeric(precision=100, scale=2))
    latitude = Column(Numeric(precision=100, scale=2))


class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    date = Column(String, nullable=False)
    sunshine_duration = Column(Numeric(precision=10000, scale=2), nullable=False)
    daylight_duration = Column(Numeric(precision=10000, scale=2), nullable=False)


def setup_schema():
    # Create tables
    Base.metadata.create_all(engine)

    # TODO: add logic here to add initial data to the database
    locations_file_path = os.path.join("src", "data", "locations.json")
    with open(locations_file_path, "r") as f:
        locations = json.load(f)
        for location_data in locations:
            location = Location(
                location_name=location_data["name"],
                longitude=location_data["longitude"],
                latitude=location_data["latitude"],
            )
            session.add(location)
        session.commit()


if __name__ == "__main__":
    # Call the setup_schema function when the script is executed
    setup_schema()
