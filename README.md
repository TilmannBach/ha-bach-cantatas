# Bach Cantata of the Week

![Bach Cantata of the Week Logo](branding/logo.png)

A Home Assistant integration that displays the Bach Cantata(s) for the current or upcoming Sunday according to the Lutheran liturgical calendar.

## Features

- **Current/Next Cantata**: Shows the BWV number and title of the cantata(s) assigned to the upcoming Sunday.
- **Liturgical Calendar**: Implements the full Lutheran liturgical year logic (ported from the [.NET LiturgicalHolidays calculator](https://gitlab.com/bach.jetzt/next-bach-cantata)).
- **Spotify Integration**: Provides a direct Spotify URL for each cantata (if available).
- **Extra Attributes**: Includes the name of the liturgical occasion and the next Sunday's date.

## Installation

### Via HACS (Recommended)

1. Open **HACS** in Home Assistant.
2. Click on the three dots in the top right corner and select **Custom repositories**.
3. Add the URL of this repository and select **Integration** as the category.
4. Search for "Bach Cantata of the Week" and click **Download**.
5. Restart Home Assistant.

### Manual

1. Download the `bach_cantata` folder from `custom_components/`.
2. Copy it into your Home Assistant `custom_components/` directory.
3. Restart Home Assistant.

## Configuration

1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for "Bach Cantata of the Week" and follow the instructions.

## Credits

- Based on the [Bach Cantata data and logic](https://gitlab.com/bach.jetzt/next-bach-cantata) by the bach.jetzt project.
- Ported to Home Assistant by Junie and Tilmann Bach.

## License

MIT
