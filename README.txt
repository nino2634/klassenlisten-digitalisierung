README 
Klassenlisten-Digitalisierungsanwendung

Übersicht
-------------------------------------------------
Diese Anwendung dient der Digitalisierung und Verwaltung von Klassenlisten.
Sie wird als Webanwendung betrieben und über einen Python-Webserver gestartet.


Voraussetzungen
-------------------------------------------------
Python, siehe requirments.txt
Zugriff auf einen eine Serverumgebung
Netzwerkzugriff auf den konfigurierten Port (Standard: 8443)


Installation
-------------------------------------------------
Repository klonen oder Projektdateien bereitstellen
Abhängigkeiten installieren
Sicherstellen, dass Python korrekt installiert ist


Start der Webanwendung
-------------------------------------------------
Die Anwendung wird im Terminal gestartet:
python -m app
Nach dem Start ist die Weboberfläche erreichbar über:
http://<server-ip>:8443


Konfiguration
-------------------------------------------------
Für Konfigurationsänderungen und administrative Aufgaben steht ein separates Konfigurationstool zur Verfügung:
python -m src.configurator

Mit diesem Tool können folgende Einstellungen vorgenommen werden:
Festlegen oder Ändern des Pfads zur Datenquelle
Anpassung der Formatierung der Datenquelle
Ändern von Passwörtern
Benutzerkonten und Ersteinrichtung


Benutzer
-------------------------------------------------
Die Anwendung verfügt standardmäßig über die folgenden Benutzerkonten:
LUSD
Lehrer

Wichtiger Hinweis:
Die zugehörigen Passwörter müssen bei der Ersteinrichtung der Anwendung zwingend geändert werden.
Der Betrieb der Anwendung mit den Standardpasswörtern stellt ein erhebliches Sicherheitsrisiko dar.

Die Passwortänderung erfolgt über das Konfigurationstool:
python -m src.configurator


Netzwerk und Protokoll
-------------------------------------------------
Standardmäßig läuft die Anwendung über HTTP
Verwendeter Port: 8443
Umstellung auf HTTPS

Um die Anwendung über HTTPS mit selbstsignierten Zertifikaten zu betreiben:
Datei app.py öffnen
Zeile 215 entkommentieren
Zeile 217 kommentieren
Anwendung neu starten

Nach der Umstellung werden automatisch selbstsignierte Zertifikate verwendet.
