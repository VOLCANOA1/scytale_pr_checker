# This script talks to the GitHub API and gets all merged pull requests.
# It goes over each page and saves only the PRs that were actually merged.
# The results are saved as a JSON file in data/raw/.


import os
import requests
import json
from dotenv import load_dotenv
import logging
from config import headers, ORG, REPO


# Set up logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/log.txt"),
        logging.StreamHandler()
    ]
)



def fetch_merged_prs():
    merged_prs = []
    page = 1

    # Keep going through pages until there's no more data
    while True:
        url = f"https://api.github.com/repos/{ORG}/{REPO}/pulls"
        params = {
            "state": "closed",
            "per_page": 100,
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            logging.error(f"Error: {response.status_code}, {response.text}")
            break

        data = response.json()
        if not data:
            logging.info("No more PRs found.")
            break

        # Only add PRs that were actually merged
        for pr in data:
            if pr.get("merged_at"):
                merged_prs.append(pr)

        logging.info(f"Page {page}: Found {len(data)} PRs, {len(merged_prs)} merged so far")
        page += 1

    return merged_prs

if __name__ == "__main__":
    logging.info(f"Fetching merged PRs from {ORG}/{REPO}...")

    # Get all merged PRs
    prs = fetch_merged_prs()

    
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/merged_prs.json", "w") as f:
        json.dump(prs, f, indent=2)
    logging.info(f"{len(prs)} merged PRs saved to data/raw/merged_prs.json")
