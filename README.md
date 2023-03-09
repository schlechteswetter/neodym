# neodym

Neodym soll ein Konzept sein, wie verschiedene Geräte miteinander über einen zentralen Server kommunizieren können.

Beta V1:
Der Server akzeptiert Websocket Verbindungen. 
Aktuell können sich 2 verschiedene Geräte mit ID 1 oder 2 einloggen. Dazu müssen sie einen JSON Login übertragen damit der Server sie zuordnen kann.
Danach kann Gerät 1 an Gerät 2 Befehle senden. 

Es gibt außerdem 2 Beispiel Clients, 1 ist eine Lampe das andere ein Lichtschalter um die ganz grobe Funktion zu demonstrieren.
