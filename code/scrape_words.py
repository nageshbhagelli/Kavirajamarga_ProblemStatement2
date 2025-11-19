import requests
from bs4 import BeautifulSoup
import re
import csv
import os

# Target: Kannada Wikipedia

URLS = [
    "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B2%B0%E0%B3%8D%E0%B2%A8%E0%B2%BE%E0%B2%9F%E0%B2%95", # Karnataka
    "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B2%A8%E0%B3%8D%E0%B2%A8%E0%B2%A1_%E0%B2%B8%E0%B2%BE%E0%B2%B9%E0%B2%BF%E0%B2%A4%E0%B3%8D%E0%B2%AF", # Kannada Literature
    "https://kn.wikipedia.org/wiki/%E0%B2%B9%E0%B2%82%E0%B2%AA%E0%B2%BF", # Hampi
    "https://kn.wikipedia.org/wiki/%E0%B2%AE%E0%B3%88%E0%B2%B8%E0%B3%82%E0%B2%B0%E0%B3%81", # Mysore
    "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B3%81%E0%B2%B5%E0%B3%86%E0%B2%82%E0%B2%AA%E0%B3%81", # Kuvempu
    "https://kn.wikipedia.org/wiki/%E0%B2%B0%E0%B2%BE%E0%B2%9C%E0%B3%8D%E0%B2%95%E0%B3%81%E0%B2%AE%E0%B2%BE%E0%B2%B0%E0%B3%8D", # Rajkumar
    "https://kn.wikipedia.org/wiki/%E0%B2%AC%E0%B3%86%E0%B2%82%E0%B2%97%E0%B2%B3%E0%B3%82%E0%B2%B0%E0%B3%81", # Bengaluru
    "https://kn.wikipedia.org/wiki/%E0%B2%AD%E0%B2%BE%E0%B2%B0%E0%B2%A4", # India
    "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B2%A8%E0%B3%8D%E0%B2%A8%E0%B2%A1_%E0%B2%9A%E0%B2%B2%E0%B2%A8%E0%B2%9A%E0%B2%BF%E0%B2%A4%E0%B3%8D%E0%B2%B0", # Kannada Cinema
    "https://kn.wikipedia.org/wiki/%E0%B2%AF%E0%B2%95%E0%B3%8D%E0%B2%B7%E0%B2%97%E0%B2%BE%E0%B2%A8", # Yakshagana
    "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B2%A8%E0%B3%8D%E0%B2%A8%E0%B2%A1", # Kannada Language
    "https://kn.wikipedia.org/wiki/%E0%B2%AC%E0%B2%B8%E0%B2%B5%E0%B2%A3%E0%B3%8D%E0%B2%A3", # Basavanna
    "https://kn.wikipedia.org/wiki/%E0%B2%B5%E0%B2%BF%E0%B2%B6%E0%B3%8D%E0%B2%B5%E0%B3%87%E0%B2%B6%E0%B3%8D%E0%B2%B5%E0%B2%B0%E0%B2%AF%E0%B3%8D%E0%B2%AF", # Sir M Visvesvaraya
    "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B2%BE%E0%B2%B5%E0%B3%87%E0%B2%B0%E0%B2%BF_%E0%B2%A8%E0%B2%A6%E0%B2%BF", # Kaveri River
    "https://kn.wikipedia.org/wiki/%E0%B2%97%E0%B3%8B%E0%B2%B2%E0%B3%8D_%E0%B2%97%E0%B3%81%E0%B2%AE%E0%B3%8D%E0%B2%AE%E0%B2%9F", # Gol Gumbaz
    "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B2%B0%E0%B3%8D%E0%B2%A8%E0%B2%BE%E0%B2%9F%E0%B2%95", # Karnataka
    "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B2%A8%E0%B3%8D%E0%B2%A8%E0%B2%A1_%E0%B2%B8%E0%B2%BE%E0%B2%B9%E0%B2%BF%E0%B2%A4%E0%B3%8D%E0%B2%AF", # Kannada Literature
]

# Headers are required to prevent Wikipedia from blocking the script
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Regex for Kannada characters (Unicode block: U+0C80 to U+0CFF)
KANNADA_REGEX = r"[\u0C80-\u0CFF]{2,}"

def get_existing_words(filepath):
    existing = set()
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['word']:
                    existing.add(row['word'])
    return existing

def scrape_wikipedia():
    # Construct absolute path to avoid "file not found" errors
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE_PATH = os.path.join(BASE_DIR, 'dictionaries', 'root_words.csv')
    
    existing_words = get_existing_words(FILE_PATH)
    new_words = set()

    print(f"Starting scrape... (Already have {len(existing_words)} words)")

    for url in URLS:
        print(f"\nFetching: {url}")
        try:
            # Added headers=HEADERS here
            response = requests.get(url, headers=HEADERS)
            response.encoding = 'utf-8' # Force UTF-8 encoding
            
            if response.status_code != 200:
                print(f"❌ Failed with Status Code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text from paragraphs
            text_content = " ".join([p.text for p in soup.find_all('p')])
            
            # Debug: Print first 50 chars to verify we got Kannada text
            print(f"   Preview content: {text_content[:50]}...") 
            
            # Find all Kannada words
            matches = re.findall(KANNADA_REGEX, text_content)
            print(f"   Found {len(matches)} potential words on this page.")
            
            for word in matches:
                # Clean the word (remove extra whitespace)
                word = word.strip()
                if word and word not in existing_words and word not in new_words:
                    new_words.add(word)
                    
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")

    print(f"\nTotal new unique words found: {len(new_words)}")

    # Append to CSV
    if new_words:
        with open(FILE_PATH, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            count = 0
            for word in new_words:
                # Format: word, meaning, word_type, last_sound, can_combine
                writer.writerow([word, "TODO", "noun", "TODO", "yes"])
                count += 1
            print(f"✅ Success! Appended {count} words to root_words.csv")
    else:
        print("⚠️ No new words to add.")

if __name__ == "__main__":
    scrape_wikipedia()