import csv
import os
import sys
from word_joiner import KannadaWordBuilder

# ANSI Colors for Terminal Output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
YELLOW = "\033[93m"

def run_validation():
    # 1. Setup Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file = os.path.join(base_dir, 'test cases', 'word_pairs_test.csv')

    if not os.path.exists(test_file):
        print(f"{RED}Error: Test file not found at {test_file}{RESET}")
        return

    # 2. Initialize System
    print("Initializing Kannada Word Builder System...")
    try:
        builder = KannadaWordBuilder()
    except Exception as e:
        print(f"{RED}CRITICAL: System failed to start. {e}{RESET}")
        return

    # 3. Metrics
    total_tests = 0
    passed = 0
    failed = 0
    results = []

    print(f"\n{'ID':<5} {'Word 1':<10} {'Word 2':<10} {'Expected':<15} {'Actual':<15} {'Result'}")
    print("-" * 70)

    # 4. Run Tests
    with open(test_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            total_tests += 1
            test_id = row['test_id']
            w1 = row['word1']
            w2 = row['word2']
            expected = row['expected_result']

            # Run the System Logic
            # Note: Our builder returns a dict {'result': ..., 'status': ...}
            system_output = builder.join_words(w1, w2)
            actual = system_output['result']

            # Compare (Stripping whitespace just in case)
            if actual and expected and actual.strip() == expected.strip():
                passed += 1
                status = f"{GREEN}PASS{RESET}"
            else:
                failed += 1
                status = f"{RED}FAIL{RESET}"
            
            print(f"{test_id:<5} {w1:<10} {w2:<10} {expected:<15} {actual if actual else 'None':<15} {status}")

    # 5. Final Report
    accuracy = (passed / total_tests) * 100 if total_tests > 0 else 0

    print("\n" + "="*30)
    print("   TEST EXECUTION REPORT   ")
    print("="*30)
    print(f"Total Cases: {total_tests}")
    print(f"Passed:      {GREEN}{passed}{RESET}")
    print(f"Failed:      {RED}{failed}{RESET}")
    print(f"Accuracy:    {YELLOW}{accuracy:.2f}%{RESET}")
    print("="*30)

    # 6. Evaluation Metric Check 
    if accuracy >= 80:
        print(f"{GREEN}✅ SUCCESS: You meet the Hackathon Requirement (>80%){RESET}")
    else:
        print(f"{RED}❌ FAIL: Improve rules to reach 80% accuracy.{RESET}")

if __name__ == "__main__":
    run_validation()