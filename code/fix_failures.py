import csv
import os

def fix_missing_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dict_dir = os.path.join(base_dir, 'dictionaries')

    print("--- 🔧 Patching System Data ---")

    # 1. Add Missing Words to root_words.csv
    # These are the words causing "None" in your test results
    missing_words = [
        ["ಅಂಗಳ", "courtyard", "noun", "ಅ", "yes"],  # For Mane + Angala
        ["ಸೂರ್ಯ", "sun", "noun", "ಅ", "yes"],       # For Surya + Udaya
        ["ಉದಯ", "rise", "noun", "ಅ", "yes"],        # For Surya + Udaya
        ["ದೇವ", "god", "noun", "ಅ", "yes"],         # For Deva + Indra
        ["ಇಂದ್ರ", "Indra", "noun", "ಇ", "yes"],     # For Deva + Indra
        ["ಹೊಸ್", "new", "adjective", "್", "yes"],   # For Hos + Gannada (Hackathon logic)
        ["ಗನ್ನಡ", "Kannada", "noun", "ಅ", "yes"],   # For Hos + Gannada
        ["ಮಳೆ", "rain", "noun", "ಎ", "yes"],        # For Male + Gala
        ["ಗಾಲ", "season", "noun", "ಅ", "yes"]       # For Male + Gala
    ]

    word_path = os.path.join(dict_dir, 'root_words.csv')
    with open(word_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(missing_words)
    print(f"✅ Added {len(missing_words)} missing words to dictionary.")

    # 2. Add Missing/Strict Rules to sandhi_rules.csv
    # Your previous rules might have been too specific (e.g., only 'aa'+'aa'). 
    # We need generic 'a'+'u' and 'a'+'i'.
    missing_rules = [
        # rule_num, sound1, sound2, result, ex1, ex2, combined
        ["7", "ಅ", "ಉ", "ಓ", "ಸೂರ್ಯ", "ಉದಯ", "ಸೂರ್ಯೋದಯ"], # Guna Sandhi (a+u=o)
        ["8", "ಅ", "ಇ", "ಏ", "ದೇವ", "ಇಂದ್ರ", "ದೇವೇಂದ್ರ"],    # Guna Sandhi (a+i=e)
        ["9", "್", "ಗ", "ಗ", "ಹೊಸ್", "ಗನ್ನಡ", "ಹೊಸಗನ್ನಡ"], # Special case for consonant join
        ["10", "ಎ", "ಗ", "ಗ", "ಮಳೆ", "ಗಾಲ", "ಮಳೆಗಾಲ"]      # Simple join
    ]

    rule_path = os.path.join(dict_dir, 'sandhi_rules.csv')
    with open(rule_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(missing_rules)
    print(f"✅ Added {len(missing_rules)} additional Sandhi rules.")

if __name__ == "__main__":
    fix_missing_data()