import csv
import os

class HintGenerator:
    def __init__(self):
        self.compound_db = {} # Stores {word1: [list of possible word2]}
        self._load_compounds()

    def _load_compounds(self):
        # Construct path to dictionaries/compound_words.csv
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, 'dictionaries', 'compound_words.csv')
        
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    w1 = row['word1']
                    w2 = row['word2']
                    combined = row['combined']
                    
                    if w1 not in self.compound_db:
                        self.compound_db[w1] = []
                    
                    # Store valid pairs [cite: 106]
                    self.compound_db[w1].append({
                        'next_word': w2,
                        'result': combined
                    })

    def get_hints(self, first_word):
        """
        Returns specific compound suggestions for a given first word.
        """
        return self.compound_db.get(first_word, [])