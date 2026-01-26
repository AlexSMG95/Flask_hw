from aiohttp import web
import jwt
from functools import wraps
from config import Config

config = Config.from_env()

def jwt_required(handler):
    """Декоратор для защищенных эндпоинтов"""
    @wraps(handler)
    async def middleware(request: web.Request):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return web.json_response(
                {"message": "Missing Authorization Header"},
                status=401
            )

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM]
            )

            request['user_id'] = payload['identity']

        except jwt.ExpiredSignatureError:
            return web.json_response(
                {"message": "Token has expired"},
                status=401
            )
        except jwt.InvalidTokenError:
            return web.json_response(
                {"message": "Invalid token"},
                status=401
            )

        return await handler(request)

    return middleware
