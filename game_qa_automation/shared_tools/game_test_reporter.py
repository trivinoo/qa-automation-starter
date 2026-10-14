"""
Game QA Automated HTML & Terminal Test Reporter.

Generates a unified test execution summary dashboard across:
- Functional Gameplay Tests (FQA)
- Localization Translation & Pseudo-Loc Audits (LQA)
- UI Clipping Risks
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class GameQAReporter:
    def __init__(self, title: str = "Game QA Automation Test Report"):
        self.title = title
        self.results: List[Dict[str, Any]] = []

    def add_suite_result(self, suite_name: str, domain: str, passed: bool, details: List[str]):
        self.results.append({
            "suite_name": suite_name,
            "domain": domain,  # 'FQA' or 'LQA'
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def generate_html(self, output_path: Path):
        cards_html = ""
        for r in self.results:
            status_badge = '<span style="background: #22c55e; color: white; padding: 4px 8px; border-radius: 4px;">PASSED</span>' if r["passed"] else '<span style="background: #ef4444; color: white; padding: 4px 8px; border-radius: 4px;">FAILED</span>'
            domain_badge = f'<span style="background: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{r["domain"]}</span>'
            items = "".join(f"<li>{d}</li>" for d in r["details"])
            
            cards_html += f"""
            <div style="background: #1e293b; padding: 16px; margin-bottom: 16px; border-radius: 8px; border-left: 4px solid {'#22c55e' if r['passed'] else '#ef4444'};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3>{domain_badge} &nbsp; {r['suite_name']}</h3>
                    <div>{status_badge}</div>
                </div>
                <ul style="color: #cbd5e1; font-family: monospace; font-size: 0.95rem;">{items}</ul>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{self.title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; max-width: 900px; margin: auto; }}
        h1 {{ color: #38bdf8; border-bottom: 1px solid #334155; padding-bottom: 10px; }}
    </style>
</head>
<body>
    <h1>🎮 {self.title}</h1>
    <p>Automated test session run on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    {cards_html}
</body>
</html>"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"📊 Visual HTML Game QA Report written to: {output_path.name}")
