from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    location_name = Column(String(100), nullable=False)
    longitude = Column(Numeric(precision=100, scale=2))
    latitude = Column(Numeric(precision=100, scale=2))


class LocationDataGateway:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_location(self, location_name, longitude, latitude):
        try:
            location = Location(
                location_name=location_name, longitude=longitude, latitude=latitude
            )
            self.session.add(location)
            self.session.commit()
            return location.id
        except Exception as e:
            print("Error:", e)
            self.session.rollback()
            return None

    def get_location_list(self):
        try:
            locations = self.session.query(Location).all()
            if locations:
                return [
                    {
                        "id": location.id,
                        "location_name": location.location_name,
                        "longitude": location.longitude,
                        "latitude": location.latitude,
                    }
                    for location in locations
                ]

        except Exception as e:
            print("Error:", e)
            return None

    def get_location_by_id(self, location_id):
        try:
            location = (
                self.session.query(Location).filter(Location.id == location_id).first()
            )
            if location:
                return {
                    "id": location.id,
                    "location_name": location.location_name,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                }
            else:
                return None
        except Exception as e:
            print("Error:", e)
            return None

    def get_location_id_by_coordinates(self, latitude, longitude):
        """Query the Location table for the record with matching latitude and longitude"""
        location = (
            self.session.query(Location)
            .filter_by(latitude=latitude, longitude=longitude)
            .first()
        )

        if location:
            return location.id
        else:
            return None
