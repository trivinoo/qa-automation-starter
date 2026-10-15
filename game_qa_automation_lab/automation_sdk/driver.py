"""
Game Automation SDK (Python).

Mirrors the design patterns of AltTester (AltUnity Driver) and Airtest Poco.
Provides high-level GameDriver and GameElement abstractions so automated tests
can interact with in-game objects seamlessly:
- driver.find_element_by_name("Player")
- element.get_component("HealthComponent")
- driver.move_object("Player", dx=1.5, dy=0.0)
- driver.attack(attacker="Player", target="Goblin_Alpha")
"""

import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List

class GameElement:
    def __init__(self, data: Dict[str, Any], driver: 'GameDriver'):
        self.raw_data = data
        self.driver = driver
        self.name: str = data.get("name", "")
        self.tag: str = data.get("tag", "Untagged")
        self.components: Dict[str, Any] = data.get("components", {})

    @property
    def position(self) -> Dict[str, float]:
        transform = self.components.get("Transform", {})
        return transform.get("position", {"x": 0.0, "y": 0.0, "z": 0.0})

    def get_component(self, component_name: str) -> Optional[Dict[str, Any]]:
        return self.components.get(component_name)

    def refresh(self):
        fresh = self.driver.find_element_by_name(self.name)
        if fresh:
            self.raw_data = fresh.raw_data
            self.components = fresh.components

class GameDriver:
    def __init__(self, host: str = "127.0.0.1", port: int = 9191):
        self.base_url = f"http://{host}:{port}"

    def _get(self, path: str) -> Dict[str, Any]:
        req = urllib.request.Request(f"{self.base_url}{path}")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())

    def reset_scene(self) -> bool:
        res = self._post("/engine/reset", {})
        return res.get("success", False)

    def set_game_state(self, state: str) -> bool:
        res = self._post("/engine/set_state", {"state": state})
        return res.get("success", False)

    def get_game_state(self) -> str:
        res = self._get("/engine/status")
        return res.get("state", "UNKNOWN")

    def find_element_by_name(self, name: str) -> Optional[GameElement]:
        try:
            data = self._get(f"/engine/object/{name}")
            return GameElement(data, self)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise

    def find_elements_by_tag(self, tag: str) -> List[GameElement]:
        hierarchy = self._get("/engine/hierarchy")
        objects = hierarchy.get("objects", {})
        matches = []
        for obj_name, data in objects.items():
            if data.get("tag") == tag:
                matches.append(GameElement(data, self))
        return matches

    def move_object(self, name: str, dx: float, dy: float) -> Dict[str, float]:
        res = self._post("/engine/input/move", {"object": name, "dx": dx, "dy": dy})
        return res.get("position", {})

    def attack(self, attacker: str, target: str) -> Dict[str, Any]:
        return self._post("/engine/action/attack", {"attacker": attacker, "target": target})

    def loot_item(self, item_id: str, item_name: str) -> Dict[str, Any]:
        return self._post("/engine/action/loot", {"item_id": item_id, "item_name": item_name})

    def advance_ticks(self, ticks: int = 1) -> int:
        res = self._post("/engine/tick", {"ticks": ticks})
        return res.get("ticks_advanced", 0)
