from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.config.database import engine, Base
from app.middlewares.error_handler import ErrorHandler
from app.routers.movie import movie_router
from app.dtos.user import User
from app.jwt_manager import create_token


app = FastAPI(title="Personal Logger", version="0.0.1")
app.add_middleware(ErrorHandler)
app.include_router(movie_router, prefix='/movies')

Base.metadata.create_all(bind=engine)

@app.post('/auth/login', tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")