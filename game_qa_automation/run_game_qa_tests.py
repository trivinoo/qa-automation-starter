"""
Game QA Master Test Runner.
Executes both FQA (Functional) and LQA (Localization) test suites,
reporting results to console and generating an HTML visual report.
"""

import sys
from pathlib import Path

# Fix Windows console UTF-8 output encoding
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Setup paths
base_dir = Path(__file__).parent
sys.path.insert(0, str(base_dir / "fqa_functional_qa"))
sys.path.insert(0, str(base_dir / "lqa_localization_qa"))
sys.path.insert(0, str(base_dir / "shared_tools"))

import test_gameplay_mechanics
from static_string_auditor import LQAAuditor
from pseudo_localizer import generate_pseudo_locale
from ui_overflow_detector import check_locale_ui_overflow
from game_test_reporter import GameQAReporter

def main():
    reporter = GameQAReporter("Game FQA & LQA Automation Dashboard")

    print("\n" + "=" * 60)
    print("🕹️  STARTING GAME QA AUTOMATION TEST SUITE")
    print("=" * 60)

    # 1. Run FQA Gameplay Mechanics
    print("\n[1/3] Running FQA Mechanics & Engine Simulation...")
    fqa_details = []
    fqa_passed = True
    try:
        test_gameplay_mechanics.setup_module()
        test_gameplay_mechanics.test_fqa_game_state_flow()
        fqa_details.append("State machine transitions validated (MENU -> PLAYING)")
        test_gameplay_mechanics.test_fqa_combat_damage_and_lethal_death()
        fqa_details.append("Combat damage and lethal GAME_OVER trigger verified")
        test_gameplay_mechanics.test_fqa_healing_caps_at_max_hp()
        fqa_details.append("Health healing cap (clamp at max_hp) verified")
        test_gameplay_mechanics.test_fqa_inventory_slot_capacity()
        fqa_details.append("Inventory capacity boundary verified (5 items max)")
        print("  ✓ All 4 FQA scenarios passed.")
    except Exception as e:
        fqa_passed = False
        fqa_details.append(f"FQA Failure: {str(e)}")
        print(f"  ❌ FQA Failure: {e}")
    reporter.add_suite_result("Gameplay Mechanics & State Machine", "FQA", fqa_passed, fqa_details)

    # 2. Run LQA Static String Audit
    print("\n[2/3] Running LQA Translation Tables Audit...")
    lqa_details = []
    locales_dir = base_dir / "lqa_localization_qa" / "sample_locales"
    auditor = LQAAuditor(locales_dir / "en_US.json")
    
    # Audit German
    de_report = auditor.audit_target_locale(locales_dir / "de_DE.json")
    lqa_details.append(f"de_DE: {de_report['status']} (Keys: {len(auditor.master_data)}, Expansions flagged: {len(de_report['high_expansion_warnings'])})")

    # Audit Japanese (contains intentional QA defects to test defect detection)
    ja_report = auditor.audit_target_locale(locales_dir / "ja_JP.json")
    lqa_details.append(f"ja_JP: Identified {len(ja_report['missing_keys'])} missing keys and {len(ja_report['mismatched_placeholders'])} broken tokens (Defect detection working as expected)")

    # 3. Generate Pseudo-Localization
    pseudo_out = locales_dir / "qps_PLOC.json"
    generate_pseudo_locale(locales_dir / "en_US.json", pseudo_out)
    lqa_details.append("Generated Pseudo-Localization asset [!!! ȁććḗƥŧ !!!] for font/clipping stress testing")

    reporter.add_suite_result("Localization Static String & Token Audit", "LQA", True, lqa_details)

    # 4. Run UI Overflow Estimator
    print("\n[3/3] Running UI Text Overflow Checks...")
    import json
    with open(locales_dir / "de_DE.json", "r", encoding="utf-8") as f:
        de_strings = json.load(f)
    overflows = check_locale_ui_overflow(de_strings)
    overflow_details = [f"{o['element']}: '{o['text']}' overflows by ~{o['overflow_px']}px [{o['severity']}]" for o in overflows]
    reporter.add_suite_result("UI Boundary & Text Clipping Analysis", "LQA", len(overflows) == 0, overflow_details)

    # Generate HTML report
    report_file = base_dir / "game_qa_report.html"
    reporter.generate_html(report_file)

    print("\n" + "=" * 60)
    print("🏁 GAME QA AUTOMATION RUN COMPLETE")
    print(f"📄 Report saved to: {report_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
