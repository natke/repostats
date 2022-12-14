import csv
import json
import glob
from dateutil import parser


c = csv.writer(open("data/issues.csv", "w", newline=''))
c.writerow(['id', 'title','state','created','closed', 'time_to_close', 'url'])

issue_files = glob.glob('data/docs-issues-*.json')
for issue_file in issue_files:

    print(issue_file)

    with open(issue_file, encoding="utf8") as f:
        d = json.load(f)   

    pr = "pull_request"
    for x in d:
        labels = x["labels"]
        for label in labels:
            if (label["name"] == 'component:documentation'):
                if not pr in x:
                    print(x["id"])
                    created = parser.isoparse(x["created_at"])
                    time_to_close =  ''
                    if (x["closed_at"]):
                        time_to_close = (parser.isoparse(x["closed_at"]) - created).days
                    c.writerow([x["id"], x["title"].encode('utf-8'), x["state"], x["created_at"], x["closed_at"], time_to_close, x["url"]])

