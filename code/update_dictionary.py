import csv
import os
import shutil

# Kannada Unicode Mapping for Vowels (Swaras)
# This maps the "Vowel Sign" (Matra) to the actual Vowel Sound
SWARA_MAP = {
    '\u0cbe': 'ಆ',  # aa
    '\u0cbf': 'ಇ',  # i
    '\u0cc0': 'ಈ',  # ii
    '\u0cc1': 'ಉ',  # u
    '\u0cc2': 'ಊ',  # uu
    '\u0cc3': 'ಋ',  # ru
    '\u0cc4': 'ೠ',  # ruu
    '\u0cc6': 'ಎ',  # e
    '\u0cc7': 'ಏ',  # ee
    '\u0cc8': 'ಐ',  # ai
    '\u0cca': 'ಒ',  # o
    '\u0ccb': 'ಓ',  # oo
    '\u0ccc': 'ಔ',  # au
}

HALANT = '\u0ccd' # The symbol that removes the inherent 'a'

def get_kannada_last_sound(word):
    """
    Analyzes the last character of a Kannada word to find its ending sound.
    """
    if not word:
        return ""
    
    last_char = word[-1]
    
    # Case 1: Word ends with a Matra (Vowel Sign)
    if last_char in SWARA_MAP:
        return SWARA_MAP[last_char]
    
    # Case 2: Word ends with Halant (Virama)
    # This means it ends in a consonant sound (Vyanjana)
    if last_char == HALANT:
        # Return the consonant before the halant
        if len(word) > 1:
            return word[-2] # Returns the consonant itself
        return "consonant"

    # Case 3: Word ends in a base Consonant
    # In Kannada, a base consonant (like ಕ) implies an inherent 'ಅ' (a) sound.
    # Unless it is a standalone vowel (like ಅ, ಆ)
    if '\u0c80' <= last_char <= '\u0c94': # It's a standalone vowel
        return last_char
    else:
        return 'ಅ' # Inherent 'a' sound

def update_csv_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE_PATH = os.path.join(BASE_DIR, 'dictionaries', 'root_words.csv')
    TEMP_PATH = os.path.join(BASE_DIR, 'dictionaries', 'root_words_temp.csv')

    # Check if file exists
    if not os.path.exists(FILE_PATH):
        print("Error: root_words.csv not found.")
        return

    print("Processing dictionary...")
    
    updated_rows = []
    
    with open(FILE_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            word = row['word']
            
            # Update Last Sound if it is missing or "TODO"
            if row['last_sound'] == 'TODO' or not row['last_sound']:
                row['last_sound'] = get_kannada_last_sound(word)
                print(f"Computed last sound for: {word} -> {row['last_sound']}")
            
            updated_rows.append(row)

    # Write to a new temp file first (Safety)
    with open(TEMP_PATH, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    # Replace old file with new file
    shutil.move(TEMP_PATH, FILE_PATH)
    print("\n✅ root_words.csv successfully updated with sounds and meanings!")

if __name__ == "__main__":
    update_csv_data()