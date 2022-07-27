import json
from dateutil import parser
import os
import requests
import glob

TOKEN=os.getenv('GITHUB_TOKEN')
PAGE_SIZE=100

num_issues = PAGE_SIZE


#issue_files = glob.glob('data/issues-*.json')
#for issue_file in issue_files:

list = [*range(1, 117)]
for index in list:

    #print(issue_file)
    #with open(issue_file, encoding="utf8") as f:
    #    d = json.load(f)

    print(index)
    with open(f'data/issues-{index}.json', encoding="utf8") as f:
        d = json.load(f)

        for x in d:
            if not "pull_request" in x:

                id = x["number"]

                # Get the events for the current issue
                url = f'{x["url"]}/events'
                headers={'Authorization': f'access_token {TOKEN}'}  
                response = requests.get(url, headers=headers)

                print("Status code for URL: ", response.status_code, url)

                if response.status_code == 200:

                    response_data = response.json()

                    with open(f'data/events-{id}.json', 'w', encoding='utf-8') as f:
                        json.dump(response_data, f, ensure_ascii=False, indent=4)


                    
