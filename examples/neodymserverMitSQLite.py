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



def login(id, password):
   global connectedDevices

   connection = sqlite3.connect("devices.db")
   cursorr = connection.cursor()
   result = cursorr.execute("SELECT * FROM devices where id=" + str(id)).fetchall()
   connection.close()
   if((result[0][1] == password) & (getDeviceById(id) == False)):
      connectedDevices.append({
       "id": result[0][0],
       "websocket": ""
       })
      return True
   return False

def registerNewDevice(password):
   connection = sqlite3.connect("devices.db")
   cursor = connection.cursor()
   result = cursor.execute("insert into devices (password) values (?)", [password])
   connection.commit()
   cursor = connection.cursor()
   result = cursor.execute("SELECT * FROM devices ORDER BY id DESC LIMIT 1")
   id= result.fetchall()
   connection.close()
   return id[0][0]
   


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
      


def executeCommand(device, message, websocket=False):
   print("führe Befehl aus: " + str(message))

   # wenn Password ändern:
   if(message["command"] == "changePassword"):
      if(changePassword(device, message["value"])):
         return '{"success": true}'
      else:
         return '{"success": false}'
      
   # wenn Login
   if(message["command"] == "login"):
      anmeldedaten = message["value"]

      print("Loginversuch mit " + str(anmeldedaten["id"]))
      if(login(anmeldedaten["id"], anmeldedaten["password"])):
         print("erfolgreich")
         element = getDeviceById(anmeldedaten["id"])
         element["websocket"] = websocket
         printConnectedDevices()
         return '{"success": true, "id": '+ str(anmeldedaten["id"]) + "}" 
      else:
         return '{"success" false, "id": '+ str(anmeldedaten["id"]) + "}" 
      
   #wenn Neuanlage
   if(message["command"] == "registerNew"):
      id = registerNewDevice(str(message["value"]))
      print(id)
      return '{"success": true, "id": '+ str(id) + "}" 

   


def changePassword(id, newPassword):
   try:
      connection = sqlite3.connect("devices.db")
      cursor = connection.cursor()
      cursor.execute("UPDATE devices set password = ? where id=?",[newPassword,str(id)])
      connection.commit()
      connection.close()
      return True
   except Exception as e:
      print(str(e))
      return False


# alle angemeldeten Geräte ausgeben
def printConnectedDevices():
   global connectedDevices
   print("\n angemeldete Geräte:")
   for device in connectedDevices:
      print(device)   





async def handle(websocket, path):
   global connectedDevices
   id=0
   async for message in websocket:
      decoded = json.loads(message)
      try:
         if(decoded["id"] == 0):
            result = executeCommand(id, decoded, websocket)
            if(decoded["command"] == "login"):
               id = json.loads(result)["id"]
            await websocket.send(result)
         else:
            await getDeviceById(decoded["id"])["websocket"].send(message)
      except:
         removeFromConnectedDevices(id)
   removeFromConnectedDevices(id)
   


setupDatabase()
start_server = websockets.serve(handle, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
