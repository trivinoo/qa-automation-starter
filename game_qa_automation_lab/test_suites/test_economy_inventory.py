"""
Suite 3: In-Game Economy & Inventory Boundaries.

Verifies:
1. Item pickup and storage.
2. Slot limit constraints (preventing inventory overflow).
3. Inventory full rejection flag.
"""

import sys
from pathlib import Path

lab_dir = Path(__file__).parent.parent
sys.path.insert(0, str(lab_dir / "automation_sdk"))
from driver import GameDriver

def test_inventory_capacity_and_overflow(driver: GameDriver):
    """Economy 01: Verify player can hold up to 4 items and 5th is rejected."""
    driver.reset_scene()
    driver.set_game_state("PLAYING")

    items = [
        ("pot_01", "Health Potion"),
        ("pot_02", "Mana Potion"),
        ("key_01", "Dungeon Key"),
        ("gem_01", "Ruby Gem")
    ]

    for item_id, name in items:
        res = driver.loot_item(item_id, name)
        assert res["success"] is True

    # Attempt to pick up 5th item (Player max_slots is 4)
    overflow = driver.loot_item("sword_02", "Excalibur")
    assert overflow["success"] is False
    assert overflow["full"] is True

    # Verify inventory state
    player = driver.find_element_by_name("Player")
    inv = player.get_component("InventoryComponent")
    assert inv["item_count"] == 4
    assert len(inv["items"]) == 4

if __name__ == "__main__":
    driver = GameDriver()
    print("Running Economy & Inventory Suite...")
    test_inventory_capacity_and_overflow(driver)
    print("  ✓ test_inventory_capacity_and_overflow passed")
    print("All Economy & Inventory tests passed!")
