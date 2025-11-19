import csv
import os
from fuzzy_matcher import FuzzyMatcher
from hint_generator import HintGenerator

class KannadaWordBuilder:
    def __init__(self):
        self.root_words = {}   
        self.sandhi_rules = [] 
        self.vibhakti_markers = {} 
        self.samasa_rules = [] # NEW: Samasa Rules
        self.fuzzy_engine = None
        self.hint_engine = HintGenerator()
        
        self._load_data()
        
        if self.root_words:
            self.fuzzy_engine = FuzzyMatcher(list(self.root_words.keys()))

    def _load_data(self):
        """Loads all CSV databases"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dict_dir = os.path.join(base_dir, 'dictionaries')

        # 1. Load Root Words
        path_root = os.path.join(dict_dir, 'root_words.csv')
        if os.path.exists(path_root):
            with open(path_root, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.root_words[row['word']] = row

        # 2. Load Sandhi Rules
        path_rules = os.path.join(dict_dir, 'sandhi_rules.csv')
        if os.path.exists(path_rules):
            with open(path_rules, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.sandhi_rules.append(row)

        # 3. Load Vibhakti Rules
        path_vibhakti = os.path.join(dict_dir, 'vibhakti_rules.csv')
        if os.path.exists(path_vibhakti):
            with open(path_vibhakti, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.vibhakti_markers[row['marker']] = row
                    
        # 4. Load Samasa Rules (NEW)
        path_samasa = os.path.join(dict_dir, 'samasa_rules.csv')
        if os.path.exists(path_samasa):
            with open(path_samasa, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.samasa_rules.append(row)

    # --- SOUND HELPERS ---
    def _get_last_swara(self, word):
        if not word: return ''
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

    # --- SAMASA LOGIC (NEW) ---
    def _resolve_samasa(self, word1):
        """
        Checks if Word 1 has a case marker that needs dropping (Tatpurusha).
        Returns: (RootWord, RuleName) or (None, None)
        """
        for rule in self.samasa_rules:
            suffix = rule['suffix_to_drop']
            
            if word1.endswith(suffix):
                # Calculate potential root
                # e.g., Suryana (ends in 'na') -> Remove 'na' -> Surya + 'a' (replacement)
                # Logic: Strip suffix
                base = word1[:-len(suffix)]
                
                # If replacement is simple (like 'a'), we usually just check if the base is valid
                # Simplification: Just return the base if it exists in our dictionary
                candidate_root = base
                
                # Special handling for 'vina' -> 'u' (Maguvina -> Magu)
                if rule['replacement_sound'] == 'ಉ' and not base.endswith('ಉ'):
                     candidate_root = base + 'ು' # Add 'u' matra
                
                # Verify if this 'root' exists in our dictionary
                if candidate_root in self.root_words:
                    return candidate_root, rule['rule_name']
                
                # If exact root not found, try fuzzy or trust the rule for specific cases
                # For 'Suryana' -> 'Surya', the base 'Surya' is correct.
                return base, rule['rule_name']
                
        return None, None

    # --- VIBHAKTI LOGIC ---
    def _apply_vibhakti(self, word, marker):
        last_sound = self._get_last_swara(word)
        if marker == 'ಗೆ':
            if last_sound in ['ಉ', 'ಊ']: return word + "ವಿಗೆ"
            return word + "ಗೆ"
        if marker in ['ಅಲ್ಲಿ', 'ಇಂದ', 'ಅನ್ನು']:
            if last_sound == 'ಅ':
                if marker == 'ಅನ್ನು': return word + "ವನ್ನು"
                if marker == 'ಅಲ್ಲಿ': return word + "ದಲ್ಲಿ"
                return word + "ವ" + marker
            if last_sound in ['ಎ', 'ಏ', 'ಇ', 'ಈ']:
                if marker == 'ಅಲ್ಲಿ': return word + "ಯಲ್ಲಿ"
                if marker == 'ಇಂದ': return word + "ಯಿಂದ"
                if marker == 'ಅನ್ನು': return word + "ಯನ್ನು"
            if last_sound in ['ಉ', 'ಊ']:
                if marker == 'ಇಂದ': return word + "ವಿಂದ"
                if marker == 'ಅನ್ನು': return word + "ವನ್ನು"
                if marker == 'ಅಲ್ಲಿ': return word + "ವಿನಲ್ಲಿ"
        return word + marker

    # --- MAIN JOINER ---
    def join_words(self, word1, word2):
        processing_log = []
        
        # 1. VALIDATION
        if word1 not in self.root_words and self.fuzzy_engine:
            # In a real app, handle fuzzy logic here
            pass

        # 2. VIBHAKTI CHECK (Word 2 is a suffix)
        if word2 in self.vibhakti_markers:
            result = self._apply_vibhakti(word1, word2)
            return {'result': result, 'status': 'success', 'rule': f"Vibhakti: {word2}"}

        # 3. SAMASA CHECK (Pre-processing Word 1) [NEW STEP]
        # Does Word 1 look like 'Suryana' instead of 'Surya'?
        root_word1, samasa_rule = self._resolve_samasa(word1)
        
        final_word1 = word1
        if root_word1:
            final_word1 = root_word1
            processing_log.append(f"Samasa: Converted '{word1}' -> '{root_word1}' (Dropped case)")
        
        # 4. EXACT MATCH (Sandhi)
        for rule in self.sandhi_rules:
            if rule['example_word1'] == final_word1 and rule['example_word2'] == word2:
                msg = f"Direct Match (Rule {rule['rule_number']})"
                if processing_log: msg += f" + {processing_log[0]}"
                return {'result': rule['combined_result'], 'status': 'success', 'rule': msg}

        # 5. PHONETIC SANDHI
        sound1 = self._get_last_swara(final_word1)
        sound2 = self._get_first_swara(word2)
        matched_rule = None

        for rule in self.sandhi_rules:
            if rule['sound1'] == sound1 and rule['sound2'] == sound2:
                matched_rule = rule
                break

        if matched_rule:
            result_sound = matched_rule['result']
            
            # AGAMA
            if result_sound in ['ಯ', 'ವ']:
                w2_stub = word2[1:] if 'ಅ' <= word2[0] <= 'ಔ' else word2
                vowel_map = {'ಅ':'','ಆ':'ಾ','ಇ':'ಿ','ಈ':'ೀ','ಉ':'ು','ಊ':'ೂ','ಎ':'ೆ','ಏ':'ೇ'}
                matra = vowel_map.get(sound2, '')
                final_word = final_word1 + result_sound + matra + w2_stub
            
            # LOPA/GUNA/ADESA
            else:
                base_w1 = final_word1
                if final_word1[-1] in ['ಾ','ಿ','ೀ','ು','ೂ','ೆ','ೇ','ೊ','ೋ','್']:
                    base_w1 = final_word1[:-1]
                
                base_w2 = word2
                if 'ಅ' <= word2[0] <= 'ಔ':
                    base_w2 = word2[1:]
                
                vowel_to_matra = {
                    'ಆ': 'ಾ', 'ಇ': 'ಿ', 'ಈ': 'ೀ', 'ಉ': 'ು', 'ಊ': 'ೂ',
                    'ಎ': 'ೆ', 'ಏ': 'ೇ', 'ಐ': 'ೈ', 'ಒ': 'ೊ', 'ಓ': 'ೋ', 'ಔ': 'ೌ', 'ಗ': 'ಗ'
                }
                mid_char = vowel_to_matra.get(result_sound, result_sound)
                final_word = base_w1 + mid_char + base_w2

            rule_msg = f"Sandhi Rule: {sound1}+{sound2}={result_sound}"
            if processing_log: rule_msg = f"{processing_log[0]} -> {rule_msg}"
            
            return {'result': final_word, 'status': 'success', 'rule': rule_msg}

        # Fallback
        return {'result': word1 + word2, 'status': 'warning', 'msg': 'No Sandhi rule found, joined directly.'}

if __name__ == "__main__":
    builder = KannadaWordBuilder()
    print("--- Kannada Word Builder (Samasa + Sandhi + vibhakti pratyeya) ---")
    w1 = input("Word 1: ")
    w2 = input("Word 2: ")
    out = builder.join_words(w1, w2)
    print(f"Result: {out['result']}")
    print(f"Logic: {out.get('rule', 'Direct Join')}")