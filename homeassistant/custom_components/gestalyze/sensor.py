"""Sensor platform for Gestalyze integration."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Gestalyze sensor platform."""
    entities = [
        GestalyzeSensor(
            hass,
            entry,
            "hand",
            "Hand",  # Display name
            "gestalyze_hand",  # Entity ID without entry_id
            f"gestalyze_hand_{entry.entry_id}",  # Unique ID (needs to remain unique)
            "",  # Initial state
        ),
        GestalyzeSensor(
            hass,
            entry,
            "orientation",
            "Orientation",
            "gestalyze_orientation",
            f"gestalyze_orientation_{entry.entry_id}",
            "",
        ),
        GestalyzeSensor(
            hass,
            entry,
            "fingers",
            "Fingers",
            "gestalyze_fingers",
            f"gestalyze_fingers_{entry.entry_id}",
            "",
        ),
        GestalyzeSensor(
            hass,
            entry,
            "finger_count",
            "Finger Count",
            "gestalyze_finger_count",
            f"gestalyze_finger_count_{entry.entry_id}",
            "",
        ),
        GestalyzeSensor(
            hass,
            entry,
            "asl_letter",
            "ASL Letter",
            "gestalyze_asl_letter",
            f"gestalyze_asl_letter_{entry.entry_id}",
            "",
        ),
    ]

    async_add_entities(entities)

    # Store entities in hass.data for later state updates
    hass.data[DOMAIN][entry.entry_id] = {
        entity.unique_id: entity for entity in entities
    }

class GestalyzeSensor(SensorEntity):
    """Representation of a Gestalyze Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        sensor_type: str,
        display_name: str,
        entity_id: str,
        unique_id: str,
        state: str,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._sensor_type = sensor_type
        self._attr_name = display_name
        self._attr_native_value = state
        self._attr_unique_id = unique_id
        self.entity_id = f"sensor.{entity_id}"
        
        # All sensors belong to the same device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Gestalyze",
            manufacturer="Gestalyze",
            model="Gesture Analyzer",
            sw_version="0.1.0",
        )

    async def async_update_from_data(self, data: dict[str, Any]) -> None:
        """Update sensor state from provided data."""
        if self._sensor_type in data:
            self._attr_native_value = data[self._sensor_type]
            self.async_write_ha_state()
