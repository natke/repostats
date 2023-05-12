import json
import os
import requests         
import glob

def parse_issue_comments(index):
    with open(f'data/issues-{index}.json', encoding="utf8") as f:
        issues_data = json.load(f)
        
        for issue in issues_data:
            if "pull_request" in issue:
                continue
                
            id = issue["number"]
            url = f'{issue["url"]}/comments'
            headers = {'Authorization': f'token {TOKEN}'}
            
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                
                with open(f'data/comments-{id}.json', 'w', encoding='utf-8') as f:
                    json.dump(response_data, f, ensure_ascii=False, indent=4)
            else:
                print(f'Error: {response.status_code}')

if __name__ == '__main__':
    TOKEN = os.getenv('GITHUB_TOKEN')
    issue_start = int(os.getenv('GITHUB_ISSUE_START_PAGE') or 0)
    issue_files = glob.glob('data/issues-*.json')
    
    for index, issue_file in enumerate(issue_files, start=issue_start):
        parse_issue_comments(index)