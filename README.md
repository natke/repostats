# ONNX Runtime website data

This project pulls issue and pull request data from GitHub using the GitHub API and decorates it with response time data.

## Setup

To set up the project, create a Personal Access Token in GitHub, set the starting page for issues and PRs, and install the dependencies. 

```bash
export GITHUB_TOKEN=<value of personal access token>
export GITHUB_URL=microsoft/onnxruntime
export GITHUB_ISSUE_START_PAGE=109
export GITHUB_PR_START_PAGE=3
pip install -r requirements.txt
```

GitHub rate-limits API calls to about 50 calls of pages containing 100 items, so historical data is preserved in this repo. If old PRs or issues have been updated, then the query may need to be run over the old data anyway.

## Pull the data from GitHub

### Issues
To get all issues from the specified GitHub repo, run:

```bash
python get_issues.py
```

The output is stored in data/issues-<page>.json.

### Events
To get all events associated with each issue, run:

```bash
python get_issues_events.py
```

The output is stored in data/event-<issue>.json.

### CommentsTo get all comments associated with each issue, run:

```bash
python get_issues_comments.py
```

The output is stored in data/comment-<issue>.json.

### Docs PR data
To get all pull requests against the gh-pages branch from the ONNX Runtime GitHub repo, run:

```bash
python get_prs.py
```

Gets all of the pull requests against the gh-pages branch from the onnxruntime GitHub repo

## Export and decorate

### SLA data for Issues
To export data/sla.csv, which contains first update, first comment, time to update, time to comment, time to close for each issue, run:


```bash
python extract_sla_data.py
```

### Docs issues
To filter issues that have the component:documentation label, calculate the time to close, in days, and export as data/issues.csv, run:

```bash
python convert_issues_to_csv.py
```

### Docs PRs
To calculate the time to close, in days, and export as CSV, run:


```bash
python convert_prs_to_csv.py
```

# Suggested Usage of SLA.csv file
The SLA.csv file provides a great way to discover trends in your project's responsiveness to issues. Here are some suggested ways to use the data for deeper insights, including the processing steps to get there:

Note: Convert the csv file to an .xlsx file to save the formulas. This data may also be graphed for visual analysis.

## Excel formulas
Created Timestamp: `=DATEVALUE(LEFT(D2,10))+TIMEVALUE(MID(D2,12,8))`

Excel Date: `=DATE(YEAR(T2),MONTH(T2),DAY(T2))`

Excel Month: `=YEAR(U2)&"-"&TEXT(MONTH(U2),"00")`

Unique ID: `=YEAR(U2)&"-"&TEXT(MONTH(U2),"00") -> Remove duplicates`

Average Time To Close Issues: `=AVERAGEIFS(K2:K1000, V2:V1000, "="&W2, K2:K1000, ">0")`

Average Time to Comment on Issues: `=AVERAGEIFS(J2:J1000, V2:V1000, "="&W2, J2:J1000, ">0")`

Uncommented Issues: `=COUNTBLANK(J2:JXXX)`

Unclosed: `=COUNTBLANK(K2:KXXX)`