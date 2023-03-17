import asyncio
import websockets

# Dieses Programm stellt beispielweise einen Lichtschalter dar. 
#
# Beim Ausführen verbindet er sich mit dem Neodym Server und loggt sich mit
# den Daten ID:1 und Password:1234 ein
#
# Danach gibt er die Serverantwort in der Konsole aus und sendet einen Licht AN Befehl
# mit der Adresse 2 (im Beispiel die Lampe)
#
# Zum Schluss beendet er die Verbindung wieder
 
async def login():
    async with websockets.connect('ws://localhost:8000') as websocket:
        await websocket.send('{"id": 0, "command":"login", "value": {"id": 1, "password": "1234"}}')
        response = await websocket.recv()
        print(response)
        await websocket.send('{ "id":2, "command":"light", "value": 1}')
        await websocket.close()
 
asyncio.get_event_loop().run_until_complete(login())