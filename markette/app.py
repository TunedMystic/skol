from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route

from markette import db


def homepage(request):
    return PlainTextResponse('Hello')


def version(request):
    return JSONResponse({'version': '0.0.1'})


async def message(request):
    row = await db.database.fetch_one('select 1 as message;')
    return JSONResponse(dict(row))


async def startup():
    await db.connect()
    print('starting up...')


async def shutdown():
    await db.disconnect()
    print('shutting down...')


routes = [
    Route('/', homepage),
    Route('/version', version),
    Route('/message', message),
]


app = Starlette(debug=True, routes=routes, on_startup=[startup], on_shutdown=[shutdown])
