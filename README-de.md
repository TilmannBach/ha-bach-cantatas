# Bach-Kantate der Woche

![Bach Cantata of the Week Logo](custom_components/bach_cantata/brand/logo.png)

Eine Home Assistant-Integration, die die Bach-Kantate(n) für den aktuellen oder kommenden Sonntag gemäß dem lutherischen liturgischen Kalender anzeigt.

## Funktionen

- **Aktuelle/Nächste Kantate**: Zeigt die BWV-Nummer und den Titel der Kantate(n) an, die dem kommenden Sonntag zugewiesen sind.
- **Liturgischer Kalender**: Implementiert die vollständige Logik des lutherischen liturgischen Jahres (portiert vom [.NET LiturgicalHolidays calculator](https://gitlab.com/bach.jetzt/next-bach-cantata)).
- **Spotify-Integration**: Stellt für jede Kantate eine direkte Spotify-URL zur Verfügung (falls vorhanden).
- **Zusätzliche Attribute**: Enthält den Namen des liturgischen Anlasses und das Datum des nächsten Sonntags.

## Installation

### Über HACS (empfohlen)

1. Öffne **HACS** in Home Assistant.
2. Klicke oben rechts auf die drei Punkte und wähle **Benutzerdefinierte Repositories** (Custom repositories).
3. Füge die URL dieses Repositories hinzu und wähle als Kategorie **Integration**.
4. Suche nach „Bach Cantata of the Week“ und klicke auf **Download**.
5. Starte Home Assistant neu.

### Manuell

1. Lade den Ordner `bach_cantata` aus `custom_components/` herunter.
2. Kopiere ihn in dein `custom_components/` Verzeichnis von Home Assistant.
3. Starte Home Assistant neu.

## Konfiguration

1. Gehe in Home Assistant zu **Einstellungen** > **Geräte & Dienste** (Settings > Devices & Services).
2. Klicke auf **Integration hinzufügen** (Add Integration).
3. Suche nach "Bach Cantata of the Week" und folge den Anweisungen.

## Danksagungen

- Basierend auf den [Bach Cantata Daten und der Logik](https://gitlab.com/bach.jetzt/next-bach-cantata) des bach.jetzt-Projekts.
- Portiert nach Home Assistant von Junie und Tilmann Bach.

## Lizenz

MIT
