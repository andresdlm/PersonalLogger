from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from app.dtos.movie import Movie
from app.models.movie import Movie as MovieModel
from app.config.database import SessionLocal
from app.middlewares.jwt_bearer import JWTBearer


movie_router = APIRouter(tags=["Movies"])


@movie_router.get("/movies", response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = SessionLocal()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get("/{id}", response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = SessionLocal()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post("/", response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = SessionLocal()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Movie has been created"})


@movie_router.put("/{id}", response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = SessionLocal()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Movie has been modified"})


@movie_router.delete("/{id}", response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = SessionLocal()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Movie has been deleted"})
