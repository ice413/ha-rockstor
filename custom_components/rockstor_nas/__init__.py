from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .api import RockstorAPI
from .coordinator import RockstorCoordinator
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data.get("host")
    username = entry.data.get("username")
    password = entry.data.get("password")
    update_interval = entry.options.get("update_interval", entry.data.get("update_interval", 60))

    try:
        api = RockstorAPI(host, username, password, verify_ssl=False)
        coordinator = RockstorCoordinator(hass, api, update_interval)
        await coordinator.async_config_entry_first_refresh()

        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = coordinator

        await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "switch"])

        entry.async_on_unload(entry.add_update_listener(update_listener))

        _LOGGER.info("Rockstor NAS integration successfully set up for host: %s", host)
        return True

    except Exception as e:
        _LOGGER.error("Failed to set up Rockstor NAS integration for host %s: %s", host, e)
        return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, ["sensor", "switch"])
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)
