# Neodym Beta V1

## Funktionen

### Verbindungen
Ein Server nimmt websocket Verbindungen der verschiedenen Geräte an und überprüft die Anmeldedaten.

### Commands
Die verbundenen Geräte können Befehle an den Server senden und er leitet diese dann an die entsprechenden Empfänger weiter.

---

## Protokoll

### Verbindungsaufbau
1. Das Gerät baut eine Websocketverbindung mit dem Neodym-server an Port 8000 auf. 
2. Es sendet seine Anmeldedaten als JSON formatiert nach folgendem Muster: 
   `{"id": <ID>, "password": "<PASSWORD>"}`
3. Der Server sendet eine Antwort, dass die anmeldung erfolgreich war:
  `{"success" true, "id": <ID>}`
4. wenn keine antwort zurückkommt oder success false ist, dann kann der Client den Anmeldevorgang wiederholen
5. wenn die Anmeldung erfolgreich war, dann kann der Client Befehle/Nachrichten an andere Geräte senden und selbst welche empfangen. Ein Befehl muss nach folgendem Muster aufgebaut sein:
`{"id": <EMPFÄNGER>, "command": "<BEFEHLNAME>", "value": "<PARAMETER>"}`