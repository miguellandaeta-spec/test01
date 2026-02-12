"""Jira Data Puller

Improved, robust version with typing, logging and CLI options.
"""

from __future__ import annotations

import json
import csv
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
import argparse
import os

from dotenv import load_dotenv
from jira import JIRA


logger = logging.getLogger(__name__)


def load_config() -> Dict[str, str]:
    load_dotenv()

    server = os.getenv('JIRA_SERVER')
    username = os.getenv('JIRA_USERNAME')
    api_token = os.getenv('JIRA_API_TOKEN')

    if not (server and username and api_token):
        missing = [k for k, v in (
            ('JIRA_SERVER', server),
            ('JIRA_USERNAME', username),
            ('JIRA_API_TOKEN', api_token),
        ) if not v]
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return {'server': server, 'username': username, 'api_token': api_token}


def connect_to_jira(config: Dict[str, str]) -> JIRA:
    try:
        jira = JIRA(server=config['server'], basic_auth=(config['username'], config['api_token']))
        return jira
    except Exception as exc:
        raise ConnectionError(f"Failed to connect to Jira: {exc}") from exc


def fetch_all_issues(jira: JIRA, jql_query: str = 'ORDER BY created DESC', max_results: int = 100) -> List[Any]:
    start_at = 0
    all_issues: List[Any] = []

    while True:
        logger.debug('Requesting issues start_at=%d max_results=%d', start_at, max_results)
        try:
            issues = jira.search_issues(jql_query, startAt=start_at, maxResults=max_results)
        except Exception as exc:
            logger.error('Error fetching issues: %s', exc)
            break

        if not issues:
            break

        all_issues.extend(issues)
        fetched = len(issues)
        logger.info('Fetched %d issues (total %d)', fetched, len(all_issues))

        if fetched < max_results:
            break

        start_at += fetched

    return all_issues


def _safe(field: Any) -> Optional[Any]:
    return None if field is None else field


def serialize_issue(issue: Any) -> Dict[str, Any]:
    f = issue.fields
    return {
        'key': getattr(issue, 'key', None),
        'summary': _safe(getattr(f, 'summary', None)),
        'description': _safe(getattr(f, 'description', None)),
        'status': getattr(f.status, 'name', None) if getattr(f, 'status', None) else None,
        'priority': getattr(f.priority, 'name', None) if getattr(f, 'priority', None) else None,
        'assignee': getattr(f.assignee, 'displayName', None) if getattr(f, 'assignee', None) else None,
        'created': _safe(getattr(f, 'created', None)),
        'updated': _safe(getattr(f, 'updated', None)),
        'issue_type': getattr(f.issuetype, 'name', None) if getattr(f, 'issuetype', None) else None,
        'project': getattr(f.project, 'key', None) if getattr(f, 'project', None) else None,
    }


def save_issues_json(issues: List[Any], output_file: Path) -> None:
    serialized = [serialize_issue(i) for i in issues]
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open('w', encoding='utf-8') as f:
        json.dump(serialized, f, indent=2, ensure_ascii=False)
    logger.info('Saved %d issues to %s', len(issues), output_file)


def save_issues_csv(issues: List[Any], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ['key', 'summary', 'status', 'priority', 'assignee', 'created', 'updated', 'issue_type', 'project']
    with output_file.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for issue in issues:
            writer.writerow(serialize_issue(issue))

    logger.info('Saved %d issues to %s', len(issues), output_file)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Pull issues from Jira and save locally')
    parser.add_argument('--jql', default='ORDER BY created DESC', help='JQL query to select issues')
    parser.add_argument('--max-results', type=int, default=100, help='Page size for Jira requests')
    parser.add_argument('--out-dir', type=Path, default=Path('data'), help='Output directory')
    parser.add_argument('--json-file', default='jira_data.json', help='JSON filename')
    parser.add_argument('--csv-file', default='jira_data.csv', help='CSV filename')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable debug logging')
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format='%(levelname)s: %(message)s')

    try:
        config = load_config()
        jira = connect_to_jira(config)
        issues = fetch_all_issues(jira, jql_query=args.jql, max_results=args.max_results)

        if not issues:
            logger.info('No issues found for JQL: %s', args.jql)
            return 0

        out_dir = Path(args.out_dir)
        save_issues_json(issues, out_dir / args.json_file)
        save_issues_csv(issues, out_dir / args.csv_file)

    except Exception as exc:
        logger.exception('Unhandled error: %s', exc)
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
