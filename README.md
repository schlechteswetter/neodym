# neodym

## Kurzbeschreibung:
Neodym soll ein Protokoll werden, damit verschiedene Geräte über einen zentralen Server miteinander kommunizieren können.

## specification
im Ordner `specification` befindet sich eine Beschreibung des Neodym Protokolls in Beta V1. 



## Beispielumsetzung:
Um das Protokoll zu nutzen habe ich 3 Beispielprogramme erstellt. Diese setzen sehr grob und unschön das Neodym Protokoll in V1 um:

### neodymserver.py
-akzeptiert WS Verbindung an localhost:8000
-nimmt exakt 2 Geräte an: 1 und 2 mit Passwort 1234 und 5678.
-kann nach Anmeldung Befehle von Gerät 1 an Gerät 2 weiterleiten

### lampe.py
-verbindet sich mit localhost:8000 und meldet sich mit ID 2 an. 
-wartet danach auf Nachrichten, wenn command "light" ist, gibt sie den value in der konsole aus

### EinmalLichtschalter.py
-verbindet sich mit localhost:8000 und meldet sich mit ID 1 an.
-sendet eine Nachricht mit command "light" und value 1 an ID 2 (Lampe)
-schließt die Verbindung wieder
