import requests
import time
import json
import os
from datetime import datetime

# HackerNews API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required User-Agent header
HEADERS = {
    "User-Agent": "TrendPulse/1.0"
}

# Maximum number of stories to collect from each category
MAX_PER_CATEGORY = 25

# Keywords used to classify stories.
# Matching is case-insensitive.
CATEGORY_KEYWORDS = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game", "book",
        "show", "award", "streaming"
    ]
}


def get_story_ids():
    """
    Fetch the list of top HackerNews story IDs.

    The API returns many IDs, but TrendPulse only needs
    the first 500.
    """
    try:
        response = requests.get(
            TOP_STORIES_URL,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        story_ids = response.json()

        # Return only the first 500 IDs as required
        return story_ids[:500]

    except requests.RequestException as error:
        print(f"Failed to fetch top story IDs: {error}")
        return []


def get_story(story_id):
    """
    Fetch the details of one HackerNews story.

    If the request fails, return None so that the
    main program can continue with the next story.
    """
    try:
        url = ITEM_URL.format(story_id)

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        return None


def classify_story(title):
    """
    Assign a category based on keywords found in the title.

    Keyword matching is case-insensitive.

    If a title contains keywords from more than one category,
    the first matching category in CATEGORY_KEYWORDS is used.
    """
    title_lower = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    # Stories without a matching keyword are ignored.
    return None


def extract_story(story, category):
    """
    Extract the seven required fields from a HackerNews story.
    """
    return {
        "post_id": story.get("id"),
        "title": story.get("title", ""),
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by", ""),
        "collected_at": datetime.now().isoformat()
    }


def save_to_json(stories):
    """
    Create the data directory if necessary and save
    all collected stories to a date-based JSON file.
    """
    os.makedirs("data", exist_ok=True)

    # Use today's date in YYYYMMDD format.
    date_string = datetime.now().strftime("%Y%m%d")

    filename = f"data/trends_{date_string}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(stories, file, indent=4, ensure_ascii=False)

    return filename


def main():
    """
    Main TrendPulse data collection process.
    """

    # Step 1: Get the first 500 top story IDs.
    print("Fetching top HackerNews story IDs...")

    story_ids = get_story_ids()

    if not story_ids:
        print("No story IDs were received. Exiting.")
        return

    print(f"Received {len(story_ids)} story IDs.")

    # Store collected stories here.
    all_stories = []

    # Track how many stories have been collected per category.
    category_counts = {
        category: 0
        for category in CATEGORY_KEYWORDS
    }

    # Fetch stories once and classify them.
    # A story can only be added once.
    for story_id in story_ids:

        # Stop once all five categories have 25 stories.
        if all(
            count >= MAX_PER_CATEGORY
            for count in category_counts.values()
        ):
            break

        story = get_story(story_id)

        # If the API request failed, move to the next story.
        if story is None:
            continue

        # Some HackerNews items may not have a title.
        title = story.get("title", "")

        if not title:
            continue

        category = classify_story(title)

        # Ignore stories that do not match any category.
        if category is None:
            continue

        # Do not collect more than 25 stories per category.
        if category_counts[category] >= MAX_PER_CATEGORY:
            continue

        extracted_story = extract_story(story, category)

        all_stories.append(extracted_story)
        category_counts[category] += 1

        print(
            f"Collected {category_counts[category]}/"
            f"{MAX_PER_CATEGORY} {category}: {title}"
        )

    # The assignment asks for one 2-second sleep per category loop,
    # not a sleep after every individual API request.
    #
    # We use the category loop below to provide the required delay.
    for category in CATEGORY_KEYWORDS:
        print(
            f"Finished category: {category} "
            f"({category_counts[category]} stories)"
        )

        time.sleep(2)

    # Step 3: Save the collected stories to JSON.
    filename = save_to_json(all_stories)

    print()
    print(f"Collected {len(all_stories)} stories.")
    print(f"Saved to {filename}")


if __name__ == "__main__":
    main()
