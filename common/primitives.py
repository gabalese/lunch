from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class Point:
    lat: float
    lon: float

    @property
    def to_4326_wkt(self):
        return f'SRID=4326;POINT({self.lon} {self.lat})'


@dataclass
class GeoID:
    id: int
    city: str
    county: str
    country: str


@dataclass
class Review:
    url: str
    rating: float
    reviews: int


@dataclass
class Venue:
    foursquare_id: str
    name: str
    address: str
    city: str
    category: str
    coordinates: Point
    reviews: Optional[Review] = None
