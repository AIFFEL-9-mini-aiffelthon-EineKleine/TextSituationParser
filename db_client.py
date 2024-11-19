import requests
from diary_analysis import DiarySentimentAnalysis

import time
import sys
from typing import List

# API Config
API_BASE_URL = "http://localhost:8000/api"
DIARY_ENDPOINT = f"{API_BASE_URL}/diary"
EMOTIONS_ENDPOINT = f"{API_BASE_URL}/keywords"

# Interval between loop iterations in seconds
LOOP_INTERVAL = 60  # e.g., 60 seconds

def fetch_diary_entries() -> List[dict]:
    """
    Fetch all diary entries from the backend.
    """
    try:
        response = requests.get(DIARY_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching diary entries: {e}")
        return []

def fetch_existing_emotions(entry_id: int) -> List[str]:
    """
    Fetch existing emotions for a specific diary entry.
    """
    try:
        response = requests.get(EMOTIONS_ENDPOINT)
        response.raise_for_status()
        all_emotions = response.json()
        # Filter emotions for the specific entry_id
        return [emo['emotion'] for emo in all_emotions if emo['entry_id'] == entry_id]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching emotions for entry ID {entry_id}: {e}")
        return []

# def extract_emotions(text: str, max_emotions: int = 5) -> List[str]:
#     """
#     Extract emotions from the provided text using RAKE.
#     """
#     rake = Rake()
#     rake.extract_keywords_from_text(text)
#     emotions = rake.get_ranked_phrases()
#     return emotions[:max_emotions]  # Return top N emotions

def post_emotion(entry_id: int, emotion: str):
    """
    Post a single emotion to the backend for a specific diary entry.
    """
    payload = {
        "entry_id": entry_id,
        "emotion": emotion
    }
    try:
        response = requests.post(EMOTIONS_ENDPOINT, json=payload)
        response.raise_for_status()
        print(f"Posted emotion '{emotion}' for entry ID {entry_id}.")
    except requests.exceptions.RequestException as e:
        print(f"Error posting emotion '{emotion}' for entry ID {entry_id}: {e}")

def process_entry(entry: dict):
    """
    Process a single diary entry: extract and post new emotions.
    """
    entry_id = entry.get("id")
    content = entry.get("content", "")
    if not entry_id or not content:
        print(f"Invalid entry data: {entry}")
        return

    print(f"\nProcessing Entry ID {entry_id}:")
    print(f"Content: {content}")

    # Fetch existing emotions to avoid duplicates
    existing_emotions = fetch_existing_emotions(entry_id)
    print(f"Existing Emotions: {existing_emotions}")

    # Extract new emotions
    extract_emotions = EmotionExtractor()  # TODO
    extracted_emotions = extract_emotions(content)
    print(f"Extracted Emotions: {extracted_emotions}")

    # Determine new emotions to post
    new_emotions = [emo for emo in extracted_emotions if emo not in existing_emotions]

    if not new_emotions:
        print(f"No new emotions to add for entry ID {entry_id}.")
        return

    # Post new emotions
    for emotion in new_emotions:
        post_emotion(entry_id, emotion)

def run_loop(interval: int = LOOP_INTERVAL):
    """
    Continuously run the emotion extraction and posting process at defined intervals.
    """
    print(f"Starting the emotion extraction loop. Processing every {interval} seconds.")
    try:
        while True:
            print("\n--- New Iteration ---")
            if entries := fetch_diary_entries():
                for entry in entries:
                    process_entry(entry)
            else:
                print("No diary entries found.")
            print(f"Iteration complete. Sleeping for {interval} seconds.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nLoop interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    """
    Main function to start the loop.
    """
    run_loop()

if __name__ == "__main__":
    main()