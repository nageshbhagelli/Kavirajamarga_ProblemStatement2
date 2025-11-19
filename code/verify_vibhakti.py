from word_joiner import KannadaWordBuilder

def test_vibhakti():
    print("--- Testing Vibhakti Features  ---")
    builder = KannadaWordBuilder()
    
    test_cases = [
        ("ಮನೆ", "ಗೆ", "ಮನೆಗೆ"),         # Mane + ge = Manege
        ("ಮನೆ", "ಅಲ್ಲಿ", "ಮನೆಯಲ್ಲಿ"),   # Mane + alli = Maneyalli
        ("ಮನೆ", "ಇಂದ", "ಮನೆಯಿಂದ"),     # Mane + inda = Maneyinda
        ("ಪುಸ್ತಕ", "ಅನ್ನು", "ಪುಸ್ತಕವನ್ನು"), # Pustaka + annu = Pustakavannu
        ("ಮಗು", "ಗೆ", "ಮಗುವಿಗೆ"),       # Magu + ge = Maguvige
        ("ಸ್ಥಳ", "ಅಲ್ಲಿ", "ಸ್ಥಳದಲ್ಲಿ")   # Sthala + alli = Sthaladalli
    ]

    passed = 0
    for w1, w2, expected in test_cases:
        output = builder.join_words(w1, w2)
        res = output['result']
        if res == expected:
            print(f"✅ PASS: {w1} + {w2} -> {res}")
            passed += 1
        else:
            print(f"❌ FAIL: {w1} + {w2} -> {res} (Expected: {expected})")

    print(f"\nScore: {passed}/{len(test_cases)}")

if __name__ == "__main__":
    test_vibhakti()