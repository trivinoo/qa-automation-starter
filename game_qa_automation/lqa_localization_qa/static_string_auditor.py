"""
Static String & LQA Translation Auditor.

In game studios, this tool runs in the CI/CD pipeline before builds are cooked,
catching the most frequent LQA release blockers:
1. Missing translation keys (Untranslated / Ghost Strings)
2. Desynchronized interpolation placeholders (e.g., {xp_amount} present in EN but missing in JA)
3. Dangerous expansion ratios (Strings expanding > 150% that cause UI clipping)
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Any

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PLACEHOLDER_REGEX = re.compile(r'\{([a-zA-Z0-9_]+)\}')

class LQAAuditor:
    def __init__(self, master_file_path: Path):
        self.master_path = master_file_path
        self.master_data = self._load_json(master_file_path)

    @staticmethod
    def _load_json(path: Path) -> Dict[str, str]:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def extract_placeholders(text: str) -> Set[str]:
        return set(PLACEHOLDER_REGEX.findall(text))

    def audit_target_locale(self, target_file_path: Path) -> Dict[str, Any]:
        target_data = self._load_json(target_file_path)
        locale_name = target_file_path.stem

        missing_keys: List[str] = []
        extra_keys: List[str] = []
        mismatched_placeholders: List[Dict[str, Any]] = []
        high_expansion_warnings: List[Dict[str, Any]] = []

        # Check for missing keys and placeholder parity
        for key, master_text in self.master_data.items():
            if key not in target_data:
                missing_keys.append(key)
                continue

            target_text = target_data[key]

            # Placeholders / token verification
            master_tokens = self.extract_placeholders(master_text)
            target_tokens = self.extract_placeholders(target_text)
            if master_tokens != target_tokens:
                mismatched_placeholders.append({
                    "key": key,
                    "expected": sorted(list(master_tokens)),
                    "found": sorted(list(target_tokens))
                })

            # Text expansion ratio check (warning if > 80% expansion)
            if len(master_text) > 0:
                ratio = len(target_text) / len(master_text)
                if ratio >= 1.70:
                    high_expansion_warnings.append({
                        "key": key,
                        "ratio": round(ratio, 2),
                        "master_len": len(master_text),
                        "target_len": len(target_text),
                        "master": master_text,
                        "target": target_text
                    })

        # Check for extraneous keys in target not present in master
        for key in target_data:
            if key not in self.master_data:
                extra_keys.append(key)

        return {
            "locale": locale_name,
            "status": "FAIL" if (missing_keys or mismatched_placeholders) else "PASS",
            "missing_keys": missing_keys,
            "extra_keys": extra_keys,
            "mismatched_placeholders": mismatched_placeholders,
            "high_expansion_warnings": high_expansion_warnings
        }

def run_audit(locales_dir: Path):
    master_path = locales_dir / "en_US.json"
    if not master_path.exists():
        raise FileNotFoundError(f"Master file not found at {master_path}")

    auditor = LQAAuditor(master_path)
    print("=" * 65)
    print(f"🎮 LQA AUDITOR: Scanning translation tables against master (en_US)")
    print("=" * 65)

    all_passed = True
    for file in sorted(locales_dir.glob("*.json")):
        if file.name == "en_US.json":
            continue

        report = auditor.audit_target_locale(file)
        badge = "✅ PASS" if report["status"] == "PASS" else "❌ FAIL"
        print(f"\n[{badge}] Locale: {report['locale']}")

        if report["missing_keys"]:
            all_passed = False
            print(f"  🚨 Missing Keys ({len(report['missing_keys'])}):")
            for k in report["missing_keys"]:
                print(f"     - {k}")

        if report["mismatched_placeholders"]:
            all_passed = False
            print(f"  🚨 Broken Variables/Placeholders ({len(report['mismatched_placeholders'])}):")
            for item in report["mismatched_placeholders"]:
                print(f"     - Key: {item['key']} | Expected: {item['expected']} | Found: {item['found']}")

        if report["high_expansion_warnings"]:
            print(f"  ⚠️  High Text Expansion Risk (>170%):")
            for w in report["high_expansion_warnings"]:
                print(f"     - Key: {w['key']} (+{int((w['ratio']-1)*100)}% expansion)")

    print("\n" + "=" * 65)
    return all_passed

if __name__ == "__main__":
    current_dir = Path(__file__).parent
    locales_dir = current_dir / "sample_locales"
    success = run_audit(locales_dir)
    print(f"Final Audit Result: {'All valid' if success else 'Defects discovered in localized assets'}")
