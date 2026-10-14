"""
Mock Game Engine Simulation with Remote Automation Bridge.

In game development (Unreal / Unity / Custom), tests interact with the game via:
- Unreal Gauntlet / Automation Driver
- AltTester / AltUnity Driver
- Embedded WebSocket or TCP command servers

This module provides a running simulation of game mechanics:
- Player state (Health, Stamina, Position)
- Inventory system with item caps
- Game state machine (MENU -> LOADING -> PLAYING -> PAUSED -> GAME_OVER)
- An RPC socket/HTTP bridge allowing external automation harnesses to query and act.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time

class GameWorldState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = "MAIN_MENU"  # MAIN_MENU, LOADING, PLAYING, PAUSED, GAME_OVER
        self.player = {
            "name": "Knight",
            "hp": 100,
            "max_hp": 100,
            "stamina": 100,
            "position": {"x": 0.0, "y": 0.0, "z": 0.0},
            "inventory": [],
            "max_inventory_slots": 5
        }
        self.enemies = [
            {"id": "goblin_1", "hp": 30, "alive": True}
        ]

    def set_game_state(self, new_state: str):
        allowed = ["MAIN_MENU", "LOADING", "PLAYING", "PAUSED", "GAME_OVER"]
        if new_state in allowed:
            self.state = new_state
            return True
        return False

    def player_take_damage(self, amount: int):
        if self.state != "PLAYING":
            return {"error": "Cannot take damage outside PLAYING state"}
        self.player["hp"] = max(0, self.player["hp"] - amount)
        if self.player["hp"] == 0:
            self.state = "GAME_OVER"
        return {"hp": self.player["hp"], "state": self.state}

    def player_heal(self, amount: int):
        if self.state != "PLAYING":
            return {"error": "Cannot heal outside PLAYING state"}
        self.player["hp"] = min(self.player["max_hp"], self.player["hp"] + amount)
        return {"hp": self.player["hp"]}

    def add_item_to_inventory(self, item_name: str):
        if len(self.player["inventory"]) >= self.player["max_inventory_slots"]:
            return {"success": False, "reason": "INVENTORY_FULL"}
        self.player["inventory"].append(item_name)
        return {"success": True, "count": len(self.player["inventory"])}

# Global world instance
WORLD = GameWorldState()

class GameAutomationRPCHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/game/state":
            self._send(200, {
                "engine_state": WORLD.state,
                "player": WORLD.player,
                "enemies": WORLD.enemies
            })
        elif self.path == "/game/health":
            self._send(200, {"status": "ok", "engine": "Simulated Unreal/Unity Core"})
        else:
            self._send(404, {"error": "Unknown endpoint"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        payload = json.loads(body) if body else {}

        if self.path == "/game/reset":
            WORLD.reset()
            self._send(200, {"message": "World reset"})
        elif self.path == "/game/set_state":
            success = WORLD.set_game_state(payload.get("state", ""))
            self._send(200 if success else 400, {"state": WORLD.state, "success": success})
        elif self.path == "/game/action/damage":
            res = WORLD.player_take_damage(payload.get("amount", 10))
            self._send(200, res)
        elif self.path == "/game/action/heal":
            res = WORLD.player_heal(payload.get("amount", 10))
            self._send(200, res)
        elif self.path == "/game/action/pickup_item":
            res = WORLD.add_item_to_inventory(payload.get("item", "Potion"))
            self._send(200, res)
        else:
            self._send(404, {"error": "Invalid action command"})

    def log_message(self, format, *args):
        # Silence console log spam during automated test runs
        return

def start_engine_server(port=9090):
    server = HTTPServer(("127.0.0.1", port), GameAutomationRPCHandler)
    server.serve_forever()

if __name__ == "__main__":
    print("🎮 Game Engine Automation RPC Server running on http://127.0.0.1:9090")
    start_engine_server()
