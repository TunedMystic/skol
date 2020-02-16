from starlette import status
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse, JSONResponse

from markette import db


def homepage(request):
    return PlainTextResponse('Hello')


def version(request):
    return JSONResponse({'version': '0.0.1'})


async def message(request):
    row = await db.database.fetch_one('select 1 as message;')
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


async def startup():
    await db.connect()
    print('starting up...')


async def shutdown():
    await db.disconnect()
    print('shutting down...')


app = Starlette()

app.add_event_handler('startup', startup)
app.add_event_handler('shutdown', shutdown)

app.add_route('/', homepage)
app.add_route('/version', version)
app.add_route('/message', message)
app.add_route('/products', ProductList)
