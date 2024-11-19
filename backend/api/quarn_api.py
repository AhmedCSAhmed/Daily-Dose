import requests
import random
from bs4 import BeautifulSoup

# Base URL for Quran API
BASE_URL = "https://quranapi.pages.dev/api"

# Tafsir API
TAFSIR_IBNKATHIR_URL = "https://api.quran.com/api/v4/tafsirs/169/by_ayah/{surah_number}:{ayah}"
TAFSIR_MAARIF_URL = "https://api.quran.com/api/v4/tafsirs/168/by_ayah/{surah_number}:{ayah}"

# Function to generate a random chapter ID between 1 and 114 (inclusive)
def get_random_chapter_id():
    """
    Generates a random chapter ID between 1 and 114.
    
    Returns:
        int: A random chapter ID.
    """
    return random.randint(1, 114)

# Fetches detailed information for a specific chapter
def fetch_chapter_info(chapter_id):
    """
    Fetches detailed information about a specific chapter from the Quran API.

    Args:
        chapter_id (int): The ID of the chapter.

    Returns:
        dict: Parsed JSON object containing chapter details.
    """
    chapter_info_url = f"{BASE_URL}/{chapter_id}.json"
    try:
        response = requests.get(chapter_info_url)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        return response.json()
    except requests.HTTPError as e:
        print(f"Failed to fetch chapter {chapter_id}: {e}")
        return None

# Extracts the name of a chapter
def get_chapter_name(chapter_data):
    """
    Extracts the chapter name from the chapter data.

    Args:
        chapter_data (dict): JSON response containing chapter data.

    Returns:
        str: Chapter name or 'Unknown' if not found.
    """
    if chapter_data:
        return chapter_data.get("surahName", "Unknown")
    return "Unknown"

# Fetches the English translation of all Ayahs in the chapter
def get_english_translations(chapter_data):
    """
    Extracts the English translations of all Ayahs in the chapter.

    Args:
        chapter_data (dict): JSON response containing chapter data.

    Returns:
        list: List of English translations or an empty list if not found.
    """
    if chapter_data:
        return chapter_data.get("english", [])
    return []

# Prints chapter information
def print_chapter_info(chapter_data):
    """
    Prints the chapter name, total Ayahs, and English translations.

    Args:
        chapter_data (dict): JSON response containing chapter data.
    """
    if not chapter_data:
        print("No data available for the chapter.")
        return
    
    # Fetch the chapter name
    chapter_name = get_chapter_name(chapter_data)
    
    # Fetch the total number of Ayahs
    total_ayahs = chapter_data.get("totalAyah", "Unknown")
    
    # Fetch the English translations
    english_translations = get_english_translations(chapter_data)
    
    print(f"Chapter Name: {chapter_name}")
    print(f"Total Ayahs: {total_ayahs}")
    print("English Translation:")
    for i, ayah in enumerate(english_translations, start=1):
        print(f" - Ayah {i}: {ayah}")

# fetch tafsir
def fetch_tafsir(chapter: str, verse: str, version="ibn_kathir"): 
    """
    Fetches tafsir for a specific chapter and verse.
    
    Args: 
        chapter (int): The chapter to fetch
        verse (int): The verse to fetch
        version (str): The version to fetch , default with ibnu kathir
    Returns:
        str: tafsir string parsed by beatiful soup from HTML into raw text
    """
    if version == "ibn_kathir":
        url = TAFSIR_IBNKATHIR_URL.format(surah_number=chapter, ayah=verse)
    elif version == "maarif":
        url = TAFSIR_MAARIF_URL.format(surah_number=chapter, ayah=verse)
    else:
        print(f"Invalid version: {version}")
        return None
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        data = response.json()
        # Extract the tafsir text from the API response, parse it into plain text, and strip leading/trailing whitespace
        tafsir_html = data.get('tafsir', {}).get('text', '')
        soup = BeautifulSoup(tafsir_html, 'html.parser')
        plain_text = soup.get_text()
        
        return plain_text.strip()
    except requests.HTTPError as e:
        print(f"Failed to fetch tafsir for chapter {chapter}, verse {verse}: {e}")
        return None

# Main logic
if __name__ == "__main__":
    # Fetch a random chapter ID
    random_chapter_id = get_random_chapter_id()
    print(f"Fetching data for chapter ID: {random_chapter_id}")
    
    # Fetch the chapter info from the API
    chapter_data = fetch_chapter_info(random_chapter_id)
    # print random tafsir alongside chapter information
    tafsir = fetch_tafsir(random_chapter_id, 1)
    # Print the chapter info
    print_chapter_info(chapter_data)
    print(tafsir)