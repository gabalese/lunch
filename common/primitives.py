from dataclasses import dataclass
from typing import Optional


@dataclass
class Point:
    lat: float
    lon: float


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
