import os
import sys
import requests
import json
import urllib.parse

def get_pr_info(page):
    # Create an API request

# Construct the URL with the environment variable
    github_issue_label = os.getenv("GITHUB_ISSUE_TAG")
    if github_issue_label:
        github_issue_label = urllib.parse.quote(github_issue_label)

    # Construct the URL with the environment variable
    url = f"https://api.github.com/repos/{URL}/issues?labels={github_issue_label}" if github_issue_label else f"https://api.github.com/repos/{URL}/issues"
    print(url)
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {
        "per_page": 100,
        "page": page,
        "since": "2022-01-01",
        "state": "all",
        "direction": "asc",
        "base": "gh-pages",
        "labels": "pytorch",
    }
    response = requests.get(url, headers=headers, params=params)

    print(f"Status code: {response.status_code}")

    if response.ok:
        # Save the API response in a variable
        response_data = response.json()

        # Evaluate the results
        num_prs = len(response_data)
        print(f"Number of PRs in page {page}: {num_prs}")

        # Save the response data to a file
        with open(f"data/prs-{page}.json", "w", encoding="utf-8") as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)

        return num_prs
    else:
        sys.exit(f"HTTP request for page {page} did not succeed")


if __name__ == "__main__":
    TOKEN = os.getenv("GITHUB_TOKEN")
    URL = os.getenv("GITHUB_URL")
    github_issue_label = os.getenv("GITHUB_ISSUE_TAG")
    PAGE_SIZE = 100
    START_PAGE = int(os.getenv("GITHUB_PR_START_PAGE"))

    # Check if the environment variable for starting page is set
    assert START_PAGE is not None, "Set environment variable GITHUB_PR_START_PAGE for PR query"

    num_prs = PAGE_SIZE
    page = START_PAGE

    # Get PRs in ascending order until the last page
    while num_prs == PAGE_SIZE:
        num_prs = get_pr_info(page)
        page += 1
