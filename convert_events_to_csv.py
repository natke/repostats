import csv
import json
import glob
import re
import datetime
import os
from dateutil import parser

c = csv.writer(open("data/events.csv", "w", newline=''))
c.writerow(['id', 'title','state','created','first_update', 'closed', 'time_to_update', 'time_to_close', 'url'])

#issue_files = glob.glob('data/issues-*.json')
#for issue_file in issue_files:

list = [*range(1, 117)]
for index in list:

    print(index)

    with open(f'data/issues-{index}.json', encoding="utf8") as f:
        d = json.load(f)

    #print(issue_file)

    #with open(issue_file, encoding="utf8") as f:
    #    d = json.load(f)


    for x in d:
        if not "pull_request" in x:
            id = x["number"]
    #        print(id)
            created = parser.isoparse(x["created_at"])
            time_to_close =  ''
            if (x["closed_at"]):
                time_to_close = (parser.isoparse(x["closed_at"]) - created).days

            events_file=f'data/events-{id}.json'
            first_update = ''
            time_to_update = ''

            if os.path.exists(events_file):
                with open(events_file, encoding="utf8") as g:
                    e = json.load(g)

                    for y in e:
                        event_type = y["event"]
                        event_time = parser.isoparse(y["created_at"])
                        if first_update == '' or event_time < first_update:
                            first_update = event_time
                            print(f'Updating first update time for issue: {id} with {event_type} {event_time} {created} {(first_update - created).days}')

            if first_update != '':
                time_to_update = (first_update - created).days
            c.writerow([id, x["title"].encode('utf-8'), x["state"], x["created_at"], first_update, x["closed_at"], time_to_update, time_to_close, x["url"]])






    