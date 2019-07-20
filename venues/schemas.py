from pydantic import BaseModel

from common.primitives import Venue, Review

class VenueCreate(Venue):
    pass


class VenueRead(Venue):
    id: int

    class Config:
        orm_mode = True


class ReviewCreate(Review):
    pass


class ReviewRead(Review):
    id: int

    class Config:
        orm_mode = True
