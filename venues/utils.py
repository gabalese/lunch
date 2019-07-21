from typing import List

import geopy.distance

from common.primitives import Point


def distance_between_points(point_a: Point, point_b: Point) -> float:  # meters!
    return geopy.distance.geodesic((point_a.lat, point_a.lon), (point_b.lat, point_b.lon)).meters


def remove_duplicates_by_key(iterable: List, key: str):
    mapping = {}
    duplicates = {}
    for item in iterable:
        if not mapping.get(getattr(item, key)):
            mapping[getattr(item, key)] = item
        else:
            duplicates[getattr(item, key)] = item

    return mapping.values(), duplicates.values()


