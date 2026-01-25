import os
from dataclasses import dataclass

@dataclass
class Config:
    # Database (изменить на async SQLite)
    DATABASE_URL: str = 'sqlite+aiosqlite:///site.db'

    # JWT настройки
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'jwtsecretkey')
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRATION_DELTA_SECONDS: int = 3600

    # Server
    HOST: str = '0.0.0.0'
    PORT: int = 8080

    @classmethod
    def from_env(cls):
        return cls()
