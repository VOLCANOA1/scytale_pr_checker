# This script loads the merged PRs and checks each one:
# - Was there an approved code review?
# - Did all status checks pass?
# You can also choose a date range.
# The output is saved as a CSV file in data/processed/.


import json
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import logging
import argparse
from datetime import datetime
from api import check_code_review, check_status_checks
from utils import is_in_date_range
from config import ORG, REPO


# Set up logging to both console and log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/log.txt"),
        logging.StreamHandler()
    ]
)


# Load merged PRs from previous extract
with open("data/raw/merged_prs.json", "r") as f:
    merged_prs = json.load(f)



if __name__ == "__main__":
    records = []

    # Parse date strings into datetime objects if provided
    parser = argparse.ArgumentParser(description="Transform merged PRs into a report")
    parser.add_argument("--from-date", type=str, help="Start date (inclusive) in YYYY-MM-DD format")
    parser.add_argument("--to-date", type=str, help="End date (inclusive) in YYYY-MM-DD format")
    args = parser.parse_args()

    from_date = datetime.strptime(args.from_date, "%Y-%m-%d") if args.from_date else None
    to_date = datetime.strptime(args.to_date, "%Y-%m-%d") if args.to_date else None

    # Go over each PR and check if it's within the date range
    for pr in merged_prs:
        pr_number = pr["number"]
        pr_title = pr["title"]
        author = pr["user"]["login"]
        merged_at = pr["merged_at"]
        if not is_in_date_range(merged_at, from_date, to_date):
            logging.info(f"Skipping PR #{pr_number} – Outside date range")
            continue
        commit_sha = pr["merge_commit_sha"]

        # Check if the PR had a code review approval and passed status checks
        cr_passed = check_code_review(ORG, REPO, pr_number)
        checks_passed = check_status_checks(ORG, REPO, commit_sha)

        # Save the results
        record = {
            "PR_number": pr_number,
            "PR_title": pr_title,
            "Author": author,
            "Merge_date": merged_at,
            "CR_Passed": cr_passed,
            "CHECKS_PASSED": checks_passed
        }

        logging.info(f"Processed PR #{pr_number} | Review: {cr_passed} | Checks: {checks_passed}")
        records.append(record)

    # Save the final report as CSV file
    df = pd.DataFrame(records)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/report.csv", index=False)
    logging.info("Report saved to data/processed/report.csv")
