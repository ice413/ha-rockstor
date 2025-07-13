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
                    "size": round(int(share["size"]) / 1024 / 1024, 2),
                    "free": round(int(share["free"]) / 1024 / 1024, 2),
                    "used": round((int(share["size"]) - int(share["free"])) / 1024 / 1024, 2)
                }
                for share in shares
            ]

            print("✅ Parsed share stats (GB):", parsed_shares)
            return parsed_shares

        except requests.RequestException as e:
            print("❌ Failed to fetch share stats:", e)
            return []

#Endpoint	Description
#/api/pools/	List/Create storage pools **
#/api/shares/	List/Create/Manage shares
#/api/snapshots/	List/Create snapshots
#/api/disks/	List physical disks
#/api/smart/	SMART status of drives
#/api/system/	System info