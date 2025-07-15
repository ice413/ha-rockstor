from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
import logging
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    service_stats = coordinator.data.get("services", [])

    switches = [
        RockstorServiceSwitch(coordinator, service)
        for service in service_stats
    ]

    async_add_entities(switches)


class RockstorServiceSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, service):
        super().__init__(coordinator)
        self._service = service
        self._attr_name = f"Rockstor {service['display_name']}"
        self._attr_unique_id = f"rockstor_service_switch_{service['id']}"

    @property
    def is_on(self):
        return self._service.get("status", False)

    async def async_turn_on(self, **kwargs):
        _LOGGER.debug("Turning ON service: %s (ID: %s)", self._service["display_name"], self._service["id"])
        result = await self.hass.async_add_executor_job(
            self.coordinator.api.toggle_service, self._service["id"], True
        )
        _LOGGER.debug("Service ON result: %s", result)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        _LOGGER.debug("Turning OFF service: %s (ID: %s)", self._service["display_name"], self._service["id"])
        result = await self.hass.async_add_executor_job(
            self.coordinator.api.toggle_service, self._service["id"], False
        )
        _LOGGER.debug("Service OFF result: %s", result)
        await self.coordinator.async_request_refresh()
