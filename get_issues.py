import os
import requests
import json
import argparse

TOKEN=os.getenv('GITHUB_TOKEN')
PAGE_SIZE=100

argparser = argparse.ArgumentParser()
argparser.add_argument('--start_page', type=int, default = 1, help='Start page for issues query')
argparser.add_argument('--end_page', type=int, default = -1, help='End page for issues query')
argparser.add_argument('--org', type=str, default = 'microsoft', help='org to query')
argparser.add_argument('--repo', type=str, default = 'onnxruntime', help='repo to query')
argparser.add_argument("--labels", type=str, help="List of comma separated GitHub labels from the repo")
args = argparser.parse_args()

start_page = args.start_page
end_page = args.end_page
org = args.org
repo = args.repo
labels = args.labels

num_issues = PAGE_SIZE
page=start_page

# Get issues in descending order (oldest first) until the last page
while (num_issues == PAGE_SIZE and (end_page == -1 or page <= end_page)):
  # Create an API request 
  url = f'https://api.github.com/repos/{org}/{repo}/issues'
  if labels != None:
    url += f'?labels={labels}'
  headers={'Authorization': f'token {TOKEN}'}  
  params = {'per_page': 100, 'page': page, 'state': "all", 'direction': "asc"}
  response = requests.get(url, headers=headers, params=params)

  response_data = response.json()

  num_issues = len(response_data)
  print(f'Number of issues in page {page} {num_issues}')

  ordered_page = f'{page:06d}'

  with open(f'data/{org}-{repo}{labels.replace(":","")}-issues-{ordered_page}.json', 'w', encoding='utf-8') as f:
    json.dump(response_data, f, ensure_ascii=False, indent=4)

  page=page+1
