import csv
import os

def update_vibhakti_rules():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'dictionaries', 'vibhakti_rules.csv')

    # Source: Page 10, Table B (Simple Vibhakti Examples) 
    # We map the 'Marker' to its behavior.
    rules = [
        # marker, meaning, type, behavior_logic
        ["ಗೆ", "to", "dative", "suffix"],
        ["ಅಲ್ಲಿ", "in", "locative", "agama_sandhi"],
        ["ಇಂದ", "from", "instrumental", "agama_sandhi"],
        ["ಅನ್ನು", "object", "accusative", "agama_sandhi"],
        ["ದ", "of", "genitive", "suffix"],
        ["ಕೆ", "to", "dative", "suffix"], # Variant of ge
        ["ಒಳಗೆ", "inside", "locative", "agama_sandhi"]
    ]

    headers = ["marker", "meaning", "type", "logic_type"]

    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rules)
    
    print(f"✅ Updated {file_path} with {len(rules)} case markers.")

if __name__ == "__main__":
    update_vibhakti_rules()