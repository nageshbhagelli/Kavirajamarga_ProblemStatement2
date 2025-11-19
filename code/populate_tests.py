import csv
import os

def populate_test_csv():
    # Path to the test file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'test cases', 'word_pairs_test.csv')

    # Headers required by PDF [cite: 148]
    headers = ["test_id", "word1", "word2", "expected_result", "sandhi_rule_used", "is_valid_compound"]

    # Examples from PDF [cite: 149-153, 218, 224]
    # We will duplicate these to simulate volume if needed, but here are the unique ones.
    test_data = [
        ["1", "ಮಹಾ", "ಆತ್ಮ", "ಮಹಾತ್ಮ", "rule_2", "yes"],      # Maha + Atma
        ["2", "ಮನೆ", "ಕೆಲಸ", "ಮನೆಕೆಲಸ", "no_sandhi", "yes"],  # Mane + Kelasa (No change)
        ["3", "ಪುಸ್ತಕ", "ಆಲಯ", "ಪುಸ್ತಕಾಲಯ", "rule_1", "yes"], # Pustaka + Alaya
        ["4", "ಗುರು", "ಉಪದೇಶ", "ಗುರೂಪದೇಶ", "rule_4", "yes"], # Guru + Upadesha
        ["5", "ರಾಮ", "ಆಲಯ", "ರಾಮಾಲಯ", "rule_1", "yes"],      # Rama + Alaya
        ["6", "ಮನೆ", "ಅಂಗಳ", "ಮನೆಯಂಗಳ", "rule_3", "yes"],     # Mane + Angala
        ["7", "ಸೂರ್ಯ", "ಉದಯ", "ಸೂರ್ಯೋದಯ", "rule_6", "yes"], # Surya + Udaya
        ["8", "ದೇವ", "ಇಂದ್ರ", "ದೇವೇಂದ್ರ", "rule_5", "yes"],   # Deva + Indra
        ["9", "ಹೊಸ್", "ಗನ್ನಡ", "ಹೊಸಗನ್ನಡ", "rule_x", "yes"],  # Example of other types
        ["10", "ಮಳೆ", "ಗಾಲ", "ಮಳೆಗಾಲ", "rule_x", "yes"], 
    ]

    # Write to CSV
    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(test_data)
    
    print(f"✅ Generated test file at: {file_path}")
    print(f"   Added {len(test_data)} baseline examples from the Problem Statement.")
    print("   ACTION: Open this CSV in Excel and add more rows to reach 500!")

if __name__ == "__main__":
    populate_test_csv()