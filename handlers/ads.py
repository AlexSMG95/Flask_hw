from aiohttp import web
from models import Ad
from database import get_db
from middlewares.jwt_auth import jwt_required

@jwt_required
async def create_ad(request: web.Request) -> web.Response:
    """POST /ads - создание объявления"""
    user_id = request.get('user_id')

    try:
        data = await request.json()
    except:
        return web.json_response({"message": "Invalid JSON"}, status=400)

    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return web.json_response(
            {"message": "Title and description are required"},
            status=400
        )

    db = get_db()
    async with db.session_factory() as session:
        new_ad = Ad(
            title=title,
            description=description,
            owner_id=int(user_id)
        )
        session.add(new_ad)
        await session.commit()

    return web.json_response(
        {"message": "Ad created successfully!"},
        status=201
    )

async def get_ad(request: web.Request) -> web.Response:
    """GET /ads/{id} - получение объявления"""
    ad_id = request.match_info.get('id')

    try:
        ad_id = int(ad_id)
    except (ValueError, TypeError):
        return web.json_response({"message": "Invalid ad ID"}, status=400)

    db = get_db()
    async with db.session_factory() as session:
        ad = await session.get(Ad, ad_id)

        if not ad:
            return web.json_response({"message": "Ad not found"}, status=404)

        ad_data = ad.to_dict()

    return web.json_response(ad_data, status=200)

@jwt_required
async def update_ad(request: web.Request) -> web.Response:
    """PUT /ads/{id} - обновление объявления"""
    user_id = int(request.get('user_id'))
    ad_id = int(request.match_info.get('id'))

    try:
        data = await request.json()
    except:
        return web.json_response({"message": "Invalid JSON"}, status=400)

    db = get_db()
    async with db.session_factory() as session:
        ad = await session.get(Ad, ad_id)

        if not ad:
            return web.json_response({"message": "Ad not found"}, status=404)

        if ad.owner_id != user_id:
            return web.json_response(
                {"message": "You are not authorized to update this ad"},
                status=403
            )

        ad.title = data.get('title', ad.title)
        ad.description = data.get('description', ad.description)

        await session.commit()

    return web.json_response(
        {"message": "Ad updated successfully!"},
        status=200
    )

@jwt_required
async def delete_ad(request: web.Request) -> web.Response:
    """DELETE /ads/{id} - удаление объявления"""
    user_id = int(request.get('user_id'))
    ad_id = int(request.match_info.get('id'))

    db = get_db()
    async with db.session_factory() as session:
        ad = await session.get(Ad, ad_id)

        if not ad:
            return web.json_response({"message": "Ad not found"}, status=404)

        if ad.owner_id != user_id:
            return web.json_response(
                {"message": "You are not authorized to delete this ad"},
                status=403
            )

        await session.delete(ad)
        await session.commit()

    return web.json_response(
        {"message": "Ad deleted successfully!"},
        status=200
    )
