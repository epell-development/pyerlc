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

    def _build_headers(self) -> Dict[str, str]:
        return {
            "server-key": self.server_key,
            "Accept": "application/json",
        }

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except ValueError:
            return {
                "success": False,
                "status_code": response.status_code,
                "error_message": f"Invalid JSON response: {response.text}",
                "data": None,
            }

        if response.status_code >= 400:
            return {
                "success": False,
                "status_code": response.status_code,
                "error_message": data.get("message", "Unknown error"),
                "data": data,
            }

        return {
            "success": True,
            "status_code": response.status_code,
            "data": data,
        }

    def _get_server(self, **query_params) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/server"
        headers = self._build_headers()

        try:
            response = requests.get(url, headers=headers, params=query_params)
        except requests.RequestException as e:
            return {
                "success": False,
                "status_code": 0,
                "error_message": str(e),
                "data": None,
            }

        return self._handle_response(response)

    def get_players_raw(self):
        return self._get_server(Players=True)

    def get_players(self) -> Dict[str, Any]:
        res = self.get_players_raw()
        if not res["success"]:
            return res

        players = res["data"].get("Players", [])

        parsed_players = []
        for p in players:
            loc = p.get("Location", {})

            parsed_players.append({
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

        res["data"]["Players"] = parsed_players
        return res
    def _format_location(self, loc: Dict[str, Any]) -> str:
        if not loc:
            return "Unknown"

        parts = []

        if loc.get("BuildingNumber"):
            parts.append(loc["BuildingNumber"])

        if loc.get("StreetName"):
            parts.append(loc["StreetName"])

        location_str = " ".join(parts)

        if loc.get("PostalCode"):
            location_str += f" (Postal {loc['PostalCode']})"

        return location_str or "Unknown"

    def get_player_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        res = self.get_players()
        if not res["success"]:
            return None

        for player in res["data"]["Players"]:
            if name.lower() in player["player"].lower():
                return player

        return None

    def get_players_by_postal(self, postal: str) -> List[Dict[str, Any]]:
        res = self.get_players()
        if not res["success"]:
            return []

        return [
            p for p in res["data"]["Players"]
            if p.get("postal") == postal
        ]

    def get_map_url(self, map_type: str = "fall_postals") -> str:
        return self.MAPS.get(map_type, self.MAPS["fall_postals"])

    def run_command(self, command: str):
        url = f"{self.BASE_URL}/server/command"
        headers = self._build_headers()

        try:
            response = requests.post(
                url,
                headers=headers,
                json={"command": command}
            )
        except requests.RequestException as e:
            return {
                "success": False,
                "status_code": 0,
                "error_message": str(e),
                "data": None,
            }

        return self._handle_response(response)