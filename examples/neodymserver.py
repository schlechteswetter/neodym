import asyncio
import websockets
import json

# NEODYM Server Beta V1
# akzeptiert Websocket Verbindungen und leitet Befehle weiter


devices = [0,0,0]

async def handle(websocket, path):
   
   global devices

   data = await websocket.recv()
   jsonresult = json.loads(data)

   if((jsonresult["id"] == 1) & (jsonresult["password"] == "1234")):
      reply = '{"success" true, "id": 1}'
      devices[1] = websocket

   elif((jsonresult["id"] == 2) & (jsonresult["password"] == "5678")):
      reply = '{"success" true, "id": 2}'
      devices[2] = websocket
      print("Lampe verbunden")

   else:
      reply = '{"success" false, "id": 0}'

   # alle angemeldeten Geräte ausgeben
   print("\n angemeldete Geräte:")
   for device in devices:
      print(device)   
      
   await websocket.send(reply)

   async for message in websocket:
      decoded = json.loads(message)
      if(decoded["id"] == 2):
          await devices[2].send(message)



start_server = websockets.serve(handle, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
