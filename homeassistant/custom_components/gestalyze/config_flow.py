"""Config flow for Gestalyze integration."""
from __future__ import annotations

from typing import Any
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from . import DOMAIN

class GestalyzeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Gestalyze."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Gestalyze", data={})

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return GestalyzeOptionsFlow(config_entry)

class GestalyzeOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Gestalyze."""

    def __init__(self, config_entry):
        """Initialize Gestalyze options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init")
