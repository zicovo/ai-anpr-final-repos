# Test to send a message from a client
# this code is used in main.py to send a message with the result
import websockets
import asyncio

async def hello():
  uri = "ws://localhost:5000"
  async with websockets.connect(uri) as websocket:
    await websocket.send("no-phone")
    greeting = await websocket.recv()
    print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())