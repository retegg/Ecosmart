import logging
import requests
from pprint import pformat
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_NAME, CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.switch import (
    SwitchEntity,
    PLATFORM_SCHEMA,
    DEVICE_CLASS_SWITCH,
)
import voluptuous as vol
from homeassistant.helpers import aiohttp_client

_LOGGER = logging.getLogger("ecomsart")

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the switch platform."""
    # Add devices
    _LOGGER.info(pformat(config))

    switch_entity = {
        "name": config[CONF_NAME],
        "host": config[CONF_HOST],
    }

    add_entities([EcoSwitchEntity(switch_entity)])


class EcoSwitchEntity(SwitchEntity):
    """Representation of a Switch Entity that controls a device via a web server."""

    def __init__(self, switch_entity) -> None:
        """Initialize the EcoSwitchEntity."""
        self._switch_entity = switch_entity
        self._name = switch_entity["name"]
        self._state = None

    @property
    def name(self) -> str:
        """Return the display name of this switch entity."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the switch entity."""
        return f"eco_switch_entity_{self._switch_entity['host']}"

    @property
    def is_on(self) -> bool:
        """Return the state of the switch entity."""
        return self._state

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the switch entity."""
        self._state = True
        url = f"http://{self._switch_entity['host']}/on"
        async with aiohttp_client.async_get_clientsession(self.hass) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    _LOGGER.error("Error turning on: %d", response.status)
                else:
                    _LOGGER.info("Switch turned on")

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the switch entity."""
        self._state = False
        url = f"http://{self._switch_entity['host']}/off"
        async with aiohttp_client.async_get_clientsession(self.hass) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    _LOGGER.error("Error turning off: %d", response.status)
                else:
                    _LOGGER.info("Switch turned off")
