import csv
import os

def update_vibhakti_rules():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'dictionaries', 'vibhakti_rules.csv')

    # Extended Rule Set based on your test failures
    rules = [
        # [cite_start]Basic Case Markers [cite: 47, 48, 51]
        ["ಗೆ", "to", "dative", "suffix"],
        ["ಅಲ್ಲಿ", "in", "locative", "agama_sandhi"],
        ["ಇಂದ", "from", "instrumental", "agama_sandhi"],
        ["ಅನ್ನು", "object", "accusative", "agama_sandhi"],
        ["ದ", "of", "genitive", "suffix"],
        ["ಕೆ", "to", "dative", "suffix"], 
        ["ಒಳಗೆ", "inside", "locative", "agama_sandhi"], # Fix for Mane + olage
        
        # Plural Suffixes (galu)
        ["ಗಳು", "plural", "nominative", "simple_append"],
        ["ಗಳಲ್ಲಿ", "in (plural)", "locative", "simple_append"],
        ["ಗಳಿಂದ", "from (plural)", "instrumental", "simple_append"],
        ["ಗಳಿಗೆ", "to (plural)", "dative", "simple_append"],
        
        # Special/Compound Markers
        ["ಜೊತೆ", "with", "associative", "requires_genitive"], # Fix for Mane + jote
        ["ಏ", "emphasis", "particle", "agama_sandhi"],       # Fix for Rama + ee
        ["ಓ", "doubt", "particle", "agama_sandhi"]           # Fix for Mani + oo
    ]

    headers = ["marker", "meaning", "type", "logic_type"]

    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rules)
    
    print(f"✅ Updated {file_path} with {len(rules)} extended markers.")

if __name__ == "__main__":
    update_vibhakti_rules()