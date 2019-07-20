from typing import List

from sqlalchemy.orm import Session

from common.primitives import Venue, Point
from venues import models

from geoalchemy2 import func

def get_venues_around(db: Session, point: Point, radius: int, limit: int) -> List[Venue]:
    venues = db.query(models.Venue)\
        .filter(func.ST_DWithin(models.Venue.coordinates, point, radius))\
        .limit(limit)\
        .all()

    return [
        venue.to_dataclass() for venue in venues
    ]
