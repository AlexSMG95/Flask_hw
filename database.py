from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from models import Base
from config import Config

class Database:
    def __init__(self, config: Config):
        self.engine: AsyncEngine = create_async_engine(
            config.DATABASE_URL,
            echo=True,
            future=True
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        """Создание всех таблиц"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        """Закрытие engine"""
        await self.engine.dispose()

db: Database = None

def init_database(config: Config) -> Database:
    global db
    db = Database(config)
    return db

def get_db() -> Database:
    return db
