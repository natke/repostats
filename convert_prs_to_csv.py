import csv
import json
import glob
import os
from dateutil import parser

def issue_parse(index):
    print(index)
    with open(f"data/prs-{index}.json", encoding="utf8") as f:
        data = json.load(f)
        for item in data:
            created = parser.isoparse(item["created_at"])
            time_to_close = ""
            if item["state"] == "closed":
                time_to_close = (parser.isoparse(item["closed_at"]) - created).days
            c.writerow([
                item["id"],
                item["title"].encode('utf-8'),
                item["state"],
                item["created_at"],
                item["closed_at"],
                time_to_close,
                item["url"]
            ])

if __name__ == "__main__":
    # Open the CSV file and write the header row
    with open("data/prs.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["id", "title", "state", "created", "closed", "time_to_close", "url"])

    # Get a list of all JSON files in the 'data' directory starting with 'prs-'
    issue_files = glob.glob("data/prs-*.json")

    # If the 'GITHUB_ISSUE_START_PAGE' environment variable is set, start parsing from that page number
    issue_start = int(os.getenv("GITHUB_ISSUE_START_PAGE")) if os.getenv("GITHUB_ISSUE_START_PAGE") else 0

    # Loop through each JSON file and extract the relevant information
    for index, issue_file in enumerate(issue_files):
        if index >= issue_start:
            issue_parse(index)