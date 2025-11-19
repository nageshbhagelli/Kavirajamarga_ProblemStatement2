import csv
import os

# Define file paths (relative to the code folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_DIR = os.path.join(BASE_DIR, 'dictionaries')

def populate_sandhi_rules():
    """Populates sandhi_rules.csv with rules from Problem Statement (Source: Page 2, 10)"""
    filepath = os.path.join(DICT_DIR, 'sandhi_rules.csv')
    
    # Data extracted from PDF Source [37, 40-43, 224]
    rules = [
        # rule_num, sound1, sound2, result, example1, example2, combined
        ["1", "ಅ", "ಆ", "ಆ", "ರಾಮ", "ಆಲಯ", "ರಾಮಾಲಯ"],      # Savarna Deergha (a+a=aa)
        ["2", "ಆ", "ಆ", "ಆ", "ಮಹಾ", "ಆತ್ಮ", "ಮಹಾತ್ಮ"],      # Savarna Deergha (aa+aa=aa)
        ["3", "ಎ", "ಅ", "ಯ", "ಮನೆ", "ಅಂಗಳ", "ಮನೆಯಂಗಳ"],    # Agama Sandhi (e+a=ya)
        ["4", "ಉ", "ಉ", "ಊ", "ಗುರು", "ಉಪದೇಶ", "ಗುರೂಪದೇಶ"], # Savarna Deergha (u+u=uu)
        ["5", "ಅ", "ಇ", "ಏ", "ದೇವ", "ಇಂದ್ರ", "ದೇವೇಂದ್ರ"],     # Guna Sandhi
        ["6", "ಆ", "ಉ", "ಓ", "ಸೂರ್ಯ", "ಉದಯ", "ಸೂರ್ಯೋದಯ"],  # Guna Sandhi
    ]

    with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(rules)
    print(f"✅ Added {len(rules)} Sandhi rules to {filepath}")

def populate_vibhakti_rules():
    """Populates vibhakti_rules.csv with case markers (Source: Page 2-3, 47-48)"""
    filepath = os.path.join(DICT_DIR, 'vibhakti_rules.csv')
    
    # Data from PDF Source [47, 48, 51-55]
    markers = [
        # marker, meaning, example, how_to_add, result
        ["ಗೆ", "to", "ಮನೆ", "add_ge", "ಮನೆಗೆ"],
        ["ಅಲ್ಲಿ", "in", "ಮನೆ", "add_y_then_alli", "ಮನೆಯಲ್ಲಿ"],
        ["ಇಂದ", "from", "ಮನೆ", "add_y_then_inda", "ಮನೆಯಿಂದ"],
        ["ಅನ್ನು", "object", "ಪುಸ್ತಕ", "add_v_then_annu", "ಪುಸ್ತಕವನ್ನು"],
        ["ದ", "possessive", "ಮರ", "add_da", "ಮರದ"] # Extra common one
    ]

    with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(markers)
    print(f"✅ Added {len(markers)} Vibhakti rules to {filepath}")

def populate_root_words():
    """Populates root_words.csv with the initial examples (Source: Page 1-2, 28-33)"""
    filepath = os.path.join(DICT_DIR, 'root_words.csv')
    
    # Data from PDF Source [28-33]
    words = [
        # word, meaning, type, last_sound, can_combine
        ["ಮಹಾ", "great", "prefix", "ಆ", "yes"],
        ["ಮನೆ", "house", "noun", "ಎ", "yes"],
        ["ಪುಸ್ತಕ", "book", "noun", "ಅ", "yes"],
        ["ಆತ್ಮ", "soul", "noun", "ಅ", "yes"],
        ["ರಾಜ", "king", "noun", "ಅ", "yes"],
        ["ರಾಮ", "Rama", "noun", "ಅ", "yes"],
        ["ಆಲಯ", "place", "noun", "ಅ", "yes"],
        ["ಗುರು", "teacher", "noun", "ಉ", "yes"],
        ["ಉಪದೇಶ", "advice", "noun", "ಅ", "yes"]
    ]

    with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(words)
    print(f"✅ Added {len(words)} root words to {filepath}")

if __name__ == "__main__":
    print("--- Populating Baseline Data from PDF ---")
    populate_sandhi_rules()
    populate_vibhakti_rules()
    populate_root_words()
    print("-----------------------------------------")