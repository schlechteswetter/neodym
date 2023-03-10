import websocket
import json

# Dieses Programm stellt die Lampe dar. 
#
# Beim Ausführen verbindet er sich mit dem Neodym Server und loggt sich mit
# den Daten ID:2 und Password:5678 ein
#
# Danach wartet er bis zum Schließen der Verbindung auf Nachrichten.
# Wenn die empfangene Nachricht ein Licht Command ist, gibt er den 
# neu empfangenen Wert in der Konsole aus.
#
# Zum Schluss beendet er die Verbindung wieder
 
def on_message(ws, message):
    try:
        decoded = json.loads(message)
        if(decoded["command"] == "light"):
            print("Licht:" + str(json.loads(message)["value"]))
    except:
        print("Nachricht: " + message)

def on_error(ws, error):
    print(error)

def on_close(ws, ws1,  ws2):
    print("Verbindung getrennt")

def on_open(ws):
    ws.send('{ "id":2, "password":"5678"}')
    print("Verbindung erfolgreich\n")

print("verbinde mit Neodym Server...")
ws = websocket.WebSocketApp("ws://localhost:8000",
    on_message = on_message,
    on_error = on_error,
    on_close = on_close
)
ws.on_open = on_open
ws.run_forever()