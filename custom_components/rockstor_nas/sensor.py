from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    pool_stats = coordinator.data.get("pools", [])
    share_stats = coordinator.data.get("shares", [])

    _LOGGER.debug("Rockstor sensor setup: pool_stats = %s", pool_stats)
    _LOGGER.debug("Rockstor sensor setup: share_stats = %s", share_stats)

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
        for pool in self.coordinator.data:
            if pool["name"] == self._pool_name:
                value = pool[self._metric]
                # Convert if necessary
                # value = value_in_mb / 1024 if needed
                return round(value, 2)
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
        for share in self.coordinator.data:
            if share["name"] == self._share_name:
                value = share[self._metric]
                # Convert if necessary
                # value = value_in_mb / 1024 if needed
                return round(value, 2)
        return None
