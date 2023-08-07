import os
import csv
import json
import glob
from dateutil import parser


c = csv.writer(open("data/docs-issues2.csv", "w", newline=''))
c.writerow(['id', 'title','state','created','closed', 'url', 'Update Made'])

issue_files = glob.glob('data/issues-*.json')
for issue_file in issue_files:

    with open(issue_file, encoding="utf8") as f:
        d = json.load(f)   

    pr = "pull_request"
    for x in d:
        id = x["number"]
        labels = x["labels"]
        for label in labels:
            if (label["name"] == 'documentation'):
                if not pr in x:
                    print(id)
                    created = parser.isoparse(x["created_at"])
                    update_made = False

                    if (x["closed_at"]):
                        # Events data: labeling etc
                        timeline_file=f'data/json/timeline-{id}.json'

                        if os.path.exists(timeline_file):
                            with open(timeline_file, encoding="utf8") as g:
                                t = json.load(g)

                                for y in t:
                                    event_type = y["event"]
                                    event_time = parser.isoparse(y["created_at"])
                                    if event_type == "closed" or event_type == "referenced":
                                        print(y["commit_id"])
                                        if y["commit_id"] != None:
                                            update_made=True
                                    elif event_type == "cross-referenced":
                                        if y["source"]["type"] == "issue":
                                            issue = y["source"]["issue"]
                                            if "pull_request" in issue:
                                                print(y["source"]["issue"]["pull_request"]["url"])
                                                update_made=True
            
                    c.writerow([id, x["title"].encode('utf-8'), x["state"], x["created_at"], x["closed_at"], x["url"], update_made])
