import json
import os
import requests
import glob
from dateutil import parser

TOKEN=os.getenv('GITHUB_TOKEN')
PAGE_SIZE=100

num_issues = PAGE_SIZE

issue_files = glob.glob('data/issues-*.json')
for issue_file in issue_files:

    print(issue_file)
    with open(issue_file, encoding="utf8") as f:
        d = json.load(f)

        for x in d:
            if not "pull_request" in x:

                id = x["number"]

                # Get the events for the current issue
                url = f'{x["url"]}/comments'
                headers={'Authorization': f'token {TOKEN}'}  
                response = requests.get(url, headers=headers)

                if response.status_code == 200:

                    response_data = response.json()

                    with open(f'data/comments-{id}.json', 'w', encoding='utf-8') as f:
                        json.dump(response_data, f, ensure_ascii=False, indent=4)
                else:
                    exit('API error. Exiting')


                    
