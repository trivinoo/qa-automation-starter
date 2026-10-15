"""
Suite 1: Smoke & Build Verification Tests (BVT).

Runs in CI/CD on every build before deploying to QA testers:
- Validates engine initializes cleanly.
- Checks Player and critical boss/enemies spawn into the scene.
- Asserts baseline health and stats match design document specifications.
"""

import sys
from pathlib import Path

# Add SDK to path
lab_dir = Path(__file__).parent.parent
sys.path.insert(0, str(lab_dir / "automation_sdk"))

from driver import GameDriver

def test_bvt_engine_initialization(driver: GameDriver):
    """BVT 01: Verify game scene resets and transitions from MENU to PLAYING."""
    assert driver.reset_scene() is True
    assert driver.set_game_state("PLAYING") is True
    assert driver.get_game_state() == "PLAYING"

def test_bvt_critical_objects_present(driver: GameDriver):
    """BVT 02: Verify Player and Dragon Boss exist in the loaded scene."""
    player = driver.find_element_by_name("Player")
    assert player is not None, "Player entity missing from scene"
    assert player.tag == "Player"

    boss = driver.find_element_by_name("Dragon_Boss")
    assert boss is not None, "Dragon Boss entity missing from scene"
    assert boss.tag == "Boss"

def test_bvt_player_baseline_stats(driver: GameDriver):
    """BVT 03: Verify player initial health is 100/100 and weapon is equipped."""
    player = driver.find_element_by_name("Player")
    health = player.get_component("HealthComponent")
    assert health is not None
    assert health["current_hp"] == 100
    assert health["max_hp"] == 100
    assert health["is_alive"] is True

    weapon = player.get_component("WeaponComponent")
    assert weapon is not None
    assert weapon["name"] == "Steel Blade"
    assert weapon["damage"] == 30

if __name__ == "__main__":
    driver = GameDriver()
    print("Running Smoke / BVT Suite...")
    test_bvt_engine_initialization(driver)
    print("  ✓ test_bvt_engine_initialization passed")
    test_bvt_critical_objects_present(driver)
    print("  ✓ test_bvt_critical_objects_present passed")
    test_bvt_player_baseline_stats(driver)
    print("  ✓ test_bvt_player_baseline_stats passed")
    print("All BVT tests passed!")
