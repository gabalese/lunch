from geoalchemy2 import Geography
from shapely import wkb
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from common.primitives import Venue as VenueSchema, Review as ReviewSchema, Point
from venues.database import Base


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    foursquare_id = Column(String, unique=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    category = Column(String)
    coordinates = Column(Geography(geometry_type='POINT', srid=4326))

    reviews = relationship('Reviews', back_populates='venue', uselist=False)

    def to_dataclass(self) -> VenueSchema:
        coordinates = wkb.loads(bytes(self.coordinates.data))
        point = Point(coordinates.x, coordinates.y)
        return VenueSchema(
            foursquare_id=self.foursquare_id,
            name=self.name,
            address=self.address,
            city=self.city,
            category=self.category,
            coordinates=point,
            reviews=self.reviews.to_dataclass() if self.reviews else None
        )


class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    rating = Column(Float)
    reviews = Column(Integer)

    venue_id = Column(Integer, ForeignKey('venues.id'))
    venue = relationship('Venue', back_populates='reviews')

    def to_dataclass(self) -> ReviewSchema:
        return ReviewSchema(
            url=self.url,
            rating=self.rating,
            reviews=self.reviews
        )
