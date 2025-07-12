from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    pool_stats = coordinator.data

    sensors = []
    for pool in pool_stats:
        name = pool["name"]
        sensors.append(RockstorPoolSensor(coordinator, name, "used", pool["used"]))
        sensors.append(RockstorPoolSensor(coordinator, name, "free", pool["free"]))
        sensors.append(RockstorPoolSensor(coordinator, name, "size", pool["size"]))

    async_add_entities(sensors, True)

class RockstorPoolSensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, pool_name, metric, value):
        super().__init__(coordinator)
        self._pool_name = pool_name
        self._metric = metric
        self._attr_name = f"Rockstor Pool {pool_name} {metric.capitalize()}"
        self._attr_unique_id = f"rockstor_{pool_name}_{metric}"
        self._attr_native_unit_of_measurement = "MB"
        self._attr_device_class = "data_size"

    @property
    def native_value(self):
        # Get the latest value from the coordinator
        for pool in self.coordinator.data:
            if pool["name"] == self._pool_name:
                return pool[self._metric]
        return None

