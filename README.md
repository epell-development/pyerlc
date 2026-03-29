# pyerlc-v2

**pyerlc-v2** is the second major version of `pyerlc`.
If you are looking for Version 1, it is deprecated and no longer maintained.

`pyerlc` is a lightweight Python SDK for the **Emergency Response: Liberty County (ER:LC) PRC API v2**.

It allows developers to interact with live server data, player locations, staff information, logs, vehicles, and execute in-game commands through a simple and modern Python interface.

---

## 🚀 Features

* 📊 Live server status monitoring
* 👥 Real-time player tracking with location data
* 📍 Postal + street-level positioning system
* 👮 Staff data (Admins / Mods / Helpers)
* 🔫 Kill, join, command, and moderation logs
* 🚓 Vehicle tracking (plates, colours, ownership)
* 📞 Emergency call monitoring
* 🧠 Remote in-game command execution
* ⚡ Single-request full server data fetch (v2 feature)

---

## 📦 Installation
** Ensure pyerlc v1 is removed **
```bash
pip install pyerlc-v2
```

---

## ⚠️ Requirements

* Python 3.12+
* Valid PRC Server Key from ER:LC server settings

---

## 🧑‍💻 Quick Start

```python
from pyerlc_v2 import PRCClientV2

client = PRCClientV2(server_key="YOUR_SERVER_KEY")

# Server status
status = client.get_server_status()
print(status)

# Get all players with location data
players = client.get_players()
print(players)

# Run an in-game command
response = client.run_command(":h Hello from pyerlc v2!")
print(response)
```

---

## 📍 Player Location System (v2)

Each player now includes live world positioning data:

```json
{
    "player": "JohnDoe:123",
    "team": "Police",
    "callsign": "5D-550",

    "x": 1084.965,
    "z": 2302.28,

    "postal": "218",
    "street": "Park Street",
    "building": "2083",

    "formatted_location": "2083 Park Street (Postal 218)"
}
```

---

## 🗺️ Map System

PRC v2 uses an X/Z coordinate system:

* **X/Z** → world position
* **Postal Code** → regional identifier
* **Street Name** → road-level detail

### Official PRC Maps

* 🗺️ Blank Map: [https://api.policeroleplay.community/maps/fall_blank.png](https://api.policeroleplay.community/maps/fall_blank.png)
* 🗺️ Postal Map: [https://api.policeroleplay.community/maps/fall_postals.png](https://api.policeroleplay.community/maps/fall_postals.png)

---

## 📡 API Methods

### 🏛️ Server Data

```python
client.get_server_status()
client.get_players()
client.get_staff()
client.get_queue()
client.get_all_data()
```

### 📊 Logs

```python
client.get_join_logs()
client.get_kill_logs()
client.get_command_logs()
client.get_mod_calls()
client.get_emergency_calls()
```

### 🚗 Vehicles

```python
client.get_vehicles()
```

**Example:**

```json
{
    "name": "Redline Fire Engine",
    "owner": "Shawnyg",
    "plate": "ABC-123",
    "texture": "Livery Name",
    "color_hex": "#ff4444",
    "color_name": "Super Red"
}
```

---

## 🧠 Commands

```python
client.run_command(":h Hello world!")
```

**Response example:**

```json
{
    "success": true,
    "status_code": 200,
    "data": {
        "message": "Success"
    }
}
```

---

## ⚡ Full Server Fetch (v2 Feature)

Fetch everything in a single request:

```python
data = client.get_all_data()
```

Includes:

* Players
* Staff
* Logs
* Vehicles
* Emergency calls
* Queue

---

## 📞 Emergency Calls

```json
{
    "team": "Police",
    "caller": 168691872,
    "players": [],
    "position": [-654.6, 666.5],
    "started_at": 1774216563,
    "call_number": 400,
    "description": "stg",
    "position_descriptor": "sdfsdfsdf"
}
```

---

## 👮 Staff Structure

```json
{
    "Admins": {
        "54249787": "PlayerName"
    },
    "Mods": {},
    "Helpers": {}
}
```

---

## 🧠 Error Handling

All responses follow this structure:

```json
{
    "success": true,
    "status_code": 200,
    "data": {},
    "error_message": "Optional error message",
    "error_code": 0
}
```

---

## ❌ Common Errors

| Code | Meaning            |
| ---- | ------------------ |
| 2000 | No server key      |
| 2002 | Invalid server key |
| 3001 | Invalid command    |
| 3002 | Server offline     |
| 4001 | Rate limited       |
| 4002 | Restricted command |

---

## 🧪 Example Use Cases

### 📍 Track a player by name

```python
player = client.get_player_by_name("JohnDoe")
print(player["formatted_location"])
```

### 📮 Find players in a postal

```python
units = client.get_players_by_postal("218")
print(units)
```

---

## 📦 Project Info

* 📦 PyPI: [https://pypi.org/project/pyerlc](https://pypi.org/project/pyerlc)
* 🏠 Website: [https://epelldevelopment.xyz](https://epelldevelopment.xyz)
* 📧 Email: [epell1@epelldevelopment.xyz](mailto:epell1@epelldevelopment.xyz)
* 💻 GitHub: [https://github.com/epell-development/pyerlc](https://github.com/epell-development/pyerlc)

---

## 📜 License

MIT License

---

⚒️ Built with ❤️ by epell Development🦘