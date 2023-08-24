import csv
import json
import glob
import re
import os
import datetime
import argparse
from dateutil import parser

argparser = argparse.ArgumentParser()
argparser.add_argument('--org', type=str, default = 'microsoft', help='org to query')
argparser.add_argument('--repo', type=str, default = 'onnxruntime', help='repo to query')
argparser.add_argument("--labels", type=str, help="Comma separated labels to query")

args = argparser.parse_args()

org = args.org
repo = args.repo
labels = args.labels
if labels != None:
  labels = labels.replace(":", "")
  file_string = 'data/' + org + '-' + repo + labels + '-issues-*.json'
else:
  file_string = 'data/' + org + '-' + repo + '-issues-*.json'
  
issue_files = glob.glob(file_string)
start_file = issue_files[0]
prefix = re.findall('(.*-.*)-issues-.*', start_file)[0]

date = datetime.date.today().strftime('%Y-%m-%d')

label_list_string = ''

c = csv.writer(open(f'{prefix}-sla-{date}.csv', "w", newline=''))
c.writerow(['org','repos','filter', 'labels', 'id', 'title','state','created','first_event', 'first_comment', 'closed', 'time_to_event', 'event_type', 'time_to_comment', 'time_to_close', 'url'])


for issue_file in issue_files:

    with open(issue_file, encoding="utf8") as f:
        d = json.load(f)

    for x in d:
        if not "pull_request" in x:
            # Issue data
            id = x["number"]
            print(f'Issue: {id}')
            created = parser.isoparse(x["created_at"])
            time_to_close =  ''
            if (x["closed_at"]):
                time_to_close = (parser.isoparse(x["closed_at"]) - created).days

            # Get labels for issue
            label_data = x["labels"]
            if label_data:
                print(f'There are labels: {label_data}')
                label_list = [o["name"] for o in label_data]
                label_list_string = ';'.join(label_list)
                print(label_list)

            # Events data: labeling etc
            events_file=f'{prefix}-events-{id}.json'
            first_update = ''
            time_to_update = ''
            update_type = ''

            if os.path.exists(events_file):
                with open(events_file, encoding="utf8") as g:
                    e = json.load(g)

                    for y in e:
                        event_type = y["event"]
                        event_time = parser.isoparse(y["created_at"])
                        if first_update == '' or event_time < first_update:
                            first_update = event_time
                            update_type = event_type
                            #print(f'Updating first update time for issue: {id} with {event_type} {event_time} {created} {(first_update - created).days}')

            if first_update != '':
                time_to_update = (first_update - created).days
            
            # Comments data
            comments_file=f'{prefix}-comments-{id}.json'
            first_comment = ''
            time_to_comment = ''

            if os.path.exists(comments_file):
                with open(comments_file, encoding="utf8") as h:
                    d = json.load(h)

                    for z in d:
                        comment_time = parser.isoparse(z["created_at"])
                        if first_comment == '' or comment_time < first_comment:
                            first_comment = comment_time

            if first_comment != '':
                time_to_comment = (first_comment - created).days
              
            c.writerow([org, repo, labels, label_list_string, id, x["title"].encode('utf-8'), x["state"], x["created_at"], first_update, first_comment, x["closed_at"], time_to_update, update_type, time_to_comment, time_to_close, x["url"]])






    