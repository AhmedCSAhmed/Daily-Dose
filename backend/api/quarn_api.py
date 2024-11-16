import requests
import json
import random

# Base URL for Quran API
BASE_URL = "https://api.quran.com/api/v4/chapters"

# Generate a random chapter ID between 1 and 114 (inclusive) to retrieve information for
chapter_id = random.randint(1, 113)

# Fetches all chapter data from the Quran API
def fetch_all_chapters():
    """
    Fetches a list of all chapters from the Quran API.

    Returns:
        dict: A parsed JSON object containing all chapter data.
    """
    headers = {'Accept': 'application/json'}
    response = requests.get(BASE_URL, headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Fetches detailed information for a specific chapter
def fetch_chapter_info(chapter_id):
    """
    Fetches detailed information about a specific chapter from the Quran API.

    Args:
        chapter_id (int): The ID of the chapter.

    Returns:
        str: The detailed chapter information text.
    """
    chapter_info_url = f"{BASE_URL}/{chapter_id}/info"
    response = requests.get(chapter_info_url)
    
    # Check if request was successful
    if response.status_code == 200:
        return response.json().get('chapter_info', {}).get('text', "Chapter information not found.")
    else:
        response.raise_for_status()

# Extracts the name of a specific chapter from the parsed chapters data
def get_chapter_name(chapters_data, chapter_id):
    """
    Retrieves the name of a chapter given its ID from the parsed chapter data.

    Args:
        chapters_data (dict): Parsed JSON response containing chapter data.
        chapter_id (int): The ID of the chapter.

    Returns:
        str: The name of the chapter.
    """
    chapters_list = chapters_data.get('chapters', [])
    
    # Ensure chapter_id is within the valid range
    if 1 <= chapter_id <= len(chapters_list):
        return chapters_list[chapter_id - 1].get('name_complex', "Name not available.")
    else:
        return "Chapter ID out of range."

# Fetch and display all chapters' data
try:
    all_chapters_data = fetch_all_chapters()
except requests.HTTPError as e:
    print("Failed to fetch chapter data:", e)
