from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

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
        return self._service["status"]

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(
            self.coordinator.api.toggle_service, self._service["id"], True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(
            self.coordinator.api.toggle_service, self._service["id"], False
        )
        await self.coordinator.async_request_refresh()
