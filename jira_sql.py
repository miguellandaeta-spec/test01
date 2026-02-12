"""Simple SQLite storage for Jira issues.

This module provides a helper to persist serialized issues into a local
SQLite database. It's intentionally lightweight and uses a single table with
columns matching the serialized issue fields.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Mapping, Any


def _ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS issues (
            key TEXT PRIMARY KEY,
            summary TEXT,
            description TEXT,
            status TEXT,
            priority TEXT,
            assignee TEXT,
            created TEXT,
            updated TEXT,
            issue_type TEXT,
            project TEXT
        )
        '''
    )


def save_issues_sqlite(issues: Iterable[Mapping[str, Any]], db_path: Path) -> int:
    """Save serialized issues (dict-like) to SQLite DB.

    Args:
        issues: iterable of dict-like serialized issues
        db_path: path to sqlite database file

    Returns:
        Number of rows inserted/updated
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    try:
        _ensure_table(conn)
        rows = 0
        cur = conn.cursor()
        for issue in issues:
            cur.execute(
                '''
                INSERT OR REPLACE INTO issues
                (key, summary, description, status, priority, assignee, created, updated, issue_type, project)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    issue.get('key'),
                    issue.get('summary'),
                    issue.get('description'),
                    issue.get('status'),
                    issue.get('priority'),
                    issue.get('assignee'),
                    issue.get('created'),
                    issue.get('updated'),
                    issue.get('issue_type'),
                    issue.get('project'),
                ),
            )
            rows += 1

        conn.commit()
        return rows
    finally:
        conn.close()
