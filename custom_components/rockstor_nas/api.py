import requests
from requests.auth import HTTPBasicAuth
import urllib3

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
            return [
                {
                    "name": pool["name"],
                    "size": pool["size"],
                    "free": pool["free"],
                    "used": pool["size"] - pool["free"]
                }
                for pool in pools
            ]
        except requests.RequestException as e:
            print("❌ Failed to fetch pool stats:", e)
            return []


#Endpoint	Description
#/api/pools/	List/Create storage pools
#/api/shares/	List/Create/Manage shares
#/api/snapshots/	List/Create snapshots
#/api/disks/	List physical disks
#/api/smart/	SMART status of drives
#/api/system/	System info