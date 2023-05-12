import csv
import json
import glob
from dateutil import parser

# Define the CSV header
csv_header = ['id', 'title', 'state', 'created', 'closed', 'time_to_close', 'url']

# Open the CSV file and write the header row
with open("data/issues.csv", "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_header)

# Get a list of all JSON files in the 'data' directory starting with 'issues-'
issue_files = glob.glob('data/issues-*.json')

# Loop through each JSON file and extract the relevant information
for index, issue_file in enumerate(issue_files):
    print(index, end=", ")

    with open(issue_file, encoding="utf8") as json_file:
        issues = json.load(json_file)

    # Loop through each issue and write the relevant information to the CSV file
    for issue in issues:
        if "pull_request" not in issue:
            created = parser.isoparse(issue["created_at"])
            time_to_close = ''
            if issue["closed_at"]:
                closed = parser.isoparse(issue["closed_at"])
                time_to_close = (closed - created).days
            csv_writer.writerow([
                issue["id"],
                issue["title"].encode('utf-8'),
                issue["state"],
                issue["created_at"],
                issue["closed_at"],
                time_to_close,
                issue["url"]
            ])