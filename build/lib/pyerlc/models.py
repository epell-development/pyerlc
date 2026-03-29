from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Dict, List
from datetime import datetime


class ErrorCode(Enum):
    UNKNOWN = 0
    ROBLOX_COMM_ERROR = 1001
    INTERNAL_ERROR = 1002
    NO_SERVER_KEY = 2000
    INVALID_SERVER_KEY_FORMAT = 2001
    INVALID_SERVER_KEY = 2002
    INVALID_GLOBAL_API_KEY = 2003
    BANNED_SERVER_KEY = 2004
    INVALID_COMMAND = 3001
    SERVER_OFFLINE = 3002
    RATE_LIMITED = 4001
    RESTRICTED_COMMAND = 4002
    PROHIBITED_MESSAGE = 4003
    RESTRICTED_RESOURCE = 9998
    OUTDATED_MODULE = 9999

@dataclass
class PRCResponse:
    success: bool
    status_code: int
    data: Optional[Any] = None
    error_code: Optional[ErrorCode] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    def __bool__(self) -> bool:
        return self.success

@dataclass
class PlayerLocation:
    x: float
    z: float
    postal_code: Optional[str]
    street_name: Optional[str]
    building_number: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayerLocation":
        return cls(
            x=data.get("LocationX", 0.0),
            z=data.get("LocationZ", 0.0),
            postal_code=data.get("PostalCode"),
            street_name=data.get("StreetName"),
            building_number=data.get("BuildingNumber"),
        )

    def formatted(self) -> str:
        parts = []
        if self.building_number:
            parts.append(self.building_number)
        if self.street_name:
            parts.append(self.street_name)

        base = " ".join(parts)

        if self.postal_code:
            base += f" (Postal {self.postal_code})"

        return base or "Unknown"


@dataclass
class Player:
    player: str
    team: str
    permission: str
    callsign: Optional[str]
    wanted_stars: int
    location: Optional[PlayerLocation]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        loc = data.get("Location")

        return cls(
            player=data.get("Player", ""),
            team=data.get("Team", ""),
            permission=data.get("Permission", ""),
            callsign=data.get("Callsign"),
            wanted_stars=data.get("WantedStars", 0),
            location=PlayerLocation.from_dict(loc) if loc else None,
        )


@dataclass
class ServerStatus:
    name: str
    owner_id: int
    co_owner_ids: List[int]
    current_players: int
    max_players: int
    join_key: str
    acc_verified_req: str  # FIXED (was bool, actually string)
    team_balance: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ServerStatus":
        return cls(
            name=data.get("Name", ""),
            owner_id=data.get("OwnerId", 0),
            co_owner_ids=data.get("CoOwnerIds", []),
            current_players=data.get("CurrentPlayers", 0),
            max_players=data.get("MaxPlayers", 0),
            join_key=data.get("JoinKey", ""),
            acc_verified_req=data.get("AccVerifiedReq", ""),
            team_balance=data.get("TeamBalance", False),
        )

@dataclass
class Staff:
    admins: Dict[str, str]
    mods: Dict[str, str]
    helpers: Dict[str, str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Staff":
        return cls(
            admins=data.get("Admins", {}),
            mods=data.get("Mods", {}),
            helpers=data.get("Helpers", {}),
        )

def _ts(ts: int) -> datetime:
    return datetime.fromtimestamp(ts) if ts else datetime.fromtimestamp(0)


@dataclass
class JoinLog:
    join: bool
    timestamp: datetime
    player: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JoinLog":
        return cls(
            join=data.get("Join", False),
            timestamp=_ts(data.get("Timestamp")),
            player=data.get("Player", ""),
        )


@dataclass
class KillLog:
    timestamp: datetime
    killer: str
    killed: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KillLog":
        return cls(
            timestamp=_ts(data.get("Timestamp")),
            killer=data.get("Killer", ""),
            killed=data.get("Killed", ""),
        )


@dataclass
class CommandLog:
    timestamp: datetime
    player: str
    command: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CommandLog":
        return cls(
            timestamp=_ts(data.get("Timestamp")),
            player=data.get("Player", ""),
            command=data.get("Command", ""),
        )


@dataclass
class ModCall:
    timestamp: datetime
    caller: str
    moderator: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModCall":
        return cls(
            timestamp=_ts(data.get("Timestamp")),
            caller=data.get("Caller", ""),
            moderator=data.get("Moderator"),
        )

@dataclass
class EmergencyCall:
    team: str
    caller: int
    players: List[int]
    position: List[float]
    started_at: datetime
    call_number: int
    description: str
    position_descriptor: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmergencyCall":
        return cls(
            team=data.get("Team", ""),
            caller=data.get("Caller", 0),
            players=data.get("Players", []),
            position=data.get("Position", []),
            started_at=_ts(data.get("StartedAt")),
            call_number=data.get("CallNumber", 0),
            description=data.get("Description", ""),
            position_descriptor=data.get("PositionDescriptor", ""),
        )

@dataclass
class Vehicle:
    name: str
    owner: str
    plate: Optional[str]
    texture: Optional[str]
    color_hex: Optional[str]
    color_name: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vehicle":
        return cls(
            name=data.get("Name", ""),
            owner=data.get("Owner", ""),
            plate=data.get("Plate"),
            texture=data.get("Texture"),
            color_hex=data.get("ColorHex"),
            color_name=data.get("ColorName"),
        )