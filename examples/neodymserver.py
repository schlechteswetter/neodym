import asyncio
import websockets
import json

# NEODYM Server Beta V2
# akzeptiert Websocket Verbindungen und leitet Befehle weiter
# und speichert geräte


devices = [
   {
    "id": 0,
    "password": "",
    "websocket": ""
   },
   {
    "id": 1,
    "password": "1234",
    "websocket": ""
   },
   {
    "id": 2,
    "password": "5678",
    "websocket": ""
   },
]

def getDeviceById(id):
   for element in devices:
      if((element["id"] == id) ):
         return element
      
def executeCommand(device, message):
   print("führe Befehl aus: " + str(message))

   # wenn Password ändern:
   if(message["command"] == "changePassword"):
      getDeviceById(device)["password"] = message["value"]
      return '{"success": true}'


async def handle(websocket, path):
   
   global devices
   connectedDevice = 0
   data = await websocket.recv()
   jsonresult = json.loads(data)

   try:
      element = getDeviceById(jsonresult["id"])
      if(element["password"] == jsonresult["password"]):
         connectedDevice = jsonresult["id"]
         reply = '{"success" true, "id": '+ str(connectedDevice) + '}'
         element["websocket"] = websocket
         
      else:
         reply = '{"success" false}'
   except:
      reply = '{"success" false}'

   
   # for element in devices:
   #    if((element["id"] == jsonresult["id"]) & (element["password"] == jsonresult["password"])):
   #       reply = '{"success" true, "id": '+ str(jsonresult["id"]) + '}'
   #       element["websocket"] = websocket
   

   # if((jsonresult["id"] == 1) & (jsonresult["password"] == "1234")):
   #    reply = '{"success" true, "id": 1}'
   #    devices[1] = websocket

   # elif((jsonresult["id"] == 2) & (jsonresult["password"] == "5678")):
   #    reply = '{"success" true, "id": 2}'
   #    devices[2] = websocket
   #    print("Lampe verbunden")

   # else:
   #    reply = '{"success" false, "id": 0}'

   # alle angemeldeten Geräte ausgeben
   print("\n angemeldete Geräte:")
   for device in devices:
      print(device)   
      
   await websocket.send(reply)

   async for message in websocket:
      decoded = json.loads(message)
      try:
         if(decoded["id"] == 0):
            await getDeviceById(connectedDevice)["websocket"].send(executeCommand(connectedDevice, decoded))
         else:
            await getDeviceById(decoded["id"])["websocket"].send(message)
        
      except:
         print("fehler")



start_server = websockets.serve(handle, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
