"""
Pseudo-Localization Generator for Game UI Stress Testing.

Why Pseudo-Localization is crucial in AAA & Indie Game Studios:
1. Accented/Diacritic character substitution verifies that game engine font sets
   support international Latin/extended glyphs without rendering squares (tofu '□').
2. String expansion (+30% to +50%) tests whether HUDs, dialogue balloons, and buttons
   clip or overflow BEFORE translating into German, French, or Russian.
3. Brackets '[...]' reveal hardcoded non-localized strings instantly during playthroughs.
"""

import json
import sys
from pathlib import Path
from typing import Dict

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Map standard characters to accented counterparts
ACCENT_MAP = {
    'a': 'ȃ', 'b': 'ƀ', 'c': 'ć', 'd': 'đ', 'e': 'ḗ', 'f': 'ƒ', 'g': 'ɠ',
    'h': 'ħ', 'i': 'ī', 'j': 'ĵ', 'k': 'ķ', 'l': 'ŀ', 'm': 'ɱ', 'n': 'ƞ',
    'o': 'ǿ', 'p': 'ƥ', 'q': 'ɋ', 'r': 'ř', 's': 'ş', 't': 'ŧ', 'u': 'ŭ',
    'v': 'ṽ', 'w': 'ŵ', 'x': 'ẋ', 'y': 'ẏ', 'z': 'ẑ',
    'A': 'Ȧ', 'B': 'Ɓ', 'C': 'Ć', 'D': 'Đ', 'E': 'Ḗ', 'F': 'Ƒ', 'G': 'Ɠ',
    'H': 'Ħ', 'I': 'Ī', 'J': 'Ĵ', 'K': 'Ķ', 'L': 'Ł', 'M': 'Ṁ', 'N': 'Ƞ',
    'O': 'Ǿ', 'P': 'Ƥ', 'Q': 'Ɋ', 'R': 'Ř', 'S': 'Ş', 'T': 'Ŧ', 'U': 'Ŭ',
    'V': 'Ṽ', 'W': 'Ŵ', 'X': 'Ẋ', 'Y': 'Ẏ', 'Z': 'Ẑ'
}

def pseudo_localize_string(text: str, expansion_factor: float = 0.35) -> str:
    """
    Transforms plain English text into pseudo-localized string:
    - Protects placeholders like {player_name}
    - Substitutes diacritics
    - Adds length expansion padding
    - Wraps with delimiters [!!! ... !!!]
    """
    result = []
    i = 0
    n = len(text)

    while i < n:
        # Preserve placeholders untouched: {variable}
        if text[i] == '{':
            end_idx = text.find('}', i)
            if end_idx != -1:
                result.append(text[i:end_idx + 1])
                i = end_idx + 1
                continue
        
        char = text[i]
        result.append(ACCENT_MAP.get(char, char))
        i += 1

    accented = "".join(result)
    
    # Calculate expansion padding
    pad_len = max(3, int(len(text) * expansion_factor))
    padding = "~" * pad_len

    return f"[!!! {accented} {padding} !!!]"

def generate_pseudo_locale(source_file: Path, output_file: Path):
    with open(source_file, "r", encoding="utf-8") as f:
        source_data: Dict[str, str] = json.load(f)

    pseudo_data: Dict[str, str] = {}
    for key, text in source_data.items():
        pseudo_data[key] = pseudo_localize_string(text)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(pseudo_data, f, indent=2, ensure_ascii=False)

    print(f"✨ Pseudo-localization file generated at: {output_file.name}")
    print(f"Sample output: {list(pseudo_data.values())[0]}")

if __name__ == "__main__":
    base = Path(__file__).parent / "sample_locales"
    source = base / "en_US.json"
    target = base / "qps_PLOC.json"
    generate_pseudo_locale(source, target)
