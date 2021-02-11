import websockets
import asyncio

connected = set()

async def server(ws, path):
  connected.add(ws)
  try:
    async for message in ws:
      print(message)
      for c in connected:
        await c.send(message)
  finally:
    connected.remove(ws)

  

start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()