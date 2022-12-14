import os
import requests
import json

TOKEN=os.getenv('GITHUB_TOKEN')
PAGE_SIZE=100
START_PAGE=int(os.getenv('GITHUB_ISSUE_START_PAGE'))
assert START_PAGE != None, "Set environment variable GITHUB_ISSUE_START_PAGE for issues query"

num_issues = PAGE_SIZE
page=START_PAGE

# Get issues in descending order (oldest first) until the last page
while (num_issues == PAGE_SIZE):
  # Create an API request 
  url = 'https://api.github.com/repos/microsoft/onnxruntime/issues'
  headers={'Authorization': f'token {TOKEN}'}  
  params = {'per_page': 100, 'page': page, 'since': "2019-01-01", 'state': "all", 'direction': "asc"}
  response = requests.get(url, headers=headers, params=params)

  print(f'Request headers: {headers}; Response status code: {response.status_code}')

  # In a variable, save the API response.
  response_data = response.json()

  # Evaluate the results.
  num_issues = len(response_data)
  print(f'Number of issues in page {page} {num_issues}')

  with open(f'data/issues-{page}.json', 'w', encoding='utf-8') as f:
    json.dump(response_data, f, ensure_ascii=False, indent=4)

  page=page+1
