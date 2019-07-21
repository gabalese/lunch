from common.primitives import Venue, Point
from venues.utils import remove_duplicates_by_key

def test_deduplicate():
    list_of_venues = [
        Venue(foursquare_id='1', name='Meo Pinelli', address='Boh', city='Rome',
                     coordinates=Point(12.5661652, 41.8533015), category='Pub'),
        Venue(foursquare_id='2', name='Trattoria Magnaroma', address='Boh', city='Rome',
                     coordinates=Point(12.5647114, 41.8521487), category='Pub'),
        Venue(foursquare_id='3', name='La Francescana', address='Boh', city='Rome',
                     coordinates=Point(12.4416217,41.965139), category='Pub'),
        Venue(foursquare_id='4', name='Subaugusta itself', address='Boh', city='Rome',
                     coordinates=Point(12.5630055, 41.8515414), category='Stazione'),
        Venue(foursquare_id='3', name='La Francescana', address='Boh', city='Rome',
              coordinates=Point(12.4416217, 41.965139), category='Pub'),
    ]

    no_duplicates, duplicates = remove_duplicates_by_key(list_of_venues, 'foursquare_id')
    assert len(no_duplicates) == 4
    assert len(duplicates) == 1

