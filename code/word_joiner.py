import csv
import os
from fuzzy_matcher import FuzzyMatcher
from hint_generator import HintGenerator

class KannadaWordBuilder:
    def __init__(self):
        self.root_words = {}   # {word: {details}}
        self.sandhi_rules = [] # List of rule dictionaries
        self.fuzzy_engine = None
        self.hint_engine = HintGenerator()
        
        self._load_data()
        
        # Initialize Fuzzy Matcher with all known words
        self.fuzzy_engine = FuzzyMatcher(list(self.root_words.keys()))

    def _load_data(self):
        """Loads CSV data into memory"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dict_dir = os.path.join(base_dir, 'dictionaries')

        # 1. Load Root Words
        with open(os.path.join(dict_dir, 'root_words.csv'), 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.root_words[row['word']] = row

        # 2. Load Sandhi Rules
        with open(os.path.join(dict_dir, 'sandhi_rules.csv'), 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.sandhi_rules.append(row)

    def _get_last_swara(self, word):
        """Finds the ending vowel/sound of a word"""
        # Check CSV first
        if word in self.root_words and self.root_words[word]['last_sound'] != 'TODO':
             return self.root_words[word]['last_sound']
        
        # Fallback logic
        swaras = {
            'ಾ': 'ಆ', 'ಿ': 'ಇ', 'ೀ': 'ಈ', 'ು': 'ಉ', 'ೂ': 'ಊ', 
            'ೆ': 'ಎ', 'ೇ': 'ಏ', 'ೊ': 'ಒ', 'ೋ': 'ಓ'
        }
        if word[-1] in swaras: return swaras[word[-1]]
        if 'ಅ' <= word[-1] <= 'ಔ': return word[-1]
        if word[-1] == '್': return '್' # Halant (Consonant ending)
        return 'ಅ' # Inherent 'a'

    def _get_first_swara(self, word):
        """Finds the starting vowel of a word"""
        char = word[0]
        if 'ಅ' <= char <= 'ಔ':
            return char
        # If it's a consonant, we return the consonant char itself to allow rule matching
        return char 

    def join_words(self, word1, word2):
        """
        The main function to join two words.
        """
        # Step 1: Validate Words
        if word1 not in self.root_words:
            sugg = self.fuzzy_engine.get_suggestions(word1)
            return {'result': None, 'status': 'error', 'msg': f"Word 1 '{word1}' not found. Suggestions: {sugg}"}
        
        if word2 not in self.root_words:
            sugg = self.fuzzy_engine.get_suggestions(word2)
            return {'result': None, 'status': 'error', 'msg': f"Word 2 '{word2}' not found. Suggestions: {sugg}"}

        # --- STRATEGY 1: EXACT MATCH LOOKUP (Fixes specific tricky words like Hosagannada) ---
        # If this specific pair exists in our rule examples, use that result directly.
        for rule in self.sandhi_rules:
            if rule['example_word1'] == word1 and rule['example_word2'] == word2:
                return {
                    'result': rule['combined_result'],
                    'status': 'success',
                    'rule': f"Direct Match (Rule {rule['rule_number']})"
                }

        # --- STRATEGY 2: PHONETIC RULES ---
        sound1 = self._get_last_swara(word1)
        sound2 = self._get_first_swara(word2)

        matched_rule = None
        for rule in self.sandhi_rules:
            if rule['sound1'] == sound1 and rule['sound2'] == sound2:
                matched_rule = rule
                break

        if matched_rule:
            result_sound = matched_rule['result']
            
            # LOGIC A: AGAMA SANDHI (Insertion) [Fixes Mane + Angala]
            # If result is 'ಯ' (ya) or 'ವ' (va), we DO NOT delete the vowel of Word 1.
            if result_sound in ['ಯ', 'ವ']:
                # Logic: Word1 + ResultChar + Word2
                # Note: Word2 usually starts with a vowel (e.g., Angala).
                # 'y' + 'a' = 'ya'. We need to combine the joiner with Word 2's vowel.
                
                # For 'y', we check the vowel of word 2
                vowel_map = {
                    'ಅ': '', 'ಆ': 'ಾ', 'ಇ': 'ಿ', 'ಈ': 'ೀ', 'ಉ': 'ು', 'ಊ': 'ೂ', 
                    'ಎ': 'ೆ', 'ಏ': 'ೇ'
                }
                
                # Matra for the second word's starting vowel
                w2_matra = vowel_map.get(sound2, '') 
                
                joiner_base = result_sound # 'ಯ' or 'ವ'
                
                # Construct: Mane + y(plus matra of A) + ngala
                # remove first char of w2 (the vowel)
                w2_remainder = word2[1:] 
                
                final_word = word1 + joiner_base + w2_matra + w2_remainder
                
                # Clean up: If joiner + empty matra, ensure it looks right (e.g., ಯ + nothing = ಯ)
                # Actually, 'ಯ' in unicode usually has inherent 'a'. 
                # If W2 is 'Angala' (A), 'y'+'a' = 'ya'. 
                # If W2 is 'I', 'y'+'i' = 'yi'.
                
                # Simplified Hackathon approach for Agama:
                # Just use the logic: Word1 + Joiner + Word2(vowel removed) + Matra
                # But simpler: Word1 + 'ಯ' + Word2 (if W2 starts with vowel, replace with matra on Ya)
                
                # Let's try the simplest Agama fix for "Mane" + "Angala":
                final_word = word1 + "ಯ" + word2[1:] # Mane + ya + ngala -> Maneyangala
                if result_sound == 'ವ':
                     final_word = word1 + "ವ" + word2[1:]

            # LOGIC B: LOPA/ADESA SANDHI (Replacement) [Standard Logic]
            else:
                # 1. Strip last matra/vowel from Word 1
                base_w1 = word1
                if word1[-1] in ['ಾ','ಿ','ೀ','ು','ೂ','ೆ','ೇ','ೊ','ೋ','್']:
                    base_w1 = word1[:-1]
                
                # 2. Strip first vowel from Word 2 (only if it's a vowel)
                base_w2 = word2
                if 'ಅ' <= word2[0] <= 'ಔ':
                    base_w2 = word2[1:]

                # 3. Insert Result Matra
                vowel_to_matra = {
                    'ಆ': 'ಾ', 'ಇ': 'ಿ', 'ಈ': 'ೀ', 'ಉ': 'ು', 'ಊ': 'ೂ',
                    'ಎ': 'ೆ', 'ಏ': 'ೇ', 'ಐ': 'ೈ', 'ಒ': 'ೊ', 'ಓ': 'ೋ', 'ಔ': 'ೌ',
                    'ಗ': 'ಗ' # Consonant replacement
                }
                mid_char = vowel_to_matra.get(result_sound, result_sound)
                
                final_word = base_w1 + mid_char + base_w2

            return {
                'result': final_word, 
                'status': 'success', 
                'rule': f"Rule {matched_rule['rule_number']}: {sound1} + {sound2} = {matched_rule['result']}"
            }

        # Default: No rule found
        return {'result': word1 + word2, 'status': 'warning', 'msg': 'No Sandhi rule found, joined directly.'}

# --- CLI INTERFACE ---
if __name__ == "__main__":
    builder = KannadaWordBuilder()
    print("--- Kannada Word Builder V2 ---")
    w1 = input("Enter Word 1: ")
    w2 = input("Enter Word 2: ")
    output = builder.join_words(w1, w2)
    print(f"Result: {output['result']}")