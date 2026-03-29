import requests
from typing import Optional, Dict, Any, List

class PRCClientV2:
    BASE_URL = "https://api.policeroleplay.community/v2"

    MAPS = {
        "fall_blank": "https://api.policeroleplay.community/maps/fall_blank.png",
        "fall_postals": "https://api.policeroleplay.community/maps/fall_postals.png",
    }

    def __init__(self, server_key: str):
        self.server_key = server_key

    def _headers(self) -> Dict[str, str]:
        return {
            "server-key": self.server_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _handle(self, response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            return {
                "success": False,
                "status_code": response.status_code,
                "error_message": response.text,
                "data": None,
                "error_code": 0,
            }

        if response.status_code >= 400:
            return {
                "success": False,
                "status_code": response.status_code,
                "error_message": data.get("message", "Unknown error"),
                "data": data,
                "error_code": data.get("error_code", 0),
            }

        return {
            "success": True,
            "status_code": response.status_code,
            "data": data,
            "error_message": None,
            "error_code": 0,
        }

    def _get(self, endpoint: str, **params) -> Dict[str, Any]:
        try:
            r = requests.get(
                f"{self.BASE_URL}/{endpoint}",
                headers=self._headers(),
                params=params
            )
        except requests.RequestException as e:
            return {
                "success": False,
                "status_code": 0,
                "error_message": str(e),
                "data": None,
                "error_code": 0,
            }

        return self._handle(r)

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            r = requests.post(
                f"{self.BASE_URL}/{endpoint}",
                headers=self._headers(),
                json=payload
            )
        except requests.RequestException as e:
            return {
                "success": False,
                "status_code": 0,
                "error_message": str(e),
                "data": None,
                "error_code": 0,
            }

        return self._handle(r)

    def get_server_status(self):
        return self._get("server")

    def _get_data_field(self, field: str) -> Dict[str, Any]:
        res = self._get("server", **{field: True})

        if not res["success"]:
            return res

        data = res["data"]

        if isinstance(data, dict) and field in data:
            return {
                "success": True,
                "status_code": res["status_code"],
                "data": data[field],
                "error_message": None,
                "error_code": 0,
            }

        return {
            "success": False,
            "status_code": res["status_code"],
            "data": None,
            "error_message": f"{field} not found in response",
            "error_code": 0,
        }

    def get_players_raw(self):
        return self._get_data_field("Players")

    def get_staff(self):
        return self._get_data_field("Staff")

    def get_queue(self):
        return self._get_data_field("Queue")

    def get_join_logs(self):
        return self._get_data_field("JoinLogs")

    def get_kill_logs(self):
        return self._get_data_field("KillLogs")

    def get_command_logs(self):
        return self._get_data_field("CommandLogs")

    def get_mod_calls(self):
        return self._get_data_field("ModCalls")

    def get_emergency_calls(self):
        return self._get_data_field("EmergencyCalls")

    def get_vehicles(self):
        return self._get_data_field("Vehicles")

    def get_all_data(self):
        return self._get(
            "server",
            Players=True,
            Staff=True,
            Queue=True,
            JoinLogs=True,
            KillLogs=True,
            CommandLogs=True,
            ModCalls=True,
            EmergencyCalls=True,
            Vehicles=True
        )

    def run_command(self, command: str):
        return self._post("server/command", {"command": command})

    def get_players(self) -> Dict[str, Any]:
        res = self.get_players_raw()
        if not res["success"]:
            return res

        players = res["data"] if isinstance(res["data"], list) else []
        parsed = []

        for p in players:
            loc = p.get("Location", {}) if isinstance(p, dict) else {}

            parsed.append({
                "player": p.get("Player"),
                "team": p.get("Team"),
                "callsign": p.get("Callsign"),
                "permission": p.get("Permission"),
                "wanted_stars": p.get("WantedStars"),

                "x": loc.get("LocationX"),
                "z": loc.get("LocationZ"),

                "postal": loc.get("PostalCode"),
                "street": loc.get("StreetName"),
                "building": loc.get("BuildingNumber"),

                "formatted_location": self._format_location(loc),
            })

        return {
            "success": True,
            "status_code": res["status_code"],
            "data": parsed,
            "error_message": None,
            "error_code": 0,
        }

    def _format_location(self, loc: Dict[str, Any]) -> str:
        if not loc:
            return "Unknown"

        parts = []

        if loc.get("BuildingNumber"):
            parts.append(str(loc["BuildingNumber"]))

        if loc.get("StreetName"):
            parts.append(loc["StreetName"])

        result = " ".join(parts)

        if loc.get("PostalCode"):
            result += f" (Postal {loc['PostalCode']})"

        return result or "Unknown"

    def get_player_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        res = self.get_players()
        if not res["success"]:
            return None

        for p in res["data"]:
            if name.lower() in (p.get("player") or "").lower():
                return p

        return None

    def get_players_by_postal(self, postal: str) -> List[Dict[str, Any]]:
        res = self.get_players()
        if not res["success"]:
            return []

        return [p for p in res["data"] if p.get("postal") == postal]

    def get_map_url(self, map_type: str = "fall_postals") -> str:
        return self.MAPS.get(map_type, self.MAPS["fall_postals"])