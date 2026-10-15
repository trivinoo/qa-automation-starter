"""
Mini 2D Game Engine Simulation with Embedded Automation RPC Bridge.

Architectural components modeled after real game engines (Unity / Unreal):
1. Game Loop with delta-time (dt) tick execution.
2. GameObject Hierarchy with Transform (x, y, z) and Tags.
3. Component-Based Architecture:
   - Transform
   - HealthComponent
   - InventoryComponent
   - WeaponComponent
   - Collider2D
4. Physics & Distance Math (Hitbox checks, collision resolution).
5. Embedded JSON-RPC Server: Exposes scene tree and allows simulated inputs,
   identical to AltTester (AltUnity) or Airtest Poco.
"""

import math
import time
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List, Optional, Any

# ==============================================================================
# 1. Component Model
# ==============================================================================

class Component:
    def __init__(self, name: str):
        self.name = name
        self.game_object: Optional['GameObject'] = None

    def serialize(self) -> Dict[str, Any]:
        return {"type": self.name}

class Transform(Component):
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        super().__init__("Transform")
        self.x = x
        self.y = y
        self.z = z

    def translate(self, dx: float, dy: float, dz: float = 0.0):
        self.x += dx
        self.y += dy
        self.z += dz

    def serialize(self) -> Dict[str, Any]:
        return {"type": "Transform", "position": {"x": self.x, "y": self.y, "z": self.z}}

class HealthComponent(Component):
    def __init__(self, max_hp: int = 100):
        super().__init__("HealthComponent")
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.is_alive = True

    def take_damage(self, amount: int) -> int:
        if not self.is_alive:
            return 0
        actual_damage = max(0, amount)
        self.current_hp = max(0, self.current_hp - actual_damage)
        if self.current_hp == 0:
            self.is_alive = False
        return actual_damage

    def heal(self, amount: int) -> int:
        if not self.is_alive:
            return 0
        prev = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp - prev

    def serialize(self) -> Dict[str, Any]:
        return {
            "type": "HealthComponent",
            "current_hp": self.current_hp,
            "max_hp": self.max_hp,
            "is_alive": self.is_alive
        }

class InventoryComponent(Component):
    def __init__(self, max_slots: int = 6):
        super().__init__("InventoryComponent")
        self.max_slots = max_slots
        self.items: List[Dict[str, Any]] = []
        self.gold: int = 100

    def add_item(self, item_id: str, name: str, quantity: int = 1) -> bool:
        if len(self.items) >= self.max_slots:
            return False
        self.items.append({"id": item_id, "name": name, "quantity": quantity})
        return True

    def remove_item(self, item_id: str) -> bool:
        for idx, item in enumerate(self.items):
            if item["id"] == item_id:
                self.items.pop(idx)
                return True
        return False

    def serialize(self) -> Dict[str, Any]:
        return {
            "type": "InventoryComponent",
            "items": self.items,
            "item_count": len(self.items),
            "max_slots": self.max_slots,
            "gold": self.gold
        }

class WeaponComponent(Component):
    def __init__(self, weapon_name: str = "Iron Sword", base_damage: int = 25, attack_range: float = 2.0):
        super().__init__("WeaponComponent")
        self.weapon_name = weapon_name
        self.base_damage = base_damage
        self.attack_range = attack_range

    def serialize(self) -> Dict[str, Any]:
        return {
            "type": "WeaponComponent",
            "name": self.weapon_name,
            "damage": self.base_damage,
            "range": self.attack_range
        }

class Collider2D(Component):
    def __init__(self, radius: float = 1.0):
        super().__init__("Collider2D")
        self.radius = radius

    def serialize(self) -> Dict[str, Any]:
        return {"type": "Collider2D", "radius": self.radius}

# ==============================================================================
# 2. GameObject Architecture
# ==============================================================================

class GameObject:
    def __init__(self, name: str, tag: str = "Untagged"):
        self.name = name
        self.tag = tag
        self.components: Dict[str, Component] = {}
        self.transform = Transform()
        self.add_component(self.transform)

    def add_component(self, component: Component):
        component.game_object = self
        self.components[component.name] = component

    def get_component(self, comp_name: str) -> Optional[Component]:
        return self.components.get(comp_name)

    def distance_to(self, other: 'GameObject') -> float:
        dx = self.transform.x - other.transform.x
        dy = self.transform.y - other.transform.y
        dz = self.transform.z - other.transform.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def serialize(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "tag": self.tag,
            "components": {k: v.serialize() for k, v in self.components.items()}
        }

# ==============================================================================
# 3. Game Scene & Engine Loop
# ==============================================================================

class MiniGameScene:
    def __init__(self):
        self.game_objects: Dict[str, GameObject] = {}
        self.game_state: str = "INIT"  # INIT, MENU, PLAYING, PAUSED, GAME_OVER, VICTORY
        self.tick_count: int = 0
        self.fps: float = 60.0
        self.is_running: bool = False
        self.reset_scene()

    def reset_scene(self):
        self.game_objects.clear()
        self.game_state = "MENU"
        self.tick_count = 0

        # Create Player
        player = GameObject("Player", tag="Player")
        player.transform.x = 0.0
        player.transform.y = 0.0
        player.add_component(HealthComponent(max_hp=100))
        player.add_component(InventoryComponent(max_slots=4))
        player.add_component(WeaponComponent("Steel Blade", base_damage=30, attack_range=2.5))
        player.add_component(Collider2D(radius=0.8))
        self.add_game_object(player)

        # Create Enemies
        goblin = GameObject("Goblin_Alpha", tag="Enemy")
        goblin.transform.x = 2.0
        goblin.transform.y = 0.0
        goblin.add_component(HealthComponent(max_hp=50))
        goblin.add_component(WeaponComponent("Dagger", base_damage=12, attack_range=1.5))
        goblin.add_component(Collider2D(radius=0.6))
        self.add_game_object(goblin)

        boss = GameObject("Dragon_Boss", tag="Boss")
        boss.transform.x = 10.0
        boss.transform.y = 5.0
        boss.add_component(HealthComponent(max_hp=250))
        boss.add_component(WeaponComponent("Fire Breath", base_damage=45, attack_range=4.0))
        boss.add_component(Collider2D(radius=2.0))
        self.add_game_object(boss)

        # Create In-game Chest / Pickable
        chest = GameObject("TreasureChest", tag="Interactable")
        chest.transform.x = 1.0
        chest.transform.y = 1.0
        self.add_game_object(chest)

    def add_game_object(self, obj: GameObject):
        self.game_objects[obj.name] = obj

    def remove_game_object(self, name: str):
        if name in self.game_objects:
            del self.game_objects[name]

    def get_game_object(self, name: str) -> Optional[GameObject]:
        return self.game_objects.get(name)

    def update_tick(self, dt: float = 0.016):
        """Simulates one engine tick delta (60 FPS default = ~16ms)."""
        if self.game_state != "PLAYING":
            return
        self.tick_count += 1
        
        # Check death states
        player = self.get_game_object("Player")
        if player:
            hp = player.get_component("HealthComponent")
            if hp and not hp.is_alive:
                self.game_state = "GAME_OVER"

# Global scene instance
SCENE = MiniGameScene()

# ==============================================================================
# 4. In-Engine Embedded RPC Bridge (AltTester / Airtest Poco Pattern)
# ==============================================================================

class EngineRPCServer(BaseHTTPRequestHandler):
    def _respond(self, status: int, data: Any):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/engine/hierarchy":
            # Returns complete scene object tree
            tree = {name: obj.serialize() for name, obj in SCENE.game_objects.items()}
            self._respond(200, {"state": SCENE.game_state, "objects": tree, "ticks": SCENE.tick_count})
        elif self.path.startswith("/engine/object/"):
            name = self.path.split("/engine/object/")[1]
            obj = SCENE.get_game_object(name)
            if obj:
                self._respond(200, obj.serialize())
            else:
                self._respond(404, {"error": f"GameObject '{name}' not found in scene"})
        elif self.path == "/engine/status":
            self._respond(200, {"status": "running", "engine": "MiniGameEngine-Python", "state": SCENE.game_state})
        else:
            self._respond(404, {"error": "Unknown endpoint"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        payload = json.loads(body)

        if self.path == "/engine/reset":
            SCENE.reset_scene()
            self._respond(200, {"success": True, "message": "Scene reset to defaults"})

        elif self.path == "/engine/set_state":
            new_state = payload.get("state")
            SCENE.game_state = new_state
            self._respond(200, {"success": True, "state": SCENE.game_state})

        elif self.path == "/engine/input/move":
            obj_name = payload.get("object", "Player")
            dx = float(payload.get("dx", 0.0))
            dy = float(payload.get("dy", 0.0))
            obj = SCENE.get_game_object(obj_name)
            if obj:
                obj.transform.translate(dx, dy)
                SCENE.update_tick()
                self._respond(200, {"success": True, "position": obj.transform.serialize()["position"]})
            else:
                self._respond(404, {"error": f"GameObject '{obj_name}' not found"})

        elif self.path == "/engine/action/attack":
            attacker_name = payload.get("attacker", "Player")
            target_name = payload.get("target")
            attacker = SCENE.get_game_object(attacker_name)
            target = SCENE.get_game_object(target_name)

            if not attacker or not target:
                self._respond(404, {"error": "Attacker or target not found"})
                return

            dist = attacker.distance_to(target)
            weapon = attacker.get_component("WeaponComponent")
            w_range = weapon.attack_range if weapon else 1.5
            w_dmg = weapon.base_damage if weapon else 10

            if dist > w_range:
                self._respond(200, {"success": False, "reason": "OUT_OF_RANGE", "distance": dist, "range": w_range})
                return

            target_hp = target.get_component("HealthComponent")
            if target_hp:
                dealt = target_hp.take_damage(w_dmg)
                SCENE.update_tick()
                self._respond(200, {
                    "success": True,
                    "damage_dealt": dealt,
                    "target_current_hp": target_hp.current_hp,
                    "target_alive": target_hp.is_alive
                })
            else:
                self._respond(400, {"error": "Target has no HealthComponent"})

        elif self.path == "/engine/action/loot":
            player = SCENE.get_game_object("Player")
            inv = player.get_component("InventoryComponent") if player else None
            item_id = payload.get("item_id", "potion_hp")
            item_name = payload.get("item_name", "Health Potion")
            
            if inv:
                success = inv.add_item(item_id, item_name)
                self._respond(200, {"success": success, "items": inv.items, "full": not success})
            else:
                self._respond(400, {"error": "No inventory component found"})

        elif self.path == "/engine/tick":
            # Advance simulation frames programmatically
            ticks = int(payload.get("ticks", 1))
            for _ in range(ticks):
                SCENE.update_tick()
            self._respond(200, {"ticks_advanced": ticks, "total_ticks": SCENE.tick_count})

        else:
            self._respond(404, {"error": "Unknown command"})

    def log_message(self, format, *args):
        # Keep test runs clean
        return

def run_server(port: int = 9191):
    server = HTTPServer(("127.0.0.1", port), EngineRPCServer)
    server.serve_forever()

if __name__ == "__main__":
    print(f"🎮 Mini Game Engine RPC Server running on http://127.0.0.1:9191")
    run_server()
