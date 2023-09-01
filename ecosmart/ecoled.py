import asyncio
import logging
import requests

from homeassistant.helpers import aiohttp_client

LOGGER = logging.getLogger(__name__)

class EcoLed:
    def __init__(self, host: str, hass) -> None:
        self._host = host
        self._is_on = None
        self._connected = None
        self._brightness = None
        self.hass = hass

    
    async def _send(self, host, act, data=""):
        url = f"http://{host}/{act}?data={data}"
        async with aiohttp_client.async_get_clientsession(self.hass) as session:
            async with session.get(url) as response:
                await response.text()
    
    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness
    
    async def set_brightness(self, intensity: int):
        await self._send(self._host, "bright", str(intensity))
        self._brightness = intensity
    
    async def turn_on(self):
        await self._send(self._host, "on")
        self._is_on = True
    
    async def turn_off(self):
        await self._send(self._host, "off")
        self._is_on = False
