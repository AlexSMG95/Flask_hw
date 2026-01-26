import bcrypt
import asyncio

async def hash_password(password: str) -> str:
    """Async хеширование пароля с bcrypt"""
    loop = asyncio.get_event_loop()

    hashed = await loop.run_in_executor(
        None,
        lambda: bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
    )

    return hashed.decode('utf-8')

async def check_password(password: str, hashed: str) -> bool:
    """Async проверка пароля"""
    loop = asyncio.get_event_loop()

    try:
        result = await loop.run_in_executor(
            None,
            lambda: bcrypt.checkpw(
                password.encode('utf-8'),
                hashed.encode('utf-8')
            )
        )
        return result
    except Exception:
        return False
