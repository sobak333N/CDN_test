from aiohttp import web
from aiohttp_apispec import (
    docs, request_schema, response_schema, querystring_schema
)

from app.schemas import ( 
    CityNameSchema, CitySchema, CityQuerySchema, CityListResponseSchema,
)
from app.services import CityService
from app.errors import MissingParametrExc
# class NearestCitiesResponseSchema(web.Schema):
#     city1 = fields.Nested(CitySchema)
#     city2 = fields.Nested(CitySchema)
CITY_API_PREFIX = "/city"
city_service = CityService()


@docs(
    tags=["Cities"],
    summary="Create city in storage",
    description="Добавляет город по названию",
)
@request_schema(CityNameSchema)
@response_schema(CitySchema, 201)
async def post_city(request: web.Request):
    data = await request.json()
    schema = CityNameSchema().load(data)
    city = await city_service.create(schema)
    return web.json_response(
        CitySchema().dump(city),
        status=201
    )


@docs(
    tags=["Cities"],
    summary="Get List of cities",
    description="Получает список",
)
@querystring_schema(CityQuerySchema)
@response_schema(CityListResponseSchema, 200)
async def get_list_cities(request: web.Request):
    page = request.query.get("page")
    if not page:
        raise MissingParametrExc(field_name="page")
    total_count, cities = await city_service.get_page(int(page))
    return web.json_response(
        {
            "cities": CitySchema(many=True).dump(cities),
            'total_count': total_count
        },
        status=200
    )    


def setup_cities_routes(app: web.Application):
    # app.router.add_post('/city/nearest_cities', get_nearest_cities)
    app.router.add_post(f'{CITY_API_PREFIX}/post', post_city)
    app.router.add_get(f'{CITY_API_PREFIX}/get/', get_list_cities)

