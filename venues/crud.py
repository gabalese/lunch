import logging
from typing import List

from geoalchemy2 import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.primitives import Venue, Point
from venues import find
from venues import models
from venues import utils


def get_db_venues_around(db: Session, point: Point, radius: int, limit: int) -> List[Venue]:
    venues = db.query(models.Venue) \
        .filter(
        func.ST_DWithin(
            models.Venue.coordinates,
            'SRID=4326;POINT({y} {x})'.format(x=point.lat, y=point.lon),
            radius)
    ) \
        .limit(limit) \
        .all()
    return [venue.to_dataclass() for venue in venues]


def get_venues_around(db: Session, point: Point, radius: int, limit: int) -> List[Venue]:
    logging.info('Getting venues...')
    venues = get_db_venues_around(db, point, radius, limit)
    if len(venues) < 5:
        logging.info(f'Got {len(venues)} venues')
        logging.info('Getting more venues from FQ...')
        additional_venues = find.search(point.lat, point.lon, rad=radius, limit=limit - len(venues))
        venues, duplicates = utils.remove_duplicates_by_key(venues + additional_venues, 'foursquare_id')
        if additional_venues:
            logging.info(f'Saving {len(additional_venues)} more venues...')
            save_venues(db, [models.Venue(**venue.dict()) for venue in additional_venues])
    return sorted(venues, key=lambda x: utils.distance_between_points(x.coordinates, point))


def save_venue(db: Session, venue: Venue) -> Venue:
    model = models.Venue(
        foursquare_id=venue.foursquare_id,
        name=venue.name,
        address=venue.address,
        city=venue.city,
        category=venue.category,
        coordinates=venue.coordinates.to_4326_wkt,
        reviews=venue.reviews
    )
    db.add(model)
    db.commit()
    return model.to_dataclass()


def save_venues(db: Session, venues: List[Venue]):
    """
    All of this because I don't know how to do a proper ON CONFLICT DO NULL
    when using a session and the ORM...
    """
    for venue in venues:
        try:
            save_venue(db, venue)
        except IntegrityError:
            db.rollback()
