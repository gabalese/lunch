import requests

from common.primitives import Point

BASE_SEARCH = "https://locationiq.com/v1/search_sandbox.php?format=json&q={query}&accept-language=en"


def search(location: str) -> Point:
    resp = requests.get(BASE_SEARCH.format(query=location))
    if resp.ok:
        locations = resp.json()
        lat, lon = locations[0]['lat'], locations[0]['lon']  # we'll assume that the first location is the right one
        return Point(lat=float(lat), lon=float(lon))
