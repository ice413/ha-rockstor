import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class RockstorCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api, update_interval):
        """Initialize coordinator."""
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name="Rockstor NAS",
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self):
        """Fetch data from the Rockstor NAS API."""
        try:
            return await self.hass.async_add_executor_job(self._fetch_all_stats)
        except Exception as err:
            raise UpdateFailed(f"Error fetching data from Rockstor: {err}") from err

    def _fetch_all_stats(self):
        """Fetch both pool and share stats."""
        return {
            "pools": self.api.get_pool_stats(),
            "shares": self.api.get_share_stats(),
            "rockons": self.api.get_started_rockons()
        }

