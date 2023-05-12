import csv
import json
import glob
import os
from dateutil import parser

def calculate_time_difference(start_time, end_time):
    time_difference = ''
    if end_time:
        time_difference = (parser.isoparse(end_time) - parser.isoparse(start_time)).days
    return time_difference

if __name__ == '__main__':
    csv_file = csv.writer(open("data/sla.csv", "w", newline=''))
    csv_file.writerow(['id', 'title','state','created','first_event', 'first_comment', 'closed', 'time_to_event', 'event_type', 'time_to_comment', 'time_to_close', 'url'])

    issue_files = sorted(glob.glob('data/issues-*.json'))
    for issue_file in issue_files:
        with open(issue_file, encoding="utf8") as f:
            issue_data = json.load(f)

        for issue in issue_data:
            if "pull_request" in issue:
                continue

            try:
                id = issue["number"]
                print(f'Issue: {id}')

                created = issue["created_at"]
                closed = issue["closed_at"]
                time_to_close = calculate_time_difference(created, closed)

                events_file = f'data/events-{id}.json'
                first_event = ''
                time_to_event = ''
                event_type = ''
                if os.path.exists(events_file):
                    with open(events_file, encoding="utf8") as g:
                        events_data = json.load(g)

                        for event in events_data:
                            current_event_type = event["event"]
                            current_event_time = event["created_at"]
                            if not first_event or current_event_time < first_event:
                                first_event = current_event_time
                                event_type = current_event_type

                    if first_event:
                        time_to_event = calculate_time_difference(created, first_event)

                comments_file = f'data/comments-{id}.json'
                first_comment = ''
                time_to_comment = ''
                if os.path.exists(comments_file):
                    with open(comments_file, encoding="utf8") as h:
                        comments_data = json.load(h)

                        for comment in comments_data:
                            comment_time = comment["created_at"]
                            if not first_comment or comment_time < first_comment:
                                first_comment = comment_time

                    if first_comment:
                        time_to_comment = calculate_time_difference(created, first_comment)

                csv_file.writerow([id, issue["title"].encode('utf-8'), issue["state"], created, first_event, first_comment, closed, time_to_event, event_type, time_to_comment, time_to_close, issue["url"]])

            except KeyError:
                print("No number found")