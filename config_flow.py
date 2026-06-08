"""Config flow for Bach Cantata integration."""
from __future__ import annotations

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN


class BachCantataConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bach Cantata."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Bach Cantata of the Week", data={})

        return self.async_show_form(step_id="user")
