"""Bach cantata lookup logic based on the Lutheran liturgical calendar."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum


class LiturgicalHoliday(str, Enum):
    Advent1 = "Advent1"
    StNicholas = "StNicholas"
    Advent2 = "Advent2"
    Advent3 = "Advent3"
    Advent4 = "Advent4"
    ChristmasEve = "ChristmasEve"
    ChristmasDay1 = "ChristmasDay1"
    ChristmasDay2 = "ChristmasDay2"
    SundayAfterChristmas = "SundayAfterChristmas"
    NewYearsEve = "NewYearsEve"
    NewYearsDay = "NewYearsDay"
    Epiphany = "Epiphany"
    Sunday1AfterEpiphany = "Sunday1AfterEpiphany"
    Sunday2AfterEpiphany = "Sunday2AfterEpiphany"
    Sunday3AfterEpiphany = "Sunday3AfterEpiphany"
    Sunday4AfterEpiphany = "Sunday4AfterEpiphany"
    Sunday5BeforeLent = "Sunday5BeforeLent"
    Sunday4BeforeLent = "Sunday4BeforeLent"
    Septuagesimae = "Septuagesimae"
    Sexagesimae = "Sexagesimae"
    Estomihi = "Estomihi"
    AshWednesday = "AshWednesday"
    Invocavit = "Invocavit"
    Reminiscere = "Reminiscere"
    Oculi = "Oculi"
    Laetare = "Laetare"
    Judica = "Judica"
    Palmarum = "Palmarum"
    MaundyThursday = "MaundyThursday"
    GoodFriday = "GoodFriday"
    HolySaturday = "HolySaturday"
    EasterSunday = "EasterSunday"
    EasterMonday = "EasterMonday"
    EasterTuesday = "EasterTuesday"
    Quasimodogeniti = "Quasimodogeniti"
    MisericordiasDomini = "MisericordiasDomini"
    Jubilate = "Jubilate"
    Kantate = "Kantate"
    Rogate = "Rogate"
    Ascension = "Ascension"
    Exaudi = "Exaudi"
    PentecostSunday = "PentecostSunday"
    PentecostMonday = "PentecostMonday"
    PentecostTuesday = "PentecostTuesday"
    Trinity = "Trinity"
    Sunday1AfterTrinity = "Sunday1AfterTrinity"
    Sunday2AfterTrinity = "Sunday2AfterTrinity"
    StJohn = "StJohn"
    Sunday3AfterTrinity = "Sunday3AfterTrinity"
    Sunday4AfterTrinity = "Sunday4AfterTrinity"
    Sunday5AfterTrinity = "Sunday5AfterTrinity"
    Sunday6AfterTrinity = "Sunday6AfterTrinity"
    Sunday7AfterTrinity = "Sunday7AfterTrinity"
    Sunday8AfterTrinity = "Sunday8AfterTrinity"
    Sunday9AfterTrinity = "Sunday9AfterTrinity"
    Sunday10AfterTrinity = "Sunday10AfterTrinity"
    Sunday11AfterTrinity = "Sunday11AfterTrinity"
    Sunday12AfterTrinity = "Sunday12AfterTrinity"
    Sunday13AfterTrinity = "Sunday13AfterTrinity"
    Sunday14AfterTrinity = "Sunday14AfterTrinity"
    Sunday15AfterTrinity = "Sunday15AfterTrinity"
    Sunday16AfterTrinity = "Sunday16AfterTrinity"
    StMichael = "StMichael"
    Thanksgiving = "Thanksgiving"
    Sunday17AfterTrinity = "Sunday17AfterTrinity"
    Sunday18AfterTrinity = "Sunday18AfterTrinity"
    Sunday19AfterTrinity = "Sunday19AfterTrinity"
    Sunday20AfterTrinity = "Sunday20AfterTrinity"
    Reformation = "Reformation"
    Sunday21AfterTrinity = "Sunday21AfterTrinity"
    Sunday22AfterTrinity = "Sunday22AfterTrinity"
    StMartin = "StMartin"
    Sunday23AfterTrinity = "Sunday23AfterTrinity"
    Sunday24AfterTrinity = "Sunday24AfterTrinity"
    RepentanceAndPrayer = "RepentanceAndPrayer"
    EternitySunday = "EternitySunday"
    Annunciation = "Annunciation"
    Presentation = "Presentation"
    MaryVisitation = "MaryVisitation"


@dataclass
class Cantata:
    """Represents a Bach cantata."""

    bwv: str
    title: str
    spotify_url: str | None
    status: str | None


def load_cantata_data() -> dict[str, list[dict]]:
    """Load cantata data from JSON file."""
    path = os.path.join(os.path.dirname(__file__), "BachCantatas.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            # Strip keys because of " StMichael" typo in the source JSON
            return {k.strip(): v for k, v in data.items()}
    except FileNotFoundError:
        return {}


CANTATA_DATA = load_cantata_data()


def _easter_date(year: int) -> date:
    """Compute Easter Sunday using the Anonymous Gregorian algorithm."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def _get_next_weekday(start: date, weekday: int) -> date:
    """Return the next occurrence of a weekday (0=Mon, 6=Sun) on or after start."""
    days_to_add = (weekday - start.weekday() + 7) % 7
    return start + timedelta(days=days_to_add)


def _get_start_of_liturgical_year(year: int) -> date:
    """Return the start of the liturgical year (1st Sunday in Advent) for the given year."""
    nov30 = date(year, 11, 30)
    sunday_before = _get_next_weekday(nov30 - timedelta(days=7), 6)
    sunday_after = _get_next_weekday(nov30, 6)

    if nov30.weekday() == 6:
        return nov30

    diff_before = nov30 - sunday_before
    diff_after = sunday_after - nov30

    return sunday_before if diff_before < diff_after else sunday_after


def get_liturgical_holiday(day: date) -> LiturgicalHoliday | None:
    """Return the liturgical holiday for the given date."""
    year = day.year
    start_of_year = _get_start_of_liturgical_year(year)

    if start_of_year > day:
        start_of_year = _get_start_of_liturgical_year(year - 1)

    # Determine liturgical year section
    end_of_christmas = date(start_of_year.year + 1, 2, 2)
    easter = _easter_date(day.year)

    if start_of_year <= day <= end_of_christmas:
        return _get_christmas_holiday(start_of_year, day)
    elif day <= easter + timedelta(days=50):
        return _get_easter_holiday(day)
    else:
        return _get_trinity_holiday(day)


def _get_christmas_holiday(start_of_year: date, day: date) -> LiturgicalHoliday | None:
    current_year = day.year
    epiphany = date(current_year, 1, 6)
    if day.month == 1 and day.day < 6:
        # If we are in January before Epiphany, use current year's Epiphany for Sunday calculation
        pass
    elif day.month == 12:
        # If we are in December, we need the Epiphany of NEXT year
        epiphany = date(current_year + 1, 1, 6)
    
    sunday_after_epiphany = _get_next_weekday(epiphany, 6)

    if day == start_of_year:
        return LiturgicalHoliday.Advent1
    if day.month == 12 and day.day == 6:
        return LiturgicalHoliday.StNicholas
    if day == start_of_year + timedelta(days=7):
        return LiturgicalHoliday.Advent2
    if day == start_of_year + timedelta(days=14):
        return LiturgicalHoliday.Advent3
    if day.month == 12 and day.day == 24:
        return LiturgicalHoliday.ChristmasEve
    if day == start_of_year + timedelta(days=21):
        return LiturgicalHoliday.Advent4
    if day.month == 12 and day.day == 25:
        return LiturgicalHoliday.ChristmasDay1
    if day.month == 12 and day.day == 26:
        return LiturgicalHoliday.ChristmasDay2
    if day.month == 12 and day.day == 31:
        return LiturgicalHoliday.NewYearsEve
    if day.month == 1 and day.day == 1:
        return LiturgicalHoliday.NewYearsDay
    if day == start_of_year + timedelta(days=28):
        return LiturgicalHoliday.SundayAfterChristmas
    if day.month == 1 and day.day == 6:
        return LiturgicalHoliday.Epiphany
    if day == sunday_after_epiphany:
        return LiturgicalHoliday.Sunday1AfterEpiphany
    if day == sunday_after_epiphany + timedelta(days=7):
        return LiturgicalHoliday.Sunday2AfterEpiphany
    if day == sunday_after_epiphany + timedelta(days=14):
        return LiturgicalHoliday.Sunday3AfterEpiphany
    if day == sunday_after_epiphany + timedelta(days=21):
        return LiturgicalHoliday.Sunday4AfterEpiphany
    if day.month == 3 and day.day == 25:
        return LiturgicalHoliday.Annunciation
    if day.month == 2 and day.day == 2:
        return LiturgicalHoliday.Presentation
    return None


def _get_easter_holiday(day: date) -> LiturgicalHoliday | None:
    easter = _easter_date(day.year)

    if day.month == 3 and day.day == 25:
        return LiturgicalHoliday.Annunciation
    if day == easter - timedelta(days=77):
        return LiturgicalHoliday.Sunday5BeforeLent
    if day == easter - timedelta(days=70):
        return LiturgicalHoliday.Sunday4BeforeLent
    if day == easter - timedelta(days=63):
        return LiturgicalHoliday.Septuagesimae
    if day == easter - timedelta(days=56):
        return LiturgicalHoliday.Sexagesimae
    if day == easter - timedelta(days=49):
        return LiturgicalHoliday.Estomihi
    if day == easter - timedelta(days=46):
        return LiturgicalHoliday.AshWednesday
    if day == easter - timedelta(days=42):
        return LiturgicalHoliday.Invocavit
    if day == easter - timedelta(days=35):
        return LiturgicalHoliday.Reminiscere
    if day == easter - timedelta(days=28):
        return LiturgicalHoliday.Oculi
    if day == easter - timedelta(days=21):
        return LiturgicalHoliday.Laetare
    if day == easter - timedelta(days=14):
        return LiturgicalHoliday.Judica
    if day == easter - timedelta(days=7):
        return LiturgicalHoliday.Palmarum
    if day == easter - timedelta(days=3):
        return LiturgicalHoliday.MaundyThursday
    if day == easter - timedelta(days=2):
        return LiturgicalHoliday.GoodFriday
    if day == easter - timedelta(days=1):
        return LiturgicalHoliday.HolySaturday
    if day == easter:
        return LiturgicalHoliday.EasterSunday
    if day == easter + timedelta(days=1):
        return LiturgicalHoliday.EasterMonday
    if day == easter + timedelta(days=2):
        return LiturgicalHoliday.EasterTuesday
    if day == easter + timedelta(days=7):
        return LiturgicalHoliday.Quasimodogeniti
    if day == easter + timedelta(days=14):
        return LiturgicalHoliday.MisericordiasDomini
    if day == easter + timedelta(days=21):
        return LiturgicalHoliday.Jubilate
    if day == easter + timedelta(days=28):
        return LiturgicalHoliday.Kantate
    if day == easter + timedelta(days=35):
        return LiturgicalHoliday.Rogate
    if day == easter + timedelta(days=39):
        return LiturgicalHoliday.Ascension
    if day == easter + timedelta(days=42):
        return LiturgicalHoliday.Exaudi
    if day == easter + timedelta(days=49):
        return LiturgicalHoliday.PentecostSunday
    if day == easter + timedelta(days=50):
        return LiturgicalHoliday.PentecostMonday
    return None


def _get_trinity_holiday(day: date) -> LiturgicalHoliday | None:
    easter = _easter_date(day.year)
    trinity = easter + timedelta(days=56)
    next_start = _get_start_of_liturgical_year(day.year)
    if next_start <= day:
        # We are already in the next liturgical year
        pass
    else:
        # Check if we should use the next year's start for Eternity Sunday calculation
        next_start = _get_start_of_liturgical_year(day.year)
        if next_start < day: # This shouldn't happen based on the logic above
             next_start = _get_start_of_liturgical_year(day.year + 1)
        # Wait, if day is in Dec but before start of NEXT liturgical year...
        # The logic in .NET is:
        # var startOfNextLiturgicalYear = GetStartOfLiturgicalYear(day);
        # which returns the start of the liturgical year FOR THAT YEAR.
        # If day is say 2023-11-20, startOfNextLiturgicalYear is likely 2023-12-03.
        pass

    if day == trinity:
        return LiturgicalHoliday.Trinity
    if day.month == 10 and day.day <= 7 and day.weekday() == 6:
        return LiturgicalHoliday.Thanksgiving
    
    offsets = {
        7: LiturgicalHoliday.Sunday1AfterTrinity,
        14: LiturgicalHoliday.Sunday2AfterTrinity,
        21: LiturgicalHoliday.Sunday3AfterTrinity,
        28: LiturgicalHoliday.Sunday4AfterTrinity,
        35: LiturgicalHoliday.Sunday5AfterTrinity,
        42: LiturgicalHoliday.Sunday6AfterTrinity,
        49: LiturgicalHoliday.Sunday7AfterTrinity,
        56: LiturgicalHoliday.Sunday8AfterTrinity,
        63: LiturgicalHoliday.Sunday9AfterTrinity,
        70: LiturgicalHoliday.Sunday10AfterTrinity,
        77: LiturgicalHoliday.Sunday11AfterTrinity,
        84: LiturgicalHoliday.Sunday12AfterTrinity,
        91: LiturgicalHoliday.Sunday13AfterTrinity,
        98: LiturgicalHoliday.Sunday14AfterTrinity,
        105: LiturgicalHoliday.Sunday15AfterTrinity,
        112: LiturgicalHoliday.Sunday16AfterTrinity,
        119: LiturgicalHoliday.Sunday17AfterTrinity,
        126: LiturgicalHoliday.Sunday18AfterTrinity,
        133: LiturgicalHoliday.Sunday19AfterTrinity,
        140: LiturgicalHoliday.Sunday20AfterTrinity,
        147: LiturgicalHoliday.Sunday21AfterTrinity,
        154: LiturgicalHoliday.Sunday22AfterTrinity,
        161: LiturgicalHoliday.Sunday23AfterTrinity,
        168: LiturgicalHoliday.Sunday24AfterTrinity,
    }
    
    delta = (day - trinity).days
    if delta in offsets:
        return offsets[delta]

    if day == next_start - timedelta(days=7):
        return LiturgicalHoliday.EternitySunday
    if day == next_start - timedelta(days=11):
        return LiturgicalHoliday.RepentanceAndPrayer
    
    if day.month == 10 and day.day == 31:
        return LiturgicalHoliday.Reformation
    if day.month == 9 and day.day == 29:
        return LiturgicalHoliday.StMichael
    if day.month == 11 and day.day == 11:
        return LiturgicalHoliday.StMartin
    if day.month == 6 and day.day == 24:
        return LiturgicalHoliday.StJohn
    if day.month == 7 and day.day == 2:
        return LiturgicalHoliday.MaryVisitation
    
    return None


def get_cantatas_for_date(for_date: date | None = None) -> tuple[str | None, list[Cantata]]:
    """Return (holiday_name, list_of_cantatas) for the current/next Sunday."""
    if for_date is None:
        for_date = date.today()

    # Advance to the next Sunday (or stay if already Sunday)
    days_until_sunday = (6 - for_date.weekday()) % 7
    sunday = for_date + timedelta(days=days_until_sunday)

    holiday = get_liturgical_holiday(sunday)
    if holiday is None:
        return None, []

    cantatas_raw = CANTATA_DATA.get(holiday.value, [])
    cantatas = []
    for c in cantatas_raw:
        spotify_url = c.get("SpotifyUrl")
        if spotify_url == "NN" or spotify_url == "":
            spotify_url = None
        
        cantatas.append(
            Cantata(
                bwv=f"BWV {c.get('Bwv')}",
                title=c.get("Name", "Unknown Title"),
                spotify_url=spotify_url,
                status=c.get("Status") or c.get("CantataStatus"),
            )
        )

    return holiday.value, cantatas
