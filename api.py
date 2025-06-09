# This file holds functions that check GitHub:
# - Did someone approve the PR?
# - Did the status checks pass?
# It uses the GitHub token for authorization.


import requests
import logging
from config import headers


def check_code_review(org, repo, pr_number):
    # Check if the PR was approved by at least one reviewer
    url = f"https://api.github.com/repos/{org}/{repo}/pulls/{pr_number}/reviews"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        logging.warning(f"Failed to get reviews for PR #{pr_number}, Status code: {resp.status_code}")
        return False
    reviews = resp.json()

    # Go through all the reviews and look for an "APPROVED" state
    for review in reviews:
        if review.get("state") == "APPROVED":
            return True
    return False


def check_status_checks(org, repo, commit_sha):
    # Check if all status checks passed for a specific commit
    url = f"https://api.github.com/repos/{org}/{repo}/commits/{commit_sha}/status"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        logging.warning(f"Failed to get status for commit {commit_sha}, Status code:  {resp.status_code}: {resp.text}")
        return False
    status = resp.json()
    return status.get("state") == "success"