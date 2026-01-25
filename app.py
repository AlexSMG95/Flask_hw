from aiohttp import web
from config import Config
from database import init_database, get_db
from routes import setup_routes

async def on_startup(app: web.Application):
    """Инициализация при запуске"""
    config = app['config']

    db = init_database(config)
    await db.init_db()

    print(f"Application started on {config.HOST}:{config.PORT}")

async def on_cleanup(app: web.Application):
    """Очистка ресурсов при остановке"""
    db = get_db()
    if db:
        await db.close()

    print("Application stopped")

def create_app(config: Config = None) -> web.Application:
    """Фабрика приложения"""
    if config is None:
        config = Config.from_env()

    app = web.Application()
    app['config'] = config

    setup_routes(app)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    return app

if __name__ == '__main__':
    config = Config.from_env()
    app = create_app(config)

    web.run_app(
        app,
        host=config.HOST,
        port=config.PORT
    )
