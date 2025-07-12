import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN
from .api import RockstorAPI

class RockstorNasConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input["host"]
            username = user_input["username"]
            password = user_input["password"]
            update_interval = user_input["update_interval"]

            api = RockstorAPI(host, username, password)
            try:
                await self.hass.async_add_executor_job(api.get_pool_stats)
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Rockstor NAS ({host})",
                    data={
                        "host": host,
                        "username": username,
                        "password": password,
                        "update_interval": update_interval,
                    },
                )

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
            vol.Optional("update_interval", default=60): int,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
