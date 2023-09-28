import logging
import requests
from pprint import pformat
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_NAME, CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.sensor import SensorEntity, PLATFORM_SCHEMA
import voluptuous as vol
from homeassistant.helpers import aiohttp_client

_LOGGER = logging.getLogger("ecosmart")

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
    """Set up the sensor platform."""
    # Add devices
    _LOGGER.info(pformat(config))

    sensor = {
        "name": config.get(CONF_NAME),  # Use .get() to safely retrieve optional config values
        "host": config[CONF_HOST],
    }

    add_entities([EcoSensor(sensor)])

class EcoSensor(SensorEntity):
    """Representation of a Temperature and Humidity Sensor that queries a web server."""

    def __init__(self, sensor) -> None:
        """Initialize the EcoSensor."""
        super().__init__()  # Call the superclass constructor
        self._sensor = sensor
        self._name = sensor["name"]
        self._state_air = None
        self._state_temp = None
        self._state_hum = None
        self._state_water = None

    @property
    def name(self) -> str:
        """Return the display name of this sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the sensor."""
        return f"eco_sensor_{self._sensor['host']}"

    async def async_update(self):
        """Update the sensor's data."""
        async with aiohttp_client.async_get_clientsession(self.hass) as session:
            try:
                url = f"http://{self._sensor['host']}/type"  # Adjust the URL format as needed
                async with session.get(url) as response_temp:
                    if response_temp.status == 200:
                        _type = await response_temp.text()
                        if _type == "1":
                            """Update the sensor state."""
                            url_temp = f"http://{self._sensor['host']}/temp"
                            url_hum = f"http://{self._sensor['host']}/hum"
                            
                            try:  # Avoid using aiohttp within aiohttp, use regular try/except
                                async with session.get(url_temp) as response_temp:
                                    if response_temp.status == 200:
                                        self._state_temp = await response_temp.text()
                                        _LOGGER.info(f"Temperature updated: {self._state_temp}°C")
                                    else:
                                        _LOGGER.error("Error retrieving temperature: %d", response_temp.status)
                            
                                async with session.get(url_hum) as response_hum:
                                    if response_hum.status == 200:
                                        self._state_hum = await response_hum.text()
                                        _LOGGER.info(f"Humidity updated: {self._state_hum}%")
                                    else:
                                        _LOGGER.error("Error retrieving humidity: %d", response_hum.status)
                            except requests.exceptions.RequestException as ex:
                                _LOGGER.error("Error during web server request: %s", ex)
                                self._state_temp = None
                                self._state_hum = None
                        elif _type == "3":
                            print("humedad de la tierra")
                            url_sensor = f"http://{self._sensor['host']}/"
                            async with session.get(url_sensor) as response_air:
                                if response_air.status == 200:
                                    self._state_air = await response_.text()
                                    _LOGGER.info(f"air updated: {self._state_air}")
                                else:
                                    _LOGGER.error("Error retrieving air sensor: %d", response_air.status)
                        elif _type == "2":
                            url_sensor = f"http://{self._sensor['host']}/"
                            async with session.get(url_sensor) as response_water:
                                if response_water.status == 200:
                                    self._state_water = await response_water.text()
                                    _LOGGER.info(f"waetr updated: {self._state_water}")
                                else:
                                    _LOGGER.error("Error retrieving water sensor: %d", response_water.status)
                        else:
                            _LOGGER.error("Error retrieving the type: %d", response_temp.status)
            except requests.exceptions.RequestException as ex:
                _LOGGER.error("Error during getting the type: %s", ex)
                self._state_temp = None
                self._state_hum = None

    @property
    def state(self) -> str | None:
        """Return the state of the sensor."""
        if self._state_temp is not None and self._state_hum is not None:
            return f"Temp: {self._state_temp}°C, Hum: {self._state_hum}%"
        elif self._state_air is not None:
            return f"Calidad del aire: {self._state_air}"
        elif self._state_water is not None:
            return f"humedad en analogico; {self._state_water}"
        else:
            return "Unknown"

