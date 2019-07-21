import re
from contextlib import contextmanager
from typing import Optional, Tuple
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.primitives import Venue, Review, GeoID

__all__ = [
    'search',
]

BASE_TRIPADVISOR_URL = 'https://www.tripadvisor.com'


@contextmanager
def selenium_webdriver():
    """
    Context manager to use a browser webdriver
    """

    options = Options()
    options.headless = True
    profile = FirefoxProfile()
    profile.set_preference('geo.enabled', True)
    profile.set_preference('geo.provider.use_corelocation', True)
    profile.set_preference('geo.prompt.testing', True)
    profile.set_preference('geo.prompt.testing.allow', True)
    driver = webdriver.Firefox(firefox_profile=profile, options=options)
    yield driver
    driver.close()


def get_venue_page_url(name: str, geoid: GeoID) -> str:
    """
    Scrape TA's website and return the restaurant URL
    Uses an actual browser session, so it might get really slow.

    :param name: venue name (doesn't need to be precise, TA will compensate for that
    :param geoid: the Tripadvisor GeoID for the city where the venue is
    """

    with selenium_webdriver() as driver:
        driver.get(
            f'https://www.tripadvisor.com/Search?geo={geoid.id}&redirect=&uiOrigin=MASTHEAD&q='
            f'{quote_plus(name)}&supportedSearchTypes=find_near_stand_alone_query'
        )
        try:
            # wait until it loads the results
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'result-content-columns'))
            WebDriverWait(driver, 20).until(element_present)
        except TimeoutException:
            return
        else:
            source = driver.page_source

    # select the first result from the search, 9/10 is the right one
    most_relevant = BeautifulSoup(source, features='html.parser').find_all('div', {'class': 'location-meta-block'})[0]
    attr = most_relevant.find('div', {'class': 'result-title'})['onclick']
    restaurant_page = re.search(r'/Restaurant_.+\.html', attr).group(0)

    return f"{BASE_TRIPADVISOR_URL}{restaurant_page}"


def get_reviews_from_url(url: str) -> Tuple[str, float, int]:
    """
    Fetch reviews data from a restaurant's tripadvisor page
    """

    response = requests.get(url)
    if not response.ok:
        return

    soup = BeautifulSoup(response.content, features='html.parser')
    venue_name = soup.find('div', {'class': 'restaurantName'}).find('h1').text

    average_rating = float(soup.find('span', {
        'class': 'restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl'}).text)
    number_of_reviews = int(
        re.search(
            r'(?<=\().+?(?=\))',
            soup.find('span', {'class': 'reviews_header_count'}).text.replace(',', '')).group(0)
    )

    return venue_name, average_rating, number_of_reviews


def get_geoid_from_city_name(city_name: str) -> Optional[GeoID]:
    """
    Tripadvisor requires a GeoID to make any search. A Geoid is a custom (presumably random?) identifier that maps
    1:1 with a city. A search for a place must be done for a specific city/region.
    """

    response = requests.get(
        url=f'{BASE_TRIPADVISOR_URL}/TypeAheadJson?action=API&query={city_name}&types=geo&name_depth=1&details=true&legacy_format=true&rescue=true&max=8&uiOrigin=Home_geopicker'
    )
    if not response.ok:
        return

    resp = response.json()
    most_relevant = resp[0]

    return GeoID(
        id=most_relevant['document_id'],
        city=most_relevant['details']['name'],
        county=most_relevant['details']['geo_name'],
        country=most_relevant['details']['grandparent_name']
    )


def get_reviews_for_venue(venue_name: str, city: str) -> Review:
    """
    A combiner method that gets a review object from a venue in a city
    """
    geoid = get_geoid_from_city_name(city)
    venue_url = get_venue_page_url(venue_name, geoid)
    name, average, reviews = get_reviews_from_url(venue_url)

    return Review(url=venue_url, rating=average, reviews=reviews)


def complete_venue_with_reviews(venue: Venue) -> Venue:
    """
    Given a venue with no reviews, attach some reviews to it
    """
    review = get_reviews_for_venue(venue.name, venue.city)
    venue.reviews = review
    return venue


def search(venue: Venue) -> Review:
    """
    Shorthand method for consistency with other modules
    """
    return get_reviews_for_venue(venue.name, venue.city)
