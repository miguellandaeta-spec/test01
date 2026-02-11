"""
Jira Data Puller
Script to pull all data from Jira and save it locally.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA


def load_config():
    """Load Jira configuration from environment variables."""
    load_dotenv()
    
    config = {
        'server': os.getenv('JIRA_SERVER'),
        'username': os.getenv('JIRA_USERNAME'),
        'api_token': os.getenv('JIRA_API_TOKEN'),
    }
    
    # Validate required configuration
    if not all(config.values()):
        raise ValueError(
            "Missing required environment variables: "
            "JIRA_SERVER, JIRA_USERNAME, JIRA_API_TOKEN"
        )
    
    return config


def connect_to_jira(config):
    """Establish connection to Jira server."""
    try:
        jira = JIRA(
            server=config['server'],
            basic_auth=(config['username'], config['api_token'])
        )
        return jira
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Jira: {e}")


def fetch_all_issues(jira, jql_query="ORDER BY created DESC"):
    """
    Fetch all issues from Jira using JQL query.
    
    Args:
        jira: JIRA connection object
        jql_query: JQL query string (optional)
    
    Returns:
        List of issues
    """
    max_results = 50
    start_at = 0
    all_issues = []
    
    while True:
        try:
            issues = jira.search_issues(
                jql_query,
                startAt=start_at,
                maxResults=max_results
            )
            
            if not issues:
                break
            
            all_issues.extend(issues)
            start_at += max_results
            print(f"Fetched {len(all_issues)} issues so far...")
            
        except Exception as e:
            print(f"Error fetching issues: {e}")
            break
    
    return all_issues


def serialize_issue(issue):
    """Convert Jira issue to JSON-serializable dictionary."""
    return {
        'key': issue.key,
        'summary': issue.fields.summary,
        'description': issue.fields.description,
        'status': issue.fields.status.name,
        'priority': issue.fields.priority.name if issue.fields.priority else None,
        'assignee': issue.fields.assignee.name if issue.fields.assignee else None,
        'created': str(issue.fields.created),
        'updated': str(issue.fields.updated),
        'issue_type': issue.fields.issuetype.name,
        'project': issue.fields.project.key,
    }


def save_issues(issues, output_file='jira_data.json'):
    """Save issues to JSON file."""
    try:
        serialized_issues = [serialize_issue(issue) for issue in issues]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serialized_issues, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully saved {len(issues)} issues to {output_file}")
        
    except Exception as e:
        print(f"Error saving issues: {e}")


def main():
    """Main function to pull Jira data."""
    try:
        print("Loading configuration...")
        config = load_config()
        
        print("Connecting to Jira...")
        jira = connect_to_jira(config)
        
        print("Fetching all issues...")
        issues = fetch_all_issues(jira)
        
        print(f"Total issues fetched: {len(issues)}")
        
        if issues:
            print("Saving data...")
            save_issues(issues)
            print("Done!")
        else:
            print("No issues found.")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
