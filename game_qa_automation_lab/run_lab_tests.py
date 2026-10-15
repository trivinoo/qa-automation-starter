"""
Master Runner for Game QA Automation Lab.

Spawns the in-memory Game Engine RPC server, executes all 4 test suites,
and prints a verified test execution report.
"""

import sys
import time
import threading
from pathlib import Path

# Setup paths
lab_dir = Path(__file__).parent
sys.path.insert(0, str(lab_dir / "mini_game_engine"))
sys.path.insert(0, str(lab_dir / "automation_sdk"))
sys.path.insert(0, str(lab_dir / "test_suites"))

# Handle UTF-8 encoding safely on Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from engine import run_server
from driver import GameDriver

# Import test suites
import test_smoke_bvt
import test_combat_and_physics
import test_economy_inventory
import test_autonomous_bot

def start_engine_background():
    t = threading.Thread(target=run_server, args=(9191,), daemon=True)
    t.start()
    time.sleep(0.6)  # Give server brief moment to bind

def main():
    print("=" * 65)
    print("🎮 GAME QA AUTOMATION LAB: RUNNING FULL TEST MATRIX")
    print("=" * 65)

    start_engine_background()
    driver = GameDriver(port=9191)

    # 1. Smoke / BVT
    print("\n[Suite 1/4] Smoke & Build Verification Tests (BVT)...")
    test_smoke_bvt.test_bvt_engine_initialization(driver)
    test_smoke_bvt.test_bvt_critical_objects_present(driver)
    test_smoke_bvt.test_bvt_player_baseline_stats(driver)
    print("  ✓ All 3 BVT tests passed.")

    # 2. Combat & Physics
    print("\n[Suite 2/4] Combat & Physics Mechanics...")
    test_combat_and_physics.test_combat_range_and_damage_execution(driver)
    test_combat_and_physics.test_player_navigation_and_movement(driver)
    print("  ✓ All Combat & Physics tests passed.")

    # 3. Economy & Inventory
    print("\n[Suite 3/4] Economy & Inventory Boundaries...")
    test_economy_inventory.test_inventory_capacity_and_overflow(driver)
    print("  ✓ Inventory boundary tests passed.")

    # 4. Autonomous Playtesting Bot
    print("\n[Suite 4/4] Autonomous Bot Playtesting (TestBot)...")
    test_autonomous_bot.run_autonomous_playtest_bot(driver)
    print("  ✓ Autonomous TestBot mission passed.")

    print("\n" + "=" * 65)
    print("🏆 ALL GAME AUTOMATION SUITES PASSED CLEANLY (100% SUCCESS)")
    print("=" * 65)

if __name__ == "__main__":
    main()
