import logging

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from common.primitives import Point
from venues import crud
from venues.database import SessionLocal

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except Exception as e:
        logging.exception(e)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.get('/venues')
async def list_venues(lat: float, lon: float, radius: int = 1000, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_venues_around(db, Point(lat, lon), radius, limit)


@app.get('/venue/{foursquare_id}')
async def get_venue(foursquare_id: int):
    pass


@app.get('/')
async def index():
    return 'Mao'
