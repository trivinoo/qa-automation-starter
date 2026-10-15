"""
Suite 4: Autonomous Playtesting Bot (Soak & Exploratory Bot).

In AAA studios, bots are deployed to:
1. Roam the game map autonomously.
2. Locate nearby enemies and engage in combat.
3. Advance simulation ticks and monitor for crashes or state deadlocks.
"""

import sys
import math
from pathlib import Path

lab_dir = Path(__file__).parent.parent
sys.path.insert(0, str(lab_dir / "automation_sdk"))
from driver import GameDriver

def run_autonomous_playtest_bot(driver: GameDriver, actions_limit: int = 15):
    """Bot 01: Autonomous agent navigating to and eliminating target."""
    driver.reset_scene()
    driver.set_game_state("PLAYING")

    print(f"🤖 Autonomous TestBot spawned in scene. Goal: Find and neutralize Goblin_Alpha...")
    
    actions_taken = 0
    target_defeated = False

    while actions_taken < actions_limit:
        actions_taken += 1
        player = driver.find_element_by_name("Player")
        goblin = driver.find_element_by_name("Goblin_Alpha")

        if not goblin:
            target_defeated = True
            break

        # Check Goblin health
        goblin_hp = goblin.get_component("HealthComponent")
        if not goblin_hp["is_alive"]:
            target_defeated = True
            break

        # Calculate vector to Goblin
        dx = goblin.position["x"] - player.position["x"]
        dy = goblin.position["y"] - player.position["y"]
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 2.0:
            # Move towards Goblin
            step_x = (dx / dist) * 1.0
            step_y = (dy / dist) * 1.0
            driver.move_object("Player", dx=step_x, dy=step_y)
        else:
            # Within attack range -> Execute strike!
            driver.attack(attacker="Player", target="Goblin_Alpha")

        # Advance engine simulation frames
        driver.advance_ticks(5)

    assert target_defeated is True, "Autonomous bot failed to defeat target within action budget"
    print(f"  ✓ Autonomous TestBot completed objective in {actions_taken} simulation actions!")

if __name__ == "__main__":
    driver = GameDriver()
    print("Running Autonomous Bot Playtesting Suite...")
    run_autonomous_playtest_bot(driver)
