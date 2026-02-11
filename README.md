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
   cp .env.example .env
   ```

2. Update `.env` with your Jira credentials:
   - `JIRA_SERVER`: Your Jira instance URL (e.g., https://yourcompany.atlassian.net)
   - `JIRA_USERNAME`: Your Jira username or email
   - `JIRA_API_TOKEN`: Your Jira API token (generate from Account Settings → Security)

## Usage

Run the script:
```bash
python jira_puller.py
```

The script will:
1. Connect to your Jira instance
2. Fetch all issues
3. Save the data to `jira_data.json`

## Output

The script generates two output files containing all issues:

### JSON File (jira_data.json)
Contains comprehensive issue details with the following fields:
- key: Issue key (e.g., PROJ-123)
- summary: Issue title
- description: Issue description
- status: Current status
- priority: Issue priority
- assignee: Person assigned to the issue
- created: Creation timestamp
- updated: Last update timestamp
- issue_type: Type of issue (Bug, Task, etc.)
- project: Project key

### CSV File (jira_data.csv)
Contains a simplified view with the following columns:
- key: Issue key
- summary: Issue title
- status: Current status

## Customization

To modify which issues are fetched, edit the JQL query in the `main()` function. Examples:

```python
# Fetch issues from a specific project
fetch_all_issues(jira, "project = MYPROJECT")

# Fetch open issues only
fetch_all_issues(jira, "status != Done")

# Fetch issues assigned to you
fetch_all_issues(jira, "assignee = currentUser()")
```

## Troubleshooting

- **Connection Error**: Verify your JIRA_SERVER URL and credentials
- **API Token Error**: Ensure your API token is valid and not expired
- **No Issues Found**: Check your JQL query or increase permissions on your Jira account
