import csv
import json
from dateutil import parser


c = csv.writer(open("data/prs.csv", "w", newline=''))
c.writerow(['id', 'title','state','created','closed', 'time_to_close', 'url'])

list = [*range(1, 76)]
for index in list:

    print(index)

    with open(f'data/prs-{index}.json', encoding="utf8") as f:
        d = json.load(f)

    for x in d:
        base = x["base"]
        if base["label"] == 'microsoft:gh-pages':
            print(x["id"])
            created = parser.isoparse(x["created_at"])
            time_to_close =  ''
            if (x["closed_at"]):
               time_to_close = (parser.isoparse(x["closed_at"]) - created).days
               c.writerow([x["id"], x["title"].encode('utf-8'), x["state"], x["created_at"], x["closed_at"], time_to_close, x["url"]])

