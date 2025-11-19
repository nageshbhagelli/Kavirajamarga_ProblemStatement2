import csv
import os
import random
from word_joiner import KannadaWordBuilder # Uses your logic

def generate_massive_data():
    print("--- 🏭 Generating Compounds & Test Cases ---")
    
    # 1. Initialize
    builder = KannadaWordBuilder()
    root_words = list(builder.root_words.keys())
    
    if len(root_words) < 100:
        print("❌ Error: Not enough root words. Run 'bulk_scrape_wiki.py' first!")
        return

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    comp_path = os.path.join(base_dir, 'dictionaries', 'compound_words.csv')
    test_path = os.path.join(base_dir, 'test cases', 'word_pairs_test.csv')

    generated_compounds = []
    generated_tests = []
    
    # 2. Generation Loop
    # We need 2500 compounds [cite: 134] and 500 tests [cite: 139]
    target_compounds = 2600 
    attempts = 0
    
    print(f"   Mining matches from {len(root_words)} words...")

    while len(generated_compounds) < target_compounds:
        attempts += 1
        
        # Pick 2 random words
        w1 = random.choice(root_words)
        w2 = random.choice(root_words)
        
        # Try to join them
        output = builder.join_words(w1, w2)
        
        # We only want "Interesting" joins (where a rule was applied)
        # output['rule'] usually contains "Rule X" or "Direct Match"
        if output['status'] == 'success' and 'Rule' in output.get('rule', ''):
            
            # Save to Compound List
            # Format: word1, word2, combined, frequency
            comp_row = [w1, w2, output['result'], "medium"]
            generated_compounds.append(comp_row)
            
            # Save to Test Cases (Take first 600 for testing)
            if len(generated_tests) < 600:
                # Format: test_id, word1, word2, expected, rule, valid
                test_id = len(generated_tests) + 1
                test_row = [test_id, w1, w2, output['result'], output['rule'][:15], "yes"]
                generated_tests.append(test_row)
                
            if len(generated_compounds) % 100 == 0:
                print(f"   ... Generated {len(generated_compounds)} matches")

        # Safety break
        if attempts > 50000:
            print("⚠️ Stopping early (checked 50k pairs). Dictionary might need more variety.")
            break

    # 3. Write to Files
    # A. Compounds
    with open(comp_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["word1", "word2", "combined", "frequency"]) # Header
        writer.writerows(generated_compounds)
    print(f"✅ Saved {len(generated_compounds)} pairs to compound_words.csv")

    # B. Test Cases
    with open(test_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["test_id", "word1", "word2", "expected_result", "sandhi_rule_used", "is_valid_compound"])
        writer.writerows(generated_tests)
    print(f"✅ Saved {len(generated_tests)} cases to word_pairs_test.csv")

if __name__ == "__main__":
    generate_massive_data()