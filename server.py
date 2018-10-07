import argparse
import atexit
import asyncio
import unicornhathd
import websockets
from jsonrpcserver.aio import methods

@methods.add
async def ping():
    return 'pong'

@methods.add
async def brightness(b):
    return unicornhd.brightness(b)

@methods.add
async def clear():
    return unicornhathd.clear()

@methods.add
async def get_rotation():
    return unicornhathd.get_rotation()

@methods.add
async def get_pixel(x, y):
    return unicornhathd.get_pixel(x, y)

@methods.add
async def get_shape():
    return unicornhathd.get_shape()

@methods.add
async def off():
    return unicornhathd.off()

@methods.add
async def set_rotation(r):
    return unicornhathd.rotation(r)

@methods.add
async def set_all(r, g, b):
    return unicornhathd.set_all(r, g, b)

@methods.add
async def set_pixel(x, y, r, g, b):
    return unicornhathd.set_pixel(x, y, r, g, b)

@methods.add
async def set_pixel_hsv(x, y, h, s=1.0, v=1.0):
    return unicornhathd.set_pixel_hsv(x, y, h, s, v)

@methods.add
async def show():
    return unicornhathd.show()

@methods.add
async def noise():
    unicornhathd._buf = unicornhathd.numpy.random.randint(low=0,high=255,size=(16,16,3))
    unicornhathd.show()

async def accept_connection(websocket, _):
    async for request in websocket:
        response = await methods.dispatch(request)
        if not response.is_notification:
            await websocket.send(str(response))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a WebSocket JSON-RPC server for Unicorn Hat HD.')
    parser.add_argument('-r', '--rotation', type=int, default=9, help='The default rotation for the display.')
    parser.add_argument('-p', '--port', type=int, default=5000, help='The port to bind the WebSocket server to.')
    parser.add_argument('-k', '--keep-screen-on', action='store_true', help='Whether to keep the screen on when the server is terminated.')
    args = parser.parse_args()

    start_server = websockets.serve(accept_connection, port=args.port)
    asyncio.get_event_loop().run_until_complete(start_server)

    try:
        asyncio.get_event_loop().run_forever()
    finally:
        if (not args.keep_screen_on):
            asyncio.get_event_loop().run_until_complete(off())
