import os
import sys
import requests
import json

TOKEN=os.getenv('GITHUB_TOKEN')
PAGE_SIZE=100
START_PAGE=int(os.getenv('GITHUB_PR_START_PAGE'))
assert START_PAGE != None, "Set environment variable GITHUB_PR_START_PAGE for PR query"

num_prs = PAGE_SIZE
page=START_PAGE

# Get issues in descending order (oldest first) until the last page
while (num_prs == PAGE_SIZE):
  # Create an API request 
  url = 'https://api.github.com/repos/microsoft/onnxruntime/pulls'
  headers={'Authorization': f'access_token {TOKEN}'}  
  params = {'per_page': 100, 'page': page, 'since': "2019-01-01", 'state': "all", 'direction': "asc", 'base': "gh-pages"}
  response = requests.get(url, headers=headers, params=params)

  print("Status code: ", response.status_code)

  if response.status_code == 200:
    # In a variable, save the API response.
    response_data = response.json()

    # Evaluate the results.
    num_prs = len(response_data)
    print(f'Number of PRs in page {page} {num_prs}')

    with open(f'data/prs-{page}.json', 'w', encoding='utf-8') as f:
      json.dump(response_data, f, ensure_ascii=False, indent=4)

    page=page+1
  else:
    sys.exit(f'HTTP request for page {page} did not succeed')
