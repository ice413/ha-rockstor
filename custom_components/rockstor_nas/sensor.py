from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    pool_stats = coordinator.data.get("pools", [])
    share_stats = coordinator.data.get("shares", [])
    rockon_stats = coordinator.data.get("rockons", [])

    _LOGGER.debug("Rockstor sensor setup: pool_stats = %s", pool_stats)
    _LOGGER.debug("Rockstor sensor setup: share_stats = %s", share_stats)
    _LOGGER.debug("Rockstor sensor setup: rockon_stats = %s", rockon_stats)

    sensors = []

    # Pool sensors
    for pool in pool_stats:
        name = pool["name"]
        sensors.append(RockstorPoolSensor(coordinator, name, "used"))
        sensors.append(RockstorPoolSensor(coordinator, name, "free"))
        sensors.append(RockstorPoolSensor(coordinator, name, "size"))

    # Share sensors
    for share in share_stats:
        name = share["name"]
        sensors.append(RockstorShareSensor(coordinator, name, "used"))
        sensors.append(RockstorShareSensor(coordinator, name, "free"))
        sensors.append(RockstorShareSensor(coordinator, name, "size"))

    # Rock-on sensor
    sensors.append(RockstorRockonSensor(coordinator))

    async_add_entities(sensors, True)



class RockstorPoolSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False

    def __init__(self, coordinator, pool_name, metric):
        super().__init__(coordinator)
        self._pool_name = pool_name
        self._metric = metric
        self._attr_name = f"Rockstor Pool {pool_name} {metric.capitalize()}"
        self._attr_unique_id = f"rockstor_{pool_name}_{metric}"
        self._attr_native_unit_of_measurement = "GB"
        self._attr_state_class = "measurement"
        self._attr_suggested_display_precision = 2

    @property
    def native_value(self):
        for pool in self.coordinator.data["pools"]:
            if pool["name"] == self._pool_name:
                return round(pool[self._metric], 2)
        return None


class RockstorShareSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False

    def __init__(self, coordinator, share_name, metric):
        super().__init__(coordinator)
        self._share_name = share_name
        self._metric = metric
        self._attr_name = f"Rockstor Share {share_name} {metric.capitalize()}"
        self._attr_unique_id = f"rockstor_{share_name}_{metric}"
        self._attr_native_unit_of_measurement = "GB"
        self._attr_state_class = "measurement"
        self._attr_suggested_display_precision = 2

    @property
    def native_value(self):
        for share in self.coordinator.data["shares"]:
            if share["name"] == self._share_name:
                return round(share[self._metric], 2)
        return None

class RockstorRockonSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False
    _attr_native_unit_of_measurement = None
    _attr_icon = "mdi:docker"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Rockstor Installed Rock-ons"
        self._attr_unique_id = "rockstor_installed_rock_ons"
        self._attr_state_class = None

    @property
    def native_value(self):
        return len(self.coordinator.data.get("rockons", []))

    @property
    def extra_state_attributes(self):
        return {
            "Installed": {
                rockon["name"]: rockon["status"]
                for rockon in self.coordinator.data.get("rockons", [])
            }
        }

class RockstorServiceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, service):
        super().__init__(coordinator)
        self._service = service
        self._attr_name = f"Rockstor {service['display_name']}"
        self._attr_unique_id = f"rockstor_service_{service['id']}"


    @property
    def state(self):
        return "running" if self._service["status"] else "stopped"

    async def async_update(self):
        await self.coordinator.async_request_refresh()

