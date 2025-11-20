import csv
import os
from fuzzy_matcher import FuzzyMatcher
from hint_generator import HintGenerator

class KannadaWordBuilder:
    def __init__(self):
        self.root_words = {}   
        self.sandhi_rules = [] 
        self.vibhakti_markers = {} 
        self.samasa_rules = []
        self.fuzzy_engine = None
        self.hint_engine = HintGenerator()
        
        self._load_data()
        
        if self.root_words:
            self.fuzzy_engine = FuzzyMatcher(list(self.root_words.keys()))

    def _load_data(self):
        """Loads CSV data into memory"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dict_dir = os.path.join(base_dir, 'dictionaries')

        # Load all CSVs (Root, Sandhi, Vibhakti, Samasa)
        # [Same loading logic as before - abbreviated for clarity]
        files = {
            'root_words.csv': self.root_words,
            'sandhi_rules.csv': self.sandhi_rules,
            'vibhakti_rules.csv': self.vibhakti_markers,
            'samasa_rules.csv': self.samasa_rules
        }
        
        for filename, target in files.items():
            path = os.path.join(dict_dir, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if isinstance(target, dict):
                            key = 'word' if 'word' in row else 'marker'
                            target[row[key]] = row
                        else:
                            target.append(row)

    # --- SOUND HELPERS ---
    def _get_last_swara(self, word):
        if not word: return ''
        # Check CSV first
        if word in self.root_words and self.root_words[word].get('last_sound', 'TODO') not in ['TODO', '']:
             return self.root_words[word]['last_sound']
        
        swaras = {'ಾ': 'ಆ', 'ಿ': 'ಇ', 'ೀ': 'ಈ', 'ು': 'ಉ', 'ೂ': 'ಊ', 'ೆ': 'ಎ', 'ೇ': 'ಏ', 'ೊ': 'ಒ', 'ೋ': 'ಓ'}
        if word[-1] in swaras: return swaras[word[-1]]
        if 'ಅ' <= word[-1] <= 'ಔ': return word[-1]
        if word[-1] == '್': return '್'
        return 'ಅ'

    def _get_first_swara(self, word):
        if not word: return ''
        char = word[0]
        if 'ಅ' <= char <= 'ಔ': return char
        return char

    # --- SAMASA LOGIC ---
    def _resolve_samasa(self, word1):
        for rule in self.samasa_rules:
            suffix = rule['suffix_to_drop']
            if word1.endswith(suffix):
                base = word1[:-len(suffix)]
                candidate_root = base
                if rule['replacement_sound'] == 'ಉ' and not base.endswith('ಉ'):
                     candidate_root = base + 'ು'
                return candidate_root, rule['rule_name']
        return None, None

    # --- VIBHAKTI LOGIC (FIXED) ---
    def _apply_vibhakti(self, word, marker):
        last_sound = self._get_last_swara(word)
        
        # GROUP 0: Plurals (start with 'ga') - DIRECT APPEND
        # Fixes: Mane + galige -> Manegalige
        if marker.startswith("ಗ") and marker != "ಗೆ": 
            return word + marker

        # GROUP 1: Dative 'ge' (ಗೆ)
        if marker == 'ಗೆ':
            # Rule: 'u' ending -> 'vige' (Magu -> Maguvige)
            if last_sound in ['ಉ', 'ಊ']: return word + "ವಿಗೆ"
            # Rule: 'a' ending (Neuter) -> 'kke' (Sthala -> Sthalakke)
            # Note: We assume 'a' ending nouns here are mostly neuter for this logic
            if last_sound == 'ಅ': return word + "ಕ್ಕೆ" 
            # Rule: 'i', 'e' -> 'ge' (Mane -> Manege)
            return word + "ಗೆ"

        # GROUP 2: Genitive 'da' (ದ)
        # Fixes: Mane + da -> Maneya, Kashi + da -> Kashiya
        if marker == 'ದ':
            if last_sound in ['ಇ', 'ಈ', 'ಎ', 'ಏ']: return word + "ಯ"
            if last_sound in ['ಉ', 'ಊ']: return word + "ವಿನ"
            if last_sound == 'ಅ': return word + "ದ" # Pustaka -> Pustakada
            return word + "ದ"

        # GROUP 3: Associative 'jote' (ಜೊತೆ)
        # Fixes: Mane + jote -> Maneya jote (Requires Genitive first)
        if marker == 'ಜೊತೆ':
            # Recursively apply 'da' (Genitive) logic first, then add ' jote'
            genitive_form = self._apply_vibhakti(word, 'ದ')
            return genitive_form + " ಜೊತೆ"

        # GROUP 4: Agama (alli, inda, annu, olage, particle 'ee'/'oo')
        # Markers that start with vowels usually trigger Agama
        agama_markers = ['ಅಲ್ಲಿ', 'ಇಂದ', 'ಅನ್ನು', 'ಒಳಗೆ', 'ಏ', 'ಓ']
        if marker in agama_markers:
            
            # SUB-RULE: 'u' ending special case for 'inda'/'alli'
            # Fixes: Magu + inda -> Maguvininda (adds 'in')
            if last_sound in ['ಉ', 'ಊ']:
                if marker == 'ಇಂದ': return word + "ವಿನಿಂದ"
                if marker == 'ಅಲ್ಲಿ': return word + "ವಿನಲ್ಲಿ"
                if marker == 'ಅನ್ನು': return word + "ವನ್ನು" # Maguvannu
                if marker == 'ಒಳಗೆ': return word + "ವೊಳಗೆ"

            # SUB-RULE: 'a' ending special case (d-agama for neuter)
            # Fixes: Sthala + alli -> Sthaladalli
            if last_sound == 'ಅ':
                if marker == 'ಅಲ್ಲಿ': return word + "ದಲ್ಲಿ"
                if marker == 'ಇಂದ': return word + "ದಿಂದ"
                if marker == 'ಒಳಗೆ': return word + "ದೊಳಗೆ"
                if marker == 'ಅನ್ನು': return word + "ವನ್ನು"
                # For particles like 'ee', use 'n' (Rama -> Ramane)
                if marker == 'ಏ': return word + "ನೇ"
                if marker == 'ಓ': return word + "ನೋ"

            # SUB-RULE: 'i', 'e' ending (y-agama)
            # Fixes: Mane + olage -> Maneyolage
            if last_sound in ['ಇ', 'ಈ', 'ಎ', 'ಏ']:
                # Map vowel start to Matra
                # a->ya, i->yi, u->yu, e->ye, o->yo
                y_joiner = "ಯ"
                
                # Map marker first char to matra
                marker_map = {
                    'ಅ': '', 'ಆ': 'ಾ', 'ಇ': 'ಿ', 'ಈ': 'ೀ', 'ಉ': 'ು', 'ಊ': 'ೂ',
                    'ಎ': 'ೆ', 'ಏ': 'ೇ', 'ಒ': 'ೊ', 'ಓ': 'ೋ'
                }
                matra = marker_map.get(marker[0], '')
                marker_stub = marker[1:] # remove first vowel char
                
                return word + y_joiner + matra + marker_stub

        # Default Fallback
        return word + marker

    # --- MAIN JOINER ---
    def join_words(self, word1, word2):
        # 1. CHECK: Is Word 2 a Case Marker?
        # Check explicit list OR generic ending (like 'galu')
        if word2 in self.vibhakti_markers or word2.startswith("ಗಳ"):
            result = self._apply_vibhakti(word1, word2)
            return {'result': result, 'status': 'success', 'rule': f"Vibhakti: {word2}"}

        # 2. SAMASA CHECK
        root_word1, samasa_rule = self._resolve_samasa(word1)
        final_word1 = root_word1 if root_word1 else word1
        
        # 3. EXACT MATCH
        for rule in self.sandhi_rules:
            if rule['example_word1'] == final_word1 and rule['example_word2'] == word2:
                return {'result': rule['combined_result'], 'status': 'success', 'rule': f"Direct Match (Rule {rule['rule_number']})"}

        # 4. PHONETIC SANDHI
        sound1 = self._get_last_swara(final_word1)
        sound2 = self._get_first_swara(word2)
        matched_rule = None

        for rule in self.sandhi_rules:
            if rule['sound1'] == sound1 and rule['sound2'] == sound2:
                matched_rule = rule
                break

        if matched_rule:
            result_sound = matched_rule['result']
            # Agama
            if result_sound in ['ಯ', 'ವ']:
                w2_stub = word2[1:] if 'ಅ' <= word2[0] <= 'ಔ' else word2
                vowel_map = {'ಅ':'','ಆ':'ಾ','ಇ':'ಿ','ಈ':'ೀ','ಉ':'ು','ಊ':'ೂ','ಎ':'ೆ','ಏ':'ೇ'}
                matra = vowel_map.get(sound2, '')
                final_word = final_word1 + result_sound + matra + w2_stub
            # Lopa/Guna
            else:
                base_w1 = final_word1
                if final_word1[-1] in ['ಾ','ಿ','ೀ','ು','ೂ','ೆ','ೇ','ೊ','ೋ','್']:
                    base_w1 = final_word1[:-1]
                base_w2 = word2
                if 'ಅ' <= word2[0] <= 'ಔ': base_w2 = word2[1:]
                vowel_to_matra = {
                    'ಆ': 'ಾ', 'ಇ': 'ಿ', 'ಈ': 'ೀ', 'ಉ': 'ು', 'ಊ': 'ೂ', 'ಎ': 'ೆ', 'ಏ': 'ೇ', 'ಐ': 'ೈ', 'ಒ': 'ೊ', 'ಓ': 'ೋ', 'ಔ': 'ೌ', 'ಗ': 'ಗ'
                }
                mid_char = vowel_to_matra.get(result_sound, result_sound)
                final_word = base_w1 + mid_char + base_w2

            return {'result': final_word, 'status': 'success', 'rule': f"Sandhi Rule: {sound1}+{sound2}={result_sound}"}

        return {'result': word1 + word2, 'status': 'warning', 'msg': 'No Sandhi rule found'}

if __name__ == "__main__":
    builder = KannadaWordBuilder()
    print("--- Kannada Word Builder (Final v3) ---")
    w1 = input("Word 1: ")
    w2 = input("Word 2: ")
    out = builder.join_words(w1, w2)
    print(f"Result: {out['result']}")