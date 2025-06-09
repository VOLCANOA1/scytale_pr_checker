 GitHub API Summary – Scytale PR Checker

This project uses the GitHub REST API to fetch and verify merged pull requests from a given repository. Below is a summary of the endpoints and their purpose.

Authentication
All API calls use a Personal Access Token (PAT) via the Authorization: token <your_token> header.

 Endpoints Used
 --------------
1. List Pull Requests
Endpoint:
GET /repos/{owner}/{repo}/pulls

Usage:
Retrieve all closed pull requests, including merged ones (with pagination).

Example:
GET https://api.github.com/repos/Scytale-exercise/scytale-repo3/pulls?state=closed&page=1&per_page=100

2. List Reviews on a Pull Request
Endpoint:
GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews

Usage:
Check if the PR has been approved by at least one reviewer.

Example:
GET https://api.github.com/repos/Scytale-exercise/scytale-repo3/pulls/5/reviews

3. Get Commit Status
Endpoint:
GET /repos/{owner}/{repo}/commits/{ref}/status

Usage:
Check if all required status checks passed before the PR was merged.

Example:
GET https://api.github.com/repos/Scytale-exercise/scytale-repo3/commits/abc123def/status

