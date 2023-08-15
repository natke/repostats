# GitHub repo data

Pull issue and pull request data from GitHub using the GitHub API, and decorate it with response time data.

## Setup

Create a Personal Access Token in GitHub. GitHub rate-limits API calls to about 50 calls of pages containing 100 items. Authorizing with a token allows a greater query rate.

```bash
export GITHUB_TOKEN=<value of personal access token>
```

Install dependencies

```bash
pip install -r requirements.txt
```

## Pull the data from GitHub

### Issues

```bash
python get_issues.py [--org <github org or account>] --repo [<repository name>] [--start_page <n>] [--end_page <m>]
```

Gets all issues from the s[ecified] repo. Stores the output in `data/{org}-{repo}-issues-{page}.json`

### Events

```bash
python get_issues_events.py
```

For all of the issues fetched in the previous step, get all of the events (add label, assign, close etc) associated with each issue. Stores the output in `data/{org}-{repo}-event-{id}.json`.

### Comments

```bash
python get_issues_comments.py
```

For all of the issues fetched in the first step, get all of the comments associated with each issue. Stores the output in `data/{org}-{repo}-comment-{id}.json`.

## Export and decorate

### SLA data for Issues

```bash
python extract_sla_data.py
```

Exports `data/sla.csv`, which contains first update, first comment, time to update, time to comment, time to close for each issue.

### Usage of sla.csv file

The sla.csv file provides a great way to discover trends in your project's responsiveness to issues. Here are some suggested ways to use the data for deeper insights, including the processing steps to get there:

Note: Convert the csv file to an .xlsx file to save the formulas. This data may also be graphed for visual analysis.

#### Excel formulas

Created Timestamp: =DATEVALUE(LEFT(D2,10))+TIMEVALUE(MID(D2,12,8))

Excel Date: =DATE(YEAR(T2),MONTH(T2),DAY(T2))

Excel Month: =YEAR(U2)&"-"&TEXT(MONTH(U2),"00")

Unique ID: =YEAR(U2)&"-"&TEXT(MONTH(U2),"00") -> Remove duplicates

Average Time To Close Issues: =AVERAGEIFS(K2:K1000, V2:V1000, "="&W2, K2:K1000, ">0")

Average Time to Comment on Issues: =AVERAGEIFS(J2:J1000, V2:V1000, "="&W2, J2:J1000, ">0")

Uncommented Issues: =COUNTBLANK(J2:JXXX)

Unclosed: =COUNTBLANK(K2:KXXX)