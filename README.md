# MEP_RVK
Automatische Planausgabe in ArchiCAD27

Automatisierte Planausgabe mit ArchiCAD

Dieses Projekt bietet eine automatisierte Lösung zur Veröffentlichung von Plänen in ArchiCAD zu vordefinierten Zeitpunkten. Es verwendet Python-Skripte, um eine Verbindung zu einer laufenden ArchiCAD-Instanz herzustellen und bestimmte Befehle mithilfe der "Additional JSON Commands" Add-on-Schnittstelle auszuführen.

Voraussetzungen

Archicad: Eine laufende Version von ArchiCAD muss installiert und gestartet sein.

Additional JSON Commands Add-on: Dieses Add-on muss installiert und in ArchiCAD aktiviert sein. Es erweitert die JSON-Schnittstelle von ArchiCAD um zusätzliche Befehle.

Python: Python 3.x sollte installiert sein, einschließlich der erforderlichen Pakete:

tkinter

tkcalendar

Dateien

1. JSON_Commands.py

Dieses Skript stellt die grundlegenden Funktionen bereit, um mit ArchiCAD über die JSON-Schnittstelle zu kommunizieren:

Funktionen:

ExecuteJSONCommands: Führt JSON-Befehle über das Add-on aus.

ConnectArchicad: Baut eine Verbindung zu einer laufenden ArchiCAD-Instanz auf.

ArchicadLocation: Ermittelt den Speicherort der ArchiCAD-Installation.

ShutdownArchicad: Beendet ArchiCAD über einen JSON-Befehl.

RunArchicad: Startet ArchiCAD und öffnet ein bestimmtes Projekt.

Fehlerbehandlung:

Überprüft, ob das Add-on installiert ist.

Behandelt fehlgeschlagene Befehle mit detaillierten Fehlermeldungen.

2. Publish_GUI.py

Dieses Skript bietet eine grafische Benutzeroberfläche (GUI) für die Planung und Durchführung der Planveröffentlichung:

Hauptfunktionen:

Auswahl und Anzeige der verfügbaren Publisher-Sets aus ArchiCAD.

Planung der Veröffentlichung zu einem bestimmten Datum und einer bestimmten Uhrzeit.

Angabe eines Speicherorts für die veröffentlichten Pläne.

GUI-Komponenten:

Projektinformationen (z. B. Speicherort, Benutzername bei Teamwork-Projekten).

Kalender und Zeitwahl für die Planung.

Fortschrittsanzeige für den Veröffentlichungsstatus.

Interaktionen:

Nutzt die Funktionen aus JSON_Commands.py, um die benötigten Befehle auszuführen.

Installation und Verwendung

Installieren des Add-ons

Laden Sie das "Additional JSON Commands" Add-on herunter und installieren Sie es in ArchiCAD.

Vorbereitung des Projekts

Starten Sie ArchiCAD und öffnen Sie das gewünschte Projekt.

Skripte ausführen

Stellen Sie sicher, dass alle Abhängigkeiten installiert sind.

Starten Sie Publish_GUI.py, um die grafische Oberfläche zu öffnen.

Planung der Veröffentlichung

Wählen Sie ein Publisher-Set und definieren Sie den gewünschten Speicherort.

Planen Sie Datum und Uhrzeit für die Veröffentlichung.

Hinweise

Teamwork-Projekte: Wenn das Projekt ein Teamwork-Projekt ist, stellt das Skript sicher, dass alle Änderungen synchronisiert werden, bevor die Veröffentlichung durchgeführt wird.

Fehlerbehandlung: Das System prüft, ob alle erforderlichen Ressourcen und Add-ons verfügbar sind. Bei Fehlern werden Benutzer mit detaillierten Meldungen informiert.
