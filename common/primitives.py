from typing import Optional

from pydantic import BaseModel


class Point(BaseModel):
    lat: float
    lon: float

    @property
    def to_4326_wkt(self):
        return f'SRID=4326;POINT({self.lon} {self.lat})'



class GeoID(BaseModel):
    id: int
    city: str
    county: str
    country: str


class Review(BaseModel):
    url: str
    rating: float
    reviews: int


class Venue(BaseModel):
    foursquare_id: str
    name: str
    address: str
    city: str
    category: str
    coordinates: Point
    reviews: Optional[Review] = None

    def dict(self, **kwargs):
        return {
            'foursquare_id': self.foursquare_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'category': self.category,
            'coordinates': self.coordinates,
            'reviews': self.reviews
        }

