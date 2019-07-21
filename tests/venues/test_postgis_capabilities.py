import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.primitives import Point
from venues.database import Base
from venues import models
from common import primitives
from venues import crud


@pytest.fixture(scope='session')
def engine():
    return create_engine('postgresql://postgres:postgres@localhost/test')  # test must be created beforehand

@pytest.yield_fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.yield_fixture(scope='session')
def dbsession(engine, tables):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    yield session
    session.close()


def test_can_create_venues(dbsession):
    venues = [
        models.Venue(foursquare_id='1', name='Meo Pinelli', address='Boh', city='Rome', coordinates='POINT(12.5661652 41.8533015)', category='Pub'),
        models.Venue(foursquare_id='2', name='Trattoria Magnaroma', address='Boh', city='Rome', coordinates='POINT(12.5647114 41.8521487)', category='Pub'),
        models.Venue(foursquare_id='3', name='La Francescana', address='Boh', city='Rome', coordinates='POINT(12.4416217 41.965139)', category='Pub'),
        models.Venue(foursquare_id='4', name='Subaugusta itself', address='Boh', city='Rome', coordinates='POINT(12.5630055 41.8515414)', category='Stazione'),
        models.Venue(foursquare_id='5', name='Altro ristorante a cazzo', address='Boh', city='Rome', coordinates='POINT(12.4416217 41.965139)', category='Stazione')
    ]

    dbsession.bulk_save_objects(venues)
    dbsession.commit()

    all_venues = dbsession.query(models.Venue).all()
    assert len(all_venues) == 5

    venues_around = crud.get_db_venues_around(dbsession, Point(41.8515414, 12.5630055), radius=200, limit=10)
    assert len(venues_around) == 2


def test_can_get_venues(dbsession):
    venues_around = crud.get_venues_around(dbsession, Point(41.8515414, 12.5630055), radius=200, limit=10)
    assert len(venues_around) == 8


def test_can_save_venues(dbsession):
    venue = primitives.Venue(
        name='Meo Pinelli',
        foursquare_id='78',
        address='Boh',
        city='Rome',
        category='Pub',
        coordinates=primitives.Point(41.8533015, 12.5661652),
        reviews=None
    )
    saved = crud.save_venue(dbsession, venue)
    assert saved
