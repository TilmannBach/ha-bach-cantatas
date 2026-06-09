"""Sensor platform for Bach Cantata of the Week."""
from __future__ import annotations

from datetime import date, timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.util.dt as dt_util

from . import DOMAIN
from .cantata import Cantata, get_cantatas_for_date

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bach Cantata sensor from a config entry."""
    async_add_entities([BachCantataSensor(entry)], update_before_add=True)


class BachCantataSensor(SensorEntity):
    """Sensor showing the Bach cantata(s) for the current/next Sunday."""

    _attr_has_entity_name = True
    _attr_name = "Bach Cantata of the Week"
    _attr_icon = "mdi:music-clef-treble"

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_cantata"
        self._occasion: str | None = None
        self._cantatas: list[Cantata] = []

    @property
    def state(self) -> str | None:
        """Return the BWV number(s) as the state, e.g. 'BWV 61, BWV 62'."""
        if not self._cantatas:
            return None
        return ", ".join(c.bwv for c in self._cantatas)

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "occasion": self._occasion,
            "cantatas": [
                {
                    "bwv": c.bwv,
                    "title": c.title,
                    "spotify_url": c.spotify_url,
                    "status": c.status,
                }
                for c in self._cantatas
            ],
            "next_sunday": self._next_sunday().isoformat(),
        }

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        today = dt_util.now().date()
        self._occasion, self._cantatas = get_cantatas_for_date(today)
        if not self._cantatas:
            _LOGGER.debug("No cantatas found for occasion: %s", self._occasion)

    @staticmethod
    def _next_sunday() -> date:
        today = date.today()
        days_ahead = (6 - today.weekday()) % 7
        return today + timedelta(days=days_ahead)
