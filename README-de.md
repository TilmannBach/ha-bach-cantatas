# Bach-Kantate der Woche

![Johann Sebastian Bach Kantaten-Logo](custom_components/bach_cantata/brand/logo.png)

Eine Home Assistant-Integration, die die für den aktuellen oder kommenden Sonntag vorgesehene Johann Sebastian Bach‑Kantate(n) gemäß dem lutherischen liturgischen Kalender anzeigt. Die Integration liefert BWV‑Nummern, Titel, liturgische Anlässe und — falls verfügbar — Spotify‑Links und ist ideal für Klassik‑Fans, die eine automatisierte "Kantate der Woche" Anzeige wünschen.

Schlüsselwörter: Johann Sebastian Bach, Bach‑Kantate, Bach‑Kantate Home Assistant, Kantate der Woche, BWV‑Kantate, Bach‑Kantaten Spotify, lutherischer liturgischer Kalender Bach, HACS Bach‑Kantate

## Funktionen

- **Aktuelle/Nächste Kantate**: Zeigt die BWV‑Nummer und den Titel der Johann Sebastian Bach‑Kantate(n) an, die dem kommenden Sonntag zugewiesen sind.
- **Liturgischer Kalender**: Implementiert die vollständige Logik des lutherischen Kirchenjahres (portiert vom [.NET LiturgicalHolidays calculator](https://gitlab.com/bach.jetzt/next-bach-cantata)), damit die richtige Kantate gewählt wird.
- **Spotify‑Integration**: Stellt für jede Kantate eine direkte Spotify‑URL zur Verfügung, um Johann Sebastian Bach‑Kantaten direkt abzuspielen.
- **Sensorattribute**: Veröffentlicht zusätzliche Attribute wie den liturgischen Anlass und das Datum des nächsten Sonntags.
- **HACS & manuelle Installation**: Einfache Installation über HACS oder manuelle Kopie des Custom Components.

## Installation

### Über HACS (empfohlen)

1. Öffne **HACS** in Home Assistant.
2. Klicke oben rechts auf die drei Punkte und wähle **Benutzerdefinierte Repositories**.
3. Füge die URL dieses Repositories hinzu und wähle als Kategorie **Integration**.
4. Suche nach "Bach Cantata of the Week" und klicke auf **Download**.
5. Starte Home Assistant neu.

> Tipp: Verwende in der HACS‑Kurzbeschreibung "Johann Sebastian Bach", damit die Integration leichter gefunden wird.

### Manuell

1. Lade den Ordner `bach_cantata` aus `custom_components/` herunter.
2. Kopiere ihn in dein Home Assistant `custom_components/` Verzeichnis.
3. Starte Home Assistant neu.

## Konfiguration

1. Gehe in Home Assistant zu **Einstellungen** > **Geräte & Dienste**.
2. Klicke auf **Integration hinzufügen**.
3. Suche nach "Bach Cantata of the Week" und folge den Anweisungen.

Nach der Integration wird ein Sensor erstellt, beispielhafter Entity‑ID: `sensor.bach_cantata_of_the_week`.

## Sensor: Attribute und Beispiel

Der Sensor‑State enthält die BWV‑Nummer(n) (z. B. `BWV 61, BWV 62`). Die folgenden Attribute werden bereitgestellt:

- `occasion`: Name des liturgischen Anlasses (z. B. "Trinitatis").
- `cantatas`: Liste der Kantatenobjekte mit Schlüsseln: `bwv`, `title`, `spotify_url`, `status`.
- `next_sunday`: ISO‑Datum des nächsten Sonntags.

Beispiel für extra_attributes (JSON‑ähnlich):

```
{ "occasion": "Trinitatis", "cantatas": [{ "bwv": "BWV 61", "title": "Nun komm, der Heiden Heiland", "spotify_url": "https://open.spotify..." }], "next_sunday": "2026-06-14" }
```

## Anwendungsbeispiele

Lovelace‑Beispiel (Markdown‑Card):

```yaml
type: markdown
content: |
  ## Kantate der Woche
  **{{ states('sensor.bach_cantata_of_the_week') }}**
  {% for c in state_attr('sensor.bach_cantata_of_the_week','cantatas') %}
  - {{ c.title }} ({{ c.bwv }}) — [Auf Spotify abspielen]({{ c.spotify_url }})
  {% endfor %}
```

Einfache Automation (Sonntagmorgen‑Ansage):

```yaml
alias: Kantate Ansage
trigger:
  - platform: time
    at: '09:00:00'
condition:
  - condition: template
    value_template: "{{ is_state('sensor.bach_cantata_of_the_week','not_none') }}"
action:
  - service: tts.google_translate_say
    data:
      entity_id: media_player.living_room_speaker
      message: "Die Kantate von Johann Sebastian Bach für diese Woche ist {{ states('sensor.bach_cantata_of_the_week') }}."
```

## Fehlerbehebung

- Keine Daten / Sensor leer: Prüfe die Home Assistant Logs und ob die Integration installiert und aktiviert ist. Die Auswahl der Kantate erfolgt lokal durch die Logik des Plugins und benötigt keine externe API.
- Zeitzonenprobleme: Stelle sicher, dass die Zeitzone in Home Assistant unter **Einstellungen** > **System** > **Zeitzone** korrekt eingestellt ist.
- HACS‑Installation nicht sichtbar: Stelle sicher, dass HACS die Repositories neu geladen hat und die URL korrekt ist.

## Mitwirken

Beiträge sind willkommen. Bitte öffne Issues für Fehler oder Feature‑Wünsche und reiche Pull‑Requests für Änderungen ein. Aktualisiere Übersetzungen, wenn du benutzerseitige Texte änderst.

Entwicklungs‑Hinweis:
- Die Datumslogik ist vom `bach.jetzt` Projekt portiert. Siehe `custom_components/bach_cantata/cantata.py` für die Berechnungen.

## Übersetzungen

Das Repository enthält Übersetzungen (siehe `custom_components/bach_cantata/translations`). Die englischen Standardtexte befinden sich in `translations/en.json`. Wenn du Übersetzungen hinzufügst, erweitere bitte `README-<lang>.md`.

## Danksagungen

- Basierend auf den [Bach Cantata Daten und der Logik](https://gitlab.com/bach.jetzt/next-bach-cantata) des bach.jetzt‑Projekts.
- Portiert nach Home Assistant von Junie und Tilmann Bach.

## Lizenz

MIT