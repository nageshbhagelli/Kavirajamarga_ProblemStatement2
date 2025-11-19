import csv
import os

def create_samasa_rules():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'dictionaries', 'samasa_rules.csv')

    # Rules for Tatpurusha Samasa (dropping case markers)
    # logic: If word1 ends with 'suffix', replace it with 'replacement' (root ending)
    rules = [
        # rule_name, suffix_to_drop, replacement_sound, example_input, example_root
        ["Tatpurusha_Genitive", "ನ", "ಅ", "ಸೂರ್ಯನ", "ಸೂರ್ಯ"], # Suryana -> Surya
        ["Tatpurusha_Genitive", "ವಿನ", "ಉ", "ಮಗುವಿನ", "ಮಗು"],   # Maguvina -> Magu
        ["Tatpurusha_Genitive", "ಯ", "ಇ", "ನದಿಯ", "ನದಿ"],     # Nadiya -> Nadi
        ["Tatpurusha_Dative", "ಗೆ", "ಅ", "ಮನೆಗೆ", "ಮನೆ"],       # Manege -> Mane
        ["Dwigu_Number", "ಮೂ", "ಮೂ", "ಮೂ", "ಮೂ"],            # Muu (Three) -> Muu
        ["Dwigu_Number", "ಇರ್", "ಇರ್", "ಇರ್", "ಇರ್"],         # Ir (Two) -> Ir
    ]

    headers = ["rule_name", "suffix_to_drop", "replacement_sound", "example_input", "example_root"]

    with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rules)
    
    print(f"✅ Created {file_path} with Samasa logic.")

if __name__ == "__main__":
    create_samasa_rules()