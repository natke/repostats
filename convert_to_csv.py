import csv
import json
from dateutil import parser


c = csv.writer(open("data/issues.csv", "w", newline=''))
c.writerow(['id', 'title','state','created','closed', 'time_to_close', 'url'])

list = [*range(1, 104)]
for index in list:

    print(index)

    with open(f'data/issues-{index}.json', encoding="utf8") as f:
        d = json.load(f)

    pr = "pull_request"
    for x in d:
        labels = x["labels"]
        for label in labels:
            if (label["name"] == 'component:documentation'):
                print(x["id"])
                if not pr in x:
                    created = parser.isoparse(x["created_at"])
                    time_to_close =  ''
                    if (x["closed_at"]):
                        time_to_close = (parser.isoparse(x["closed_at"]) - created).days
                    c.writerow([x["id"], x["title"].encode('utf-8'), x["state"], x["created_at"], x["closed_at"], time_to_close, x["url"]])

