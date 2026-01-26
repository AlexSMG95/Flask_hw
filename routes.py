from aiohttp import web
from handlers.auth import register, login
from handlers.ads import create_ad, get_ad, update_ad, delete_ad

def setup_routes(app: web.Application):
    """Регистрация всех маршрутов"""

    app.router.add_post('/register', register)
    app.router.add_post('/login', login)

    app.router.add_post('/ads', create_ad)
    app.router.add_get('/ads/{id}', get_ad)
    app.router.add_put('/ads/{id}', update_ad)
    app.router.add_delete('/ads/{id}', delete_ad)
