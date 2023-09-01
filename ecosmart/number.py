import logging
import requests
from pprint import pformat
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_NAME, CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.number import NumberEntity, PLATFORM_SCHEMA
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
    """Set up the number platform."""
    # Add devices
    _LOGGER.info(pformat(config))

    number_entity = {
        "name": config[CONF_NAME],
        "host": config[CONF_HOST],
    }

    add_entities([EcoNumberEntity(number_entity)])


class EcoNumberEntity(NumberEntity):
    """Representation of a Number Entity that controls a servo via a web server."""

    def __init__(self, number_entity) -> None:
        """Initialize the EcoNumberEntity."""
        self._number_entity = number_entity
        self._name = number_entity["name"]
        self._state = None

    @property
    def name(self) -> str:
        """Return the display name of this number entity."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the number entity."""
        return f"eco_number_entity_{self._number_entity['host']}"

    @property
    def state(self) -> float | None:
        """Return the state of the number entity."""
        return self._state

    async def async_set_value(self, value: float) -> None:
        """Set the value of the number entity."""
        self._state = value
        url = f"http://{self._number_entity['host']}?data={value}"
        async with aiohttp_client.async_get_clientsession(self.hass) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    _LOGGER.error("Error setting value: %d", response.status)
                else:
                    _LOGGER.info("Value set to: %f", value)
