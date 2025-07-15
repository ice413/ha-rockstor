import requests
from requests.auth import HTTPBasicAuth
import urllib3

import logging

_LOGGER = logging.getLogger(__name__)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RockstorAPI:
    def __init__(self, host, username, password, verify_ssl=False):
        self._host = host.rstrip("/")
        self._session = requests.Session()
        self._verify_ssl = verify_ssl
        self._session.auth = HTTPBasicAuth(username, password)
        self._session.headers.update({
            "Content-Type": "application/json"
        })


    def get_pool_stats(self):
        url = f"{self._host}/api/pools"
        try:
            response = self._session.get(url, verify=self._verify_ssl)
            response.raise_for_status()
            data = response.json()
            pools = data.get("results", [])

            parsed_pools = [
                {
                    "name": pool["name"],
                    "size": round(int(pool["size"]) / 1024 / 1024, 2),
                    "free": round(int(pool["free"]) / 1024 / 1024, 2),
                    "used": round((int(pool["size"]) - int(pool["free"])) / 1024 / 1024, 2)
                }
                for pool in pools
            ]

            print("✅ Parsed pool stats (GB):", parsed_pools)
            return parsed_pools

        except requests.RequestException as e:
            print("❌ Failed to fetch pool stats:", e)
            return []


    def get_share_stats(self):
        url = f"{self._host}/api/shares"
        try:
            response = self._session.get(url, verify=self._verify_ssl)
            response.raise_for_status()
            data = response.json()
            shares = data.get("results", [])

            parsed_shares = [
                {
                    "name": share["name"],
                    "size": round(int(share["size"]) / 1024 / 1024, 2),  # Total allocated size
                    "used": round(int(share["rusage"]) / 1024 / 1024, 2),  # Actual used space
                    "free": round((int(share["size"]) - int(share["rusage"])) / 1024 / 1024, 2)  # Remaining space
                }
                for share in shares
            ]

            print("✅ Parsed share stats (GB):", parsed_shares)
            return parsed_shares

        except requests.RequestException as e:
            print("❌ Failed to fetch share stats:", e)
            return []

    def get_installed_rockons(self):
        """ Fetch all Rock-ons with state 'installed' and return their status. """
        installed_rockons = []
        url = f"{self._host}/api/rockons"

        while url:
            try:
                response = self._session.get(url, verify=self._verify_ssl)
                response.raise_for_status()
                data = response.json()

                # Filter only those with state "installed"
                installed = [
                    {
                        "name": rockon.get("name"),
                        "status": rockon.get("status")
                    }
                    for rockon in data.get("results", [])
                    if rockon.get("state") == "installed"
                ]
                installed_rockons.extend(installed)

                # Follow pagination
                url = data.get("next")

            except requests.RequestException as e:
                print("❌ Failed to fetch rock-ons:", e)
                break

        print("✅ Installed Rock-ons:", installed_rockons)
        return installed_rockons

    def get_services(self):
        url = f"{self._host}/api/sm/services"
        all_services = []

        while url:
            try:
                response = self._session.get(url, verify=self._verify_ssl)
                response.raise_for_status()
                data = response.json()
                services = data.get("results", [])

                parsed_services = [
                    {
                        "id": service.get("id"),
                        "name": service.get("name"),
                        "display_name": service.get("display_name"),
                        "status": service.get("status"),
                        "config": service.get("config"),
                        "count": service.get("count"),
                        "ts": service.get("ts")
                    }
                    for service in services
                ]

                all_services.extend(parsed_services)
                url = data.get("next")  # Follow pagination

            except requests.RequestException as e:
                print("❌ Failed to fetch services:", e)
                break

        print("✅ Parsed services:", all_services)
        return all_services


    def toggle_service(self, service: dict, turn_on: bool):
        required_keys = ["id", "name", "display_name", "config", "service"]
        missing_keys = [key for key in required_keys if key not in service]
        if missing_keys:
            _LOGGER.error("❌ Missing required keys in service data: %s", missing_keys)
            return False
    
        url = f"{self._host}/api/sm/services/"
        payload = {
            "id": service["id"],
            "name": service["name"],
            "display_name": service["display_name"],
            "config": service["config"],
            "service": service["service"],
            "status": turn_on
        }
        _LOGGER.debug("Sending toggle request to: %s with payload: %s", url, payload)
        try:
            response = self._session.post(url, json=payload, verify=self._verify_ssl)
            response.raise_for_status()
            _LOGGER.debug("✅ Successfully toggled service %s to %s", service["id"], turn_on)
            return True
        except requests.RequestException as e:
            _LOGGER.error("❌ Failed to toggle service %s: %s", service["id"], e)
            return False


