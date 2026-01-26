from aiohttp import web
from sqlalchemy import select
from models import User
from utils.password import hash_password, check_password
from utils.jwt_utils import create_access_token
from database import get_db
import json

async def register(request: web.Request) -> web.Response:
    """POST /register - регистрация пользователя"""
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"message": "Invalid JSON"}, status=400)

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return web.json_response(
            {"message": "Email and password are required"},
            status=400
        )

    db = get_db()
    async with db.session_factory() as session:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            return web.json_response(
                {"message": "Email already exists!"},
                status=400
            )

        hashed_password = await hash_password(password)

        new_user = User(email=email, password=hashed_password)
        session.add(new_user)
        await session.commit()

    return web.json_response(
        {"message": "User registered successfully!"},
        status=201
    )

async def login(request: web.Request) -> web.Response:
    """POST /login - аутентификация пользователя"""
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"message": "Invalid JSON"}, status=400)

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return web.json_response(
            {"message": "Email and password are required"},
            status=400
        )

    db = get_db()
    async with db.session_factory() as session:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return web.json_response(
                {"message": "Invalid credentials"},
                status=401
            )

        password_valid = await check_password(password, user.password)
        if not password_valid:
            return web.json_response(
                {"message": "Invalid credentials"},
                status=401
            )

        access_token = create_access_token(identity=str(user.id))

    return web.json_response({"access_token": access_token}, status=200)
