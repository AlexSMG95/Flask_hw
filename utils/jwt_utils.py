import jwt
from datetime import datetime, timedelta
from config import Config

config = Config.from_env()

def create_access_token(identity: str) -> str:
    """Создание JWT токена"""
    payload = {
        'identity': identity,
        'exp': datetime.utcnow() + timedelta(
            seconds=config.JWT_EXPIRATION_DELTA_SECONDS
        ),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )

    return token

def decode_access_token(token: str) -> dict:
    """Декодирование JWT токена"""
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
