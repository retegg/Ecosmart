import logging
import requests
from pprint import pformat
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_NAME, CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.binary_sensor import BinarySensorEntity, PLATFORM_SCHEMA
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
    """Set up the binary sensor platform."""
    # Add devices
    _LOGGER.info(pformat(config))

    binary_sensor = {
        "name": config[CONF_NAME],
        "host": config[CONF_HOST],
    }

    add_entities([EcoBinarySensor(binary_sensor)])


class EcoBinarySensor(BinarySensorEntity):
    """Representation of a Binary Sensor that queries a web server."""

    def __init__(self, binary_sensor) -> None:
        """Initialize the EcoBinarySensor."""
        self._binary_sensor = binary_sensor
        self._name = binary_sensor["name"]
        self._state = None

    @property
    def name(self) -> str:
        """Return the display name of this binary sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the binary sensor."""
        return f"eco_binary_sensor_{self._binary_sensor['host']}"

    @property
    def is_on(self) -> bool | None:
        """Return True if the binary sensor is on."""
        return self._state

    async def async_update(self):
        """Update the binary sensor state."""
        url = f"http://{self._binary_sensor['host']}"
        async with aiohttp_client.async_get_clientsession(self.hass) as session:
            async with session.get(url) as response:
                try:
                    if (await response.text()).strip() == "on":
                        self._state = True  # Set binary sensor state based on response
                        _LOGGER.info(f"binary modificado a {self._state}")
                    else:
                        self._state = False
                        _LOGGER.info(f"sensor binary modificado a {self._state}")
                except requests.exceptions.RequestException as ex:
                    _LOGGER.error("Error during web server request: %s", ex)
                    self._state = False  # Set binary sensor state to False on error
