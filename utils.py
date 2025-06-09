# Helper functions.
# Right now it only checks if a PR was merged in a certain date range.

from datetime import datetime


def is_in_date_range(merged_at, from_date=None, to_date=None):
    pr_date = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ")
    if from_date and pr_date < from_date:
        return False
    if to_date and pr_date > to_date:
        return False
    return True

