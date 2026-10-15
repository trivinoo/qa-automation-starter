"""
Suite 2: Combat & Physics Distance Mechanics.

Verifies:
1. Melee attack fails when player is OUT_OF_RANGE.
2. Player navigation/movement closes distance.
3. In-range attacks connect and reduce enemy health.
4. Consecutive attacks kill the enemy (is_alive transitions to False).
"""

import sys
from pathlib import Path

lab_dir = Path(__file__).parent.parent
sys.path.insert(0, str(lab_dir / "automation_sdk"))
from driver import GameDriver

def test_combat_range_and_damage_execution(driver: GameDriver):
    """Combat 01: Verify distance check, damage application, and death."""
    driver.reset_scene()
    driver.set_game_state("PLAYING")

    # Dragon Boss is at (10.0, 5.0), Player is at (0, 0)
    # Weapon range is 2.5 units -> Attack MUST fail due to distance
    out_of_range_res = driver.attack(attacker="Player", target="Dragon_Boss")
    assert out_of_range_res["success"] is False
    assert out_of_range_res["reason"] == "OUT_OF_RANGE"

    # Goblin is at (2.0, 0.0), Player is at (0, 0) -> Distance is 2.0 (Range is 2.5) -> In Range!
    hit1 = driver.attack(attacker="Player", target="Goblin_Alpha")
    assert hit1["success"] is True
    assert hit1["damage_dealt"] == 30
    assert hit1["target_current_hp"] == 20
    assert hit1["target_alive"] is True

    # Attack again to deliver lethal blow (Goblin HP 20 - 30 = 0)
    hit2 = driver.attack(attacker="Player", target="Goblin_Alpha")
    assert hit2["success"] is True
    assert hit2["target_current_hp"] == 0
    assert hit2["target_alive"] is False

def test_player_navigation_and_movement(driver: GameDriver):
    """Physics 01: Verify player coordinate translations."""
    driver.reset_scene()
    pos_before = driver.find_element_by_name("Player").position
    assert pos_before["x"] == 0.0

    # Move player forward 3.5 units along X
    new_pos = driver.move_object("Player", dx=3.5, dy=1.2)
    assert new_pos["x"] == 3.5
    assert new_pos["y"] == 1.2

if __name__ == "__main__":
    driver = GameDriver()
    print("Running Combat & Physics Mechanics Suite...")
    test_combat_range_and_damage_execution(driver)
    print("  ✓ test_combat_range_and_damage_execution passed")
    test_player_navigation_and_movement(driver)
    print("  ✓ test_player_navigation_and_movement passed")
    print("All Combat & Physics tests passed!")
