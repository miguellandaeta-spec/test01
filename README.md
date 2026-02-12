# Jira Data Puller

A Python script to pull all data from Jira and save it to a JSON file.

## Features

- Fetches all issues from Jira using JQL queries
- Supports pagination to handle large datasets
- Saves issue data to a JSON file
- Configurable via environment variables

## Requirements

- Python 3.7+
- Jira account with API token

## Installation

1. Clone or navigate to this repository:
   ```bash
   cd test01
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   ````markdown
   # Jira Data Puller

   Improved script to pull Jira issues and save them as JSON and CSV.

   ## Highlights

   - Adds a small CLI for JQL, page size, and output location
   - Robust pagination and safer serialization for missing fields
   - JSON and CSV outputs written to a configurable `--out-dir`

   ## Requirements

   - Python 3.8+ recommended
   - Jira account with API token
   - Install dependencies:

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

   ## Configuration

   Create a `.env` file in the repository root (copy from `.env.example` if present) and set:

   - `JIRA_SERVER` — your Jira base URL (e.g. https://yourcompany.atlassian.net)
   - `JIRA_USERNAME` — your account email or username
   - `JIRA_API_TOKEN` — an API token from your Atlassian account

   ## Usage

   Run `jira_puller.py` with optional flags:

   ```bash
   python jira_puller.py [--jql "ORDER BY created DESC"] [--max-results 100] [--out-dir data] [--json-file jira_data.json] [--csv-file jira_data.csv] [-v]
   ```

   Examples:

   - Default run (writes to `data/jira_data.json` and `data/jira_data.csv`):

   ```bash
   python jira_puller.py
   ```

   - Fetch a single project and increase verbosity:

   ```bash
   python jira_puller.py --jql "project = MYPROJECT ORDER BY created DESC" --max-results 200 -v
   ```

   ## Output

   By default the script writes both JSON and CSV outputs into the directory passed via `--out-dir` (default `data`).

   - JSON (`jira_data.json`): complete issue details (key, summary, description, status, priority, assignee, created, updated, issue_type, project)
   - CSV (`jira_data.csv`): flattened view containing the same logical fields as columns for easy import into spreadsheets

   ## Customization

   You can change the default JQL, page size, and output paths via CLI flags. For quick changes inside the code, the `fetch_all_issues` call in `main()` accepts a `jql_query` and `max_results`.

   ## Troubleshooting

   - Connection errors: verify `JIRA_SERVER`, `JIRA_USERNAME`, and `JIRA_API_TOKEN` in your environment
   - No issues returned: validate your JQL and account permissions

   ````
