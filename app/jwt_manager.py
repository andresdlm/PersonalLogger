from jwt import encode, decode
from app.config.settings import settings

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=settings.jwt_secret, algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=settings.jwt_secret, algorithms=['HS256'])
    return data