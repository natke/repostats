# ONNX Runtime website data

Pull issue and pull request data from GitHub using the GitHub API, and decaorate it with response time data.

## Setup

Create a Personal Access Token in GitHub. Set the starting page for issues and PRs. GitHub rate-limits API calls to about 50 calls of pages containing 100 items, so historical data is preserved in this repo. If old PRs or issues have been updated, then the query may need to be run over the old data anyway.

```bash
export GITHUB_TOKEN=<value of personal access token>
export GITHUB_ISSUE_START_PAGE=109
export GITHUB_PR_START_PAGE=3
```

Install dependencies

```bash
pip install -r requirements.txt
```

## Pull the data from GitHub

### Issues

```bash
python get_issues.py
```

Gets all issues from the onnxruntime GitHub repo. Stores the output in `data/issues-<page>.json`

### Events

```bash
python get_issues_events.py
```

For all of the issues fetched in the previous step, get all of the events (add label, assign, close etc) associated with each issue. Stores the output in `data/event-<issue>.json`.

### Comments

```bash
python get_issues_comments.py
```

For all of the issues fetched in the first step, get all of the comments associated with each issue. Stores the output in `data/comment-<issue>.json`.

### Docs PR data

```bash
python get_prs.py
```

Gets all of the pull requests against the gh-pages branch from the onnxruntime GitHub repo

## Export and decorate

### SLA data for Issues

```bash
python extract_sla_data.py
```

Exports `data/sla.csv`, which contains first update, first comment, time to update, time to comment, time to close for each issue.

### Docs issues

```bash
python filter_docs_issues.py
```

Filters issues that have the component:documentation label, and calculates the time to close, in days, and exports as `data/docs-issues.csv`.
Reads associated events and comments and figures out whether the issue is associated with a PR fix.


### Docs PRs

```bash
python convert_prs_to_csv.py
```

Calculates the time to close, in days, and exports as CSV.
