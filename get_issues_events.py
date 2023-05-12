import json
import os
import requests
import glob
from dateutil import parser

def issue_events_parse(index):
    print(index)
    with open(f'data/issues-{index}.json', encoding="utf8") as f:
        issues = json.load(f)
        for issue in issues:
            if "pull_request" in issue:
                continue
            id = issue["number"]

            # Get the events for the current issue
            url = f'{issue["url"]}/events'
            headers={'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
            response = requests.get(url, headers=headers)

            print("Status code for URL: ", response.status_code, url)

            if response.status_code == 200:
                response_data = response.json()
                with open(f'data/events-{id}.json', 'w', encoding='utf-8') as f:
                    json.dump(response_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    PAGE_SIZE = 100
    issue_start = int(os.getenv('GITHUB_ISSUE_START_PAGE', '0'))
    issue_files = glob.glob('data/issues-*.json')

    for index, issue_file in enumerate(issue_files):
        if issue_start != 0 and issue_start != index + 1:
            continue
        issue_events_parse(index + 1)
        issue_start += 1