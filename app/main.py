from starlette import status
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, PlainTextResponse

from app import database, settings


def homepage(request):
    return PlainTextResponse('Hello')


def version(request):
    return JSONResponse({'version': '0.0.1'})


async def message(request):
    conn = await database.get_connection()
    row = await conn.fetchrow('select 1 as message;')
    await conn.close()
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

app.add_event_handler('startup', database.initialize)
app.add_event_handler('shutdown', database.close)

app.add_route('/', homepage)
app.add_route('/version', version)
app.add_route('/message', message)
app.add_route('/products', ProductList)
