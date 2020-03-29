import logging

from starlette import status
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, PlainTextResponse

from app import database, settings

logger = logging.getLogger(__name__)


def homepage(request):
    return PlainTextResponse('Hello')


def version(request):
    return JSONResponse({'version': '0.0.1'})


async def message(request):
    # async with database.grab_connection() as conn:
    #     row = await conn.fetchrow('SELECT floor(random() * 5) AS message;')
    #     server_pid = conn.get_server_pid()
    #     msg = f'app_id: {id(request.app)} - conn_id: {server_pid} - pool_id: {id(database._pool)}'
    #     logger.info(msg)
    conn, done = await database.get_connection()
    row = await conn.fetchrow('SELECT floor(random() * 5) AS message;')
    server_pid = conn.get_server_pid()
    await done()
    msg = f'app_id: {id(request.app)} - conn_id: {server_pid} - pool_id: {id(database._pool)}'
    logger.info(msg)
    return JSONResponse(dict(row))


class ProductList(HTTPEndpoint):
    async def get(self, request):
        data = [
            {'id': '2c2dd3ff', 'name': 'Amazon Echo'},
            {'id': '2c2dd3ff', 'name': 'Apple iPhone'},
            {'id': '2c2dd3ff', 'name': 'SanDisk 1TB Harddrive'},
            {'id': '2c2dd3ff', 'name': 'Sony Extra Bass Headphones'},
            {'id': '2c2dd3ff', 'name': 'RFID Bifold Wallet'},
        ]
        return JSONResponse(data)

    async def post(self, request):
        return JSONResponse({'message': 'Product created'},
                            status_code=status.HTTP_201_CREATED)


app = Starlette(debug=settings.DEV)

app.add_event_handler('startup', database.connect)
app.add_event_handler('shutdown', database.close)

app.add_route('/', homepage)
app.add_route('/version', version)
app.add_route('/message', message)
app.add_route('/products', ProductList)
