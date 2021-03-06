from unittest import mock

import pytest

import reviews
import venues
from common.primitives import Venue, Point


@pytest.fixture
def venue():
    return Venue(
        foursquare_id='Nothing',
        name='Meo Pinelli',
        address='Not important',
        city='Rome, Italy',
        category='Pub',
        coordinates=Point(lat=0, lon=0),
        reviews=None
    )


def test_api_gets_venues():
    places = venues.search(41.8532354, 12.5662685, limit=10, rad=1000)

    assert places
    assert places[0].name == 'Alice pizza'


def test_get_reviews(venue):
    with mock.patch('reviews.find.get_venue_page_url') as mock_find_venue:
        mock_find_venue.return_value = 'https://www.tripadvisor.co.uk/Restaurant_Review-g186363-d786796-Reviews-L_Ortolan-Reading_Berkshire_England.html'
        review = reviews.search(venue)

    assert review.reviews

    assert review.rating
    assert review.reviews != 0
