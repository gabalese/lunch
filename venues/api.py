from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response

from common.primitives import Point
from venues import crud
from venues.database import SessionLocal

app = FastAPI()


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except:
        return Response('Server Error', status_code=500)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.route('/venues')
def list_venues(lat: int, lon: int, radius: int = 2000, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_venues_around(db, Point(lat, lon), radius, limit)


@app.route('/venue/{foursquare_id}')
def get_venue(foursquare_id: int):
    pass
