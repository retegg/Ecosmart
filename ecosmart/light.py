import logging
import hashlib

from pprint import pformat

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.light import (
    SUPPORT_BRIGHTNESS,
    ATTR_BRIGHTNESS,
    PLATFORM_SCHEMA,
    LightEntity,
)
from homeassistant.const import CONF_NAME, CONF_HOST
import voluptuous as vol

from .ecoled import EcoLed

_LOGGER = logging.getLogger("ecomsart")

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
    }
)

def generate_unique_id(light):
    # Generate a unique ID based on the device configuration
    config_str = f"{light['name']}_{light['host']}"
    return hashlib.md5(config_str.encode()).hexdigest()

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    # Add devices
    _LOGGER.info(pformat(config))

    light = {
        "name": config[CONF_NAME],
        "host": config[CONF_HOST],
    }

    unique_id = generate_unique_id(light)
    add_entities([EcoLedLight(light, hass, unique_id)])


class EcoLedLight(LightEntity):
    """Representation of a Godox Light."""

    def __init__(self, light, hass, unique_id) -> None:
        """Initialize a GodoxLight."""
        _LOGGER.info(pformat(light))
        self._light = EcoLed(light["host"], hass)
        self._name = light["name"]
        self._state = None
        self._brightness = None
        self._unique_id = unique_id

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the light entity."""
        return self._unique_id

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self._brightness

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        if ATTR_BRIGHTNESS in kwargs:
            await self._light.set_brightness(kwargs[ATTR_BRIGHTNESS])
        await self._light.turn_on()

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        await self._light.turn_off()

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._light.is_on
        self._brightness = self._light.brightness
