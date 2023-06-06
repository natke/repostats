import os
import requests
import json
import urllib.parse

def get_github_issues():
    github_issue_label = os.getenv("GITHUB_ISSUE_TAG")
    URL = os.getenv("GITHUB_URL")
    if github_issue_label:
        github_issue_label = urllib.parse.quote(github_issue_label)

    # Construct the URL with the environment variable
    url = f"https://api.github.com/repos/{URL}/issues?labels={github_issue_label}" if github_issue_label else f"https://api.github.com/repos/{URL}/issues"
    print(url)
    headers = {'Authorization': f'Bearer {os.getenv("GITHUB_TOKEN")}'}
    page = int(os.getenv('GITHUB_ISSUE_START_PAGE', 1))
    page_size = 100
    
    while True:
        params = {
            'per_page': page_size,
            'page': page,
            'since': '2022-01-01',
            'state': 'all',
            'direction': 'asc',
        }
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            response_data = response.json()
            num_issues = len(response_data)
            print(f'Number of issues in page {page}: {num_issues}')

            with open(f'data/issues-{page}.json', 'w', encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=4)

            page += 1
            if num_issues < page_size:
                break
        else:
            print('API error {}. Exiting'.format(response.status_code))
            break

if __name__ == "__main__":
    get_github_issues()
