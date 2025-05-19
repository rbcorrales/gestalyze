"""The Gestalyze integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "gestalyze"
PLATFORMS = [Platform.SENSOR]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Gestalyze component."""
    hass.data.setdefault(DOMAIN, {})

    # Register service
    async def handle_set_gesture_state(call: ServiceCall) -> None:
        """Handle the service call."""
        await async_set_gesture_state(hass, call.data)

    hass.services.async_register(
        DOMAIN,
        "set_gesture_state",
        handle_set_gesture_state
    )

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Gestalyze from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    # Load platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

async def async_set_gesture_state(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Update the state of all gesture sensors."""
    if DOMAIN not in hass.data:
        return

    # Update each sensor's state
    for entry_data in hass.data[DOMAIN].values():
        for sensor in entry_data.values():
            if hasattr(sensor, "async_update_from_data"):
                await sensor.async_update_from_data(data)
