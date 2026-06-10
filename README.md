# Bach Cantata of the Week

![Johann Sebastian Bach cantata logo](custom_components/bach_cantata/brand/logo.png)

A Home Assistant integration that displays the Johann Sebastian Bach cantata(s) assigned to the current or upcoming Sunday according to the Lutheran liturgical calendar. This integration shows BWV numbers, titles, liturgical occasions and provides Spotify links when available — ideal for classical music fans and Home Assistant users who want an automated "Cantata of the Week" display.

Keywords: Johann Sebastian Bach, Bach cantata, Bach cantata Home Assistant, Cantata of the Week, BWV cantata, Bach cantatas Spotify, Lutheran liturgical calendar Bach, HACS Bach cantata

## Features

- **Current/Next Cantata**: Shows the BWV number and title of the Johann Sebastian Bach cantata(s) assigned to the upcoming Sunday.
- **Liturgical Calendar**: Implements the full Lutheran liturgical year logic (ported from the [.NET LiturgicalHolidays calculator](https://gitlab.com/bach.jetzt/next-bach-cantata)) to reliably select the correct cantata each Sunday.
- **Spotify Integration**: Provides a direct Spotify URL for each cantata (if available) so you can play Johann Sebastian Bach cantatas straight from your dashboard.
- **Sensor Attributes**: Publishes extra attributes including the liturgical occasion and the date of the next Sunday.
- **HACS & Manual Install**: Install via HACS for easy updates or copy the custom component manually.

## Installation

### Via HACS (Recommended)

1. Open **HACS** in Home Assistant.
2. Click on the three dots in the top right corner and select **Custom repositories**.
3. Add the URL of this repository and select **Integration** as the category.
4. Search for "Bach Cantata of the Week" and click **Download**.
5. Restart Home Assistant.

> Tip: Make the short HACS description include "Johann Sebastian Bach" so the integration is easier to find in searches.

### Manual

1. Download the `bach_cantata` folder from `custom_components/`.
2. Copy it into your Home Assistant `custom_components/` directory.
3. Restart Home Assistant.

## Configuration

1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for "Bach Cantata of the Week" and follow the instructions.

After adding the integration a sensor will be created (example entity id): `sensor.bach_cantata_of_the_week`.

## Sensor: attributes and example

The sensor state contains the BWV number(s) (e.g. `BWV 61, BWV 62`). The sensor exposes the following attributes:

- `occasion`: Name of the liturgical occasion (e.g. "Trinity Sunday").
- `cantatas`: List of cantata objects with keys: `bwv`, `title`, `spotify_url`, `status`.
- `next_sunday`: ISO date of the next Sunday.

Example extra_attributes (JSON-like):

```
{ "occasion": "Trinity Sunday", "cantatas": [{ "bwv": "BWV 61", "title": "Nun komm, der Heiden Heiland", "spotify_url": "https://open.spotify..." }], "next_sunday": "2026-06-14" }
```

## Usage Examples

Lovelace card example (simple markdown card):

```yaml
type: markdown
content: |
  ## Cantata of the Week
  **{{ states('sensor.bach_cantata_of_the_week') }}**
  {% for c in state_attr('sensor.bach_cantata_of_the_week','cantatas') %}
  - {{ c.title }} ({{ c.bwv }}) — [Play on Spotify]({{ c.spotify_url }})
  {% endfor %}
```

Simple automation example (announce cantata on Sunday morning):

```yaml
alias: Announce Bach Cantata
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
      message: "This week's Johann Sebastian Bach cantata is {{ states('sensor.bach_cantata_of_the_week') }}."
```

## Troubleshooting

- No data / sensor is empty: Check Home Assistant logs and ensure the integration is installed and enabled. The integration uses the local liturgical calculation logic and does not require a remote API for cantata selection.
- Timezone issues: Ensure your Home Assistant timezone is set correctly in **Settings** > **System** > **Timezone**.
- HACS install not visible: Ensure HACS has refreshed repositories and the custom repository URL includes this project.

## Contributing

Contributions are welcome. Please open issues for bugs or feature requests and submit pull requests for fixes. When contributing, include small focused changes and update translations if you modify user-facing text.

Development notes:
- The calculation logic is ported from the `bach.jetzt` project and unit-tested upstream. See `custom_components/bach_cantata/cantata.py` for date logic.

## Translations

This repository contains translations (see `custom_components/bach_cantata/translations`). The default English strings are in `translations/en.json`. If you add translations, please add or update `README-<lang>.md`.

## Credits

- Based on the [Bach Cantata data and logic](https://gitlab.com/bach.jetzt/next-bach-cantata) by the bach.jetzt project.
- Ported to Home Assistant by Junie and Tilmann Bach.

## License

MIT