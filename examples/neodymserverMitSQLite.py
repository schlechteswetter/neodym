import asyncio
import websockets
import json
import sqlite3

# NEODYM Server Beta V2 mit SQLite für Devices Speicher
# akzeptiert Websocket Verbindungen und leitet Befehle weiter
# und speichert geräte

connectedDevices = []


def setupDatabase():
   connection = sqlite3.connect("devices.db")
   cursor = connection.cursor()
   try:
      print("erfolgreich mit Datenbank verbunden")
      try:
         cursor.execute("CREATE TABLE devices (id INTEGER PRIMARY KEY, password TEXT NOT NULL)")
         cursor.execute("INSERT INTO devices (id, password) VALUES (0, '')")
         cursor.execute("INSERT INTO devices (id, password) VALUES (1, '1234')")
         cursor.execute("INSERT INTO devices (id, password) VALUES (2, '5678')")
         connection.commit()
      except:
         print("Datenbank Anfangsstand existiert bereits")

   except:
      print("keine Datenbankverbindung möglich")

   print(cursor.execute("SELECT * FROM devices").fetchall())

   connection.close()
   



   #devices = []

   # for device in DBresult:
   #    devices.append({
   #    "id": device[0],
   #    "password": device[1],
   #    "websocket": ""
   #    })

   # print(devices)





def login(id, password):
   global connectedDevices

   connection = sqlite3.connect("devices.db")
   cursorr = connection.cursor()
   result = cursorr.execute("SELECT * FROM devices where id=" + str(id)).fetchall()
   connection.close()
   if(result[0][1] == password) & getDeviceById(id) == False:
      connectedDevices.append({
       "id": result[0][0],
       "websocket": ""
       })
      return True
   return False


def removeFromConnectedDevices(id):
   global connectedDevices
   for element in connectedDevices:
      if element["id"] == id:
         connectedDevices.remove(element)


def getDeviceById(id):
   global connectedDevices
   for element in connectedDevices:
      if((element["id"] == id) ):
         return element
   return False
      
def executeCommand(device, message):
   print("führe Befehl aus: " + str(message))

   # wenn Password ändern:
   # if(message["command"] == "changePassword"):
   #    getDeviceById(device)["password"] = message["value"]
   #    return '{"success": true}'


# alle angemeldeten Geräte ausgeben
def printConnectedDevices():
   global connectedDevices
   print("\n angemeldete Geräte:")
   for device in connectedDevices:
      print(device)   





async def handle(websocket, path):
   global connectedDevices
   connectedDevice = 0
   data = await websocket.recv()
   jsonresult = json.loads(data)
   id = jsonresult["id"]

   try:
      print("Loginversuch mit " + str(id))
      if(login(jsonresult["id"], jsonresult["password"])):
         print("erfolgreich")
         reply = '{"success" true, "id": '+ str(connectedDevice) + '}' 
         element = getDeviceById(jsonresult["id"])
         connectedDevice = jsonresult["id"]
         element["websocket"] = websocket
         
      else:
         reply = '{"success" false}'
   except:
      reply = '{"success" false}'

   
   printConnectedDevices()
      
   await websocket.send(reply)

   async for message in websocket:
      decoded = json.loads(message)
      try:
         if(decoded["id"] == 0):
            await getDeviceById(connectedDevice)["websocket"].send(executeCommand(connectedDevice, decoded))
         else:
            await getDeviceById(decoded["id"])["websocket"].send(message)
        
      except:
         removeFromConnectedDevices(id)
   removeFromConnectedDevices(id)


setupDatabase()
start_server = websockets.serve(handle, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
