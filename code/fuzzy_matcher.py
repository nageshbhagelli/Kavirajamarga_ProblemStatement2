from fuzzywuzzy import process # [cite: 86]

class FuzzyMatcher:
    def __init__(self, word_list):
        """
        Initialize with a list of valid dictionary words.
        """
        self.word_list = word_list

    def get_suggestions(self, user_input, limit=3): # [cite: 92]
        """
        Returns top 3 closest matches for a typo.
        Returns: List of tuples [('word', score), ...]
        """
        if not user_input:
            return []
            
        # Extract top matches using Levenshtein distance
        matches = process.extract(user_input, self.word_list, limit=limit)
        
        # Filter for decent matches (>70% similarity) to avoid garbage suggestions
        valid_matches = [m for m in matches if m[1] > 70]
        return valid_matches