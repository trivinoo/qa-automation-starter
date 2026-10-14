"""
FQA Automated Gameplay Mechanics Test Suite.

Simulates how modern automated game tests verify:
1. Game State Transitions (Finite State Machine validation)
2. Combat Damage Math & Death Condition triggering GAME_OVER
3. Healing Mechanics and Max HP clamping
4. Inventory system limits (Stack caps, Slot limits, Over-encumbrance)
"""

import urllib.request
import json
import threading
import time
from pathlib import Path
import sys

# Import local engine to run in-process for headless testing
from mock_game_engine import start_engine_server

BASE_URL = "http://127.0.0.1:9090"

def _rpc_post(endpoint: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def _rpc_get(endpoint: str) -> dict:
    req = urllib.request.Request(f"{BASE_URL}{endpoint}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def setup_module():
    """Starts the engine server in a background thread."""
    t = threading.Thread(target=start_engine_server, args=(9090,), daemon=True)
    t.start()
    time.sleep(0.5)

def test_fqa_game_state_flow():
    """FQA: Verify valid transitions between game states."""
    _rpc_post("/game/reset", {})
    state = _rpc_get("/game/state")
    assert state["engine_state"] == "MAIN_MENU", "Game should launch into MAIN_MENU"

    # Transition to PLAYING
    res = _rpc_post("/game/set_state", {"state": "PLAYING"})
    assert res["success"] is True
    assert res["state"] == "PLAYING"

def test_fqa_combat_damage_and_lethal_death():
    """FQA: Player receives damage and triggers GAME_OVER state upon reaching 0 HP."""
    _rpc_post("/game/reset", {})
    _rpc_post("/game/set_state", {"state": "PLAYING"})

    # Non-lethal damage
    dmg_res = _rpc_post("/game/action/damage", {"amount": 35})
    assert dmg_res["hp"] == 65
    assert dmg_res["state"] == "PLAYING"

    # Lethal damage
    lethal_res = _rpc_post("/game/action/damage", {"amount": 70})
    assert lethal_res["hp"] == 0
    assert lethal_res["state"] == "GAME_OVER", "0 HP must trigger GAME_OVER state"

def test_fqa_healing_caps_at_max_hp():
    """FQA: Healing cannot exceed player max health pool."""
    _rpc_post("/game/reset", {})
    _rpc_post("/game/set_state", {"state": "PLAYING"})
    _rpc_post("/game/action/damage", {"amount": 30}) # HP is 70

    heal_res = _rpc_post("/game/action/heal", {"amount": 100})
    assert heal_res["hp"] == 100, "Health must clamp at max_hp (100)"

def test_fqa_inventory_slot_capacity():
    """FQA: Enforces maximum carrying capacity (5 slots)."""
    _rpc_post("/game/reset", {})
    _rpc_post("/game/set_state", {"state": "PLAYING"})

    # Fill 5 slots
    for i in range(5):
        res = _rpc_post("/game/action/pickup_item", {"item": f"Item_{i}"})
        assert res["success"] is True

    # 6th item must be rejected
    overflow = _rpc_post("/game/action/pickup_item", {"item": "Overflow_Sword"})
    assert overflow["success"] is False
    assert overflow["reason"] == "INVENTORY_FULL"

if __name__ == "__main__":
    setup_module()
    print("🎮 Running FQA Automated Test Suite...")
    test_fqa_game_state_flow()
    print("  ✓ test_fqa_game_state_flow passed")
    test_fqa_combat_damage_and_lethal_death()
    print("  ✓ test_fqa_combat_damage_and_lethal_death passed")
    test_fqa_healing_caps_at_max_hp()
    print("  ✓ test_fqa_healing_caps_at_max_hp passed")
    test_fqa_inventory_slot_capacity()
    print("  ✓ test_fqa_inventory_slot_capacity passed")
    print("\n✅ All FQA game test scenarios passed successfully!")
