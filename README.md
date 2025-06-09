Scytale PR Checker - Home Assignment

A lightweight script tool to analyze merged pull requests from a GitHub repository and check their compliance.

Features:
--------

- Fetches all merged PRs from a given GitHub repository (single repository from the Scytale organization GitHub)
- Verifies:
  * If the PR had at least one approved code review
  * If all status checks passed
- Supports filtering PRs by merge date range
- Outputs a detailed report in CSV format
- Includes logging to console and file

---
Getting Started
---------------

1. Clone the repository
    git clone https://github.com/YOUR_USERNAME/scytale_pr_checker.git
    cd scytale_pr_checker

2. Create and activate a virtual environment (optional but recommended)
    python3 -m venv venv
    source venv/bin/activate

3. Install dependencies
    pip install -r requirements.txt

4. Set your GitHub token - Create a .env file in the project root with the following line 
    GITHUB_TOKEN = your_personal_access_token_here

Fetch PR data
--------------
python extract.py

Generate the report
-------------------
python transform.py

Or with optional date filters:
python transform.py --from-date 2023-11-01 --to-date 2023-11-30

Output
------
This will output a report to:
data/processed/report.csv

```
 Project Structure
 -----------------

├── api.py                 # GitHub API interaction  
├── utils.py               # Helper functions (e.g. date filtering)  
├── extract.py             # Fetch merged PRs  
├── transform.py           # Analyze PRs and create a report  
├── data/  
│   ├── raw/               # JSON input  
│   └── processed/         # CSV output  
├── logs/  
│   └── log.txt            # Full log output  
├── .env                   # Your GitHub token (not committed)  
├── requirements.txt  
├── README.md  
└── summary.md             # API endpoints summary  
```


# Notes
- I tried to keep the code simple and easy to understand.
- I used logging to make it easy to see what’s going on.
- I split the logic into different files so it’s not all in one place.
