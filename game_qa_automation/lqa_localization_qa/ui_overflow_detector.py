"""
LQA UI Text Overflow & Clipping Estimator.

In video games, localized text is rendered into fixed pixel-dimension UI elements
(Buttons, Dialog boxes, HUD banners, Quest logs).
This tool models UI container bounds and flags strings that exceed available space
in target languages (e.g., German, Russian, French).
"""

from typing import Dict, List, Tuple

# Approximate pixel widths per character at default 16px game UI font
AVG_CHAR_PX = 9.2

# Predefined Game UI element constraints
UI_ELEMENT_CONSTRAINTS: Dict[str, Dict[str, int]] = {
    "ui.menu.start": {"max_width_px": 120, "max_lines": 1, "description": "Main Menu Start Button"},
    "ui.menu.options": {"max_width_px": 120, "max_lines": 1, "description": "Main Menu Settings Button"},
    "ui.menu.quit": {"max_width_px": 140, "max_lines": 1, "description": "Main Menu Quit Button"},
    "ui.button.confirm": {"max_width_px": 90, "max_lines": 1, "description": "Modal Dialog Confirm Button"},
    "ui.button.cancel": {"max_width_px": 90, "max_lines": 1, "description": "Modal Dialog Cancel Button"},
}

def estimate_string_pixel_width(text: str) -> int:
    return int(len(text) * AVG_CHAR_PX)

def check_locale_ui_overflow(locale_strings: Dict[str, str]) -> List[Dict[str, any]]:
    clipping_defects = []
    
    for key, constraint in UI_ELEMENT_CONSTRAINTS.items():
        if key in locale_strings:
            text = locale_strings[key]
            estimated_width = estimate_string_pixel_width(text)
            max_width = constraint["max_width_px"]
            
            if estimated_width > max_width:
                overflow_px = estimated_width - max_width
                clipping_defects.append({
                    "key": key,
                    "text": text,
                    "element": constraint["description"],
                    "estimated_width_px": estimated_width,
                    "max_allowed_px": max_width,
                    "overflow_px": overflow_px,
                    "severity": "CRITICAL" if overflow_px > 30 else "WARNING"
                })
                
    return clipping_defects

if __name__ == "__main__":
    german_sample = {
        "ui.menu.start": "Spiel starten",
        "ui.menu.quit": "Zum Desktop beenden", # 19 chars -> ~174px (Limit: 140px)
        "ui.button.confirm": "Bestätigen"      # 10 chars -> ~92px (Limit: 90px)
    }
    
    print("🔍 Testing LQA UI Overflow Estimator on German strings...")
    defects = check_locale_ui_overflow(german_sample)
    for d in defects:
        print(f"[{d['severity']}] {d['element']}: '{d['text']}' overflows by ~{d['overflow_px']}px")
