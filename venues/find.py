from typing import List

from foursquare import Foursquare

from common.primitives import Venue, Point
from config import FOURSQUARE_CLIENT_ID, FOURSQUARE_CLIENT_SECRET

__all__ = [
    'search'
]


class Categories:
    FOOD = '4d4b7105d754a06374d81259'
    BAR = '4bf58dd8d48988d116941735'  # includes pubs...


class LunchClient:
    def __init__(self, client_id: str, client_secret: str):
        self.fq = Foursquare(client_id=client_id, client_secret=client_secret)

    def search(self, lat: float, long: float, rad:int=2000, limit:int=50) -> List[Venue]:
        """
        Search FQ's api

        :param lat: Latitude
        :param long: Longitude
        :param rad: Radius to search in (when it's too wide, only the most relevant results will pop in)
        :param limit: How many venues to return
        :return: List of matched venues
        """

        venues = self.fq.venues.search({
            'll': f'{lat:.5},{long:.5}',
            'radius': rad,
            'categoryId': f'{Categories.FOOD},{Categories.BAR}',
            'intent': 'browse',
            'limit': limit
        })
        if not venues:
            return []

        ordered_venues = sorted(
            filter(lambda x: x['location'].get('city'), venues['venues']),
            key=lambda k: k['location']['distance']
        )
        return [
            Venue(foursquare_id=venue['id'], name=venue['name'],
                  address=", ".join(venue['location']['formattedAddress']),
                  city=", ".join(venue['location']['formattedAddress'][1:]),
                  category=venue['categories'][0]['name'],
                  coordinates=Point(venue['location']['lat'], venue['location']['lng']))
            for venue in ordered_venues
        ]


client = LunchClient(FOURSQUARE_CLIENT_ID, FOURSQUARE_CLIENT_SECRET)


def search(lat: float, long: float, rad:int=2000, limit:int=50) -> List[Venue]:
    """
    Search FQ's API using the supplied client wrapper
    """
    return client.search(lat, long, rad, limit)
