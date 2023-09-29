import json
import os
import requests
import glob
import argparse
import re
from dateutil import parser

TOKEN=os.getenv('GITHUB_TOKEN')

argparser = argparse.ArgumentParser()
argparser.add_argument('--org', type=str, default = 'microsoft', help='org to query')
argparser.add_argument('--repo', type=str, default = 'onnxruntime', help='repo to query')
argparser.add_argument('--start_page', type=int, help='Start page for issues query')
argparser.add_argument('--end_page', type=int, help='End page for issues query')
argparser.add_argument("--labels", type=str, help="Comma separated labels to query")
args = argparser.parse_args()

org = args.org
repo = args.repo
start_page = args.start_page
end_page = args.end_page
label_filter = args.labels
label_filter_string = ''

if label_filter:
  label_filter_string = f'-{label_filter.replace(",", "-").replace(" ", "-")}'

file_string = f'data/{org}-{repo}{label_filter_string}-issues-*.json'
issue_files = sorted(glob.glob(file_string))
start_file = issue_files[0]
end_file = issue_files[-1]
prefix = re.findall('(.*-.*)-issues-.*', start_file)[0]

if start_page is None:
  start_page = int(re.findall( '\d+', start_file)[0])

if end_page is None:
  end_page = int(re.findall( '\d+', end_file)[0])

list = [*range(start_page, end_page+1)]
for index in list:

    print(f'Page: {index}')
    with open(f'{prefix}-issues-{index:06d}.json', encoding="utf8") as f:
        d = json.load(f)

        for x in d:
            if not "pull_request" in x:

                id = x["number"]

                # Get the events for the current issue
                url = f'{x["url"]}/comments'
                headers={'Authorization': f'token {TOKEN}'}  
                response = requests.get(url, headers=headers)

                print(url)

                if response.status_code == 200:

                    response_data = response.json()

                    with open(f'{prefix}-comments-{id}.json', 'w', encoding='utf-8') as f:
                        json.dump(response_data, f, ensure_ascii=False, indent=4)
                else:
                    exit('API error. Exiting')


                    
