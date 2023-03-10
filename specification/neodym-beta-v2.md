# Neodym Beta V2

## Ziel
Neodym soll ein Protokoll werden, damit verschiedene Geräte über einen zentralen Server miteinander kommunizieren können.

---

## neue Funktionen zu Beta-V1:
- Geräteverwaltung/Passwort ändern
- Geräteverwaltung/neues Gerät hinzufügen

---

## Funktionen

### Verbindungen
Ein Server nimmt websocket Verbindungen der verschiedenen Geräte an und überprüft die Anmeldedaten. 

### Commands
Die verbundenen Geräte können Befehle an den Server senden und er leitet diese dann an die entsprechenden Empfänger weiter.

### Geräteverwaltung

- Passwort ändern:
Geräte können ihr Passwort ändern

- neue Geräte hinzufügen:
mit einem verbundenen Gerät können Anmeldedaten für ein neues Gerät angefordert werden.

---

## Protokolle


### Verbindungsaufbau

1. Das Gerät baut eine Websocketverbindung mit dem Neodym-server an Port 8000 auf. 
2. Es sendet seine Anmeldedaten als JSON formatiert nach folgendem Muster: 
   `{"id": <ID>, "password": "<PASSWORD>"}`
3. Der Server sendet eine Antwort, dass die anmeldung erfolgreich war:
  `{"success" true, "id": <ID>}`
4. wenn keine antwort zurückkommt oder success false ist, dann kann der Client den Anmeldevorgang wiederholen
5. wenn die Anmeldung erfolgreich war, dann kann der Client Befehle/Nachrichten an andere Geräte senden und selbst welche empfangen. Ein Befehl muss nach folgendem Muster aufgebaut sein:
`{"id": <EMPFÄNGER>, "command": "<BEFEHLNAME>", "value": "<PARAMETER>"}`

### neues Gerät registrieren
1. Gerät baut Verbindung auf
2. Gerät sendet Befehl an ID 0 (Neodym Server selbst), dass ein neues Gerät hinzugefügt werden soll:
`{"id":0, "command": "registerNewDevice", "value":{"id": <NEUE GERÄTE ID>, "password": <PASSWORT>}}`
wenn man keine id oder password mit angibt, soll der Server die zufällig generieren
3. Der Server sendet eine Bestätigung mit ID und Passwort zurück:
`{"success": true, "id": "<NEUE ID>", "password":"<PASSWORT>"}`

### Passwort ändern
1. Gerät baut Verbindung auf
2. Gerät sendet Befehl an ID 0 (Neodym Server selbst), dass Passwort geändert werden soll:
`{"id": 0, "command": "changePassword", "value":"<NEW PASSWORD>"`
3. Server sendet Bestätigung:
`{"success": true}`
4. Gerät loggt sich mit den neuen Daten neu ein