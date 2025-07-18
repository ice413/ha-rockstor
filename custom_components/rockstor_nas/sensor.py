from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    pool_stats = coordinator.data.get("pools", [])
    _LOGGER.debug("Rockstor sensor setup: pool_stats = %s", pool_stats)
    share_stats = coordinator.data.get("shares", [])
    _LOGGER.debug("Rockstor sensor setup: share_stats = %s", share_stats)
    rockon_stats = coordinator.data.get("rockons", [])
    _LOGGER.debug("Rockstor sensor setup: rockon_stats = %s", rockon_stats)
    service_stats = coordinator.data.get("services", []) 
    _LOGGER.debug("Rockstor sensor setup: service_stats = %s", service_stats) 
    
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

    # Service sensors
    sensors.append(RockstorServiceSummarySensor(coordinator))
    _LOGGER.debug("Rockstor sensor setup: sensors = %s", sensors)

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


class RockstorServiceSummarySensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False
    _attr_native_unit_of_measurement = None
    _attr_icon = "mdi:server-network"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Rockstor Services"
        self._attr_unique_id = "rockstor_services_summary"
        self._attr_state_class = None

    @property
    def native_value(self):
        return len(self.coordinator.data.get("services", []))

    @property
    def extra_state_attributes(self):
        return {
            "Services": {
                service["display_name"]: "Started" if service["status"] else "Stopped"
                for service in self.coordinator.data.get("services", [])
            }
        }

