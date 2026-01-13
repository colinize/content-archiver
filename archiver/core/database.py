"""SQLite database for tracking downloads and enabling resume."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, asdict

from .config import DATABASE_FILE, ensure_dirs


@dataclass
class Download:
    """Represents a download record."""
    id: Optional[int]
    url: str
    content_type: str  # youtube, podcast, forum, article, site
    source_name: str   # Channel name, podcast name, etc.
    title: str
    status: str        # pending, downloading, complete, error
    local_path: Optional[str]
    file_size: Optional[int]
    downloaded_bytes: int
    created_at: str
    updated_at: str
    error_message: Optional[str]
    metadata: Optional[str]  # JSON string


class Database:
    """Database manager for download tracking."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DATABASE_FILE
        ensure_dirs()
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    source_name TEXT,
                    title TEXT,
                    status TEXT DEFAULT 'pending',
                    local_path TEXT,
                    file_size INTEGER,
                    downloaded_bytes INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    error_message TEXT,
                    metadata TEXT,
                    UNIQUE(url, title)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_status ON downloads(status)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_type ON downloads(content_type)
            """)
            conn.commit()

    def add_download(
        self,
        url: str,
        content_type: str,
        source_name: str,
        title: str,
        metadata: Optional[dict] = None
    ) -> int:
        """Add a new download record. Returns the record ID."""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT OR REPLACE INTO downloads
                (url, content_type, source_name, title, status, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, 'pending', ?, ?, ?)
            """, (url, content_type, source_name, title, now, now,
                  json.dumps(metadata) if metadata else None))
            conn.commit()
            return cursor.lastrowid

    def update_status(
        self,
        download_id: int,
        status: str,
        local_path: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> None:
        """Update the status of a download."""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE downloads
                SET status = ?, local_path = ?, error_message = ?, updated_at = ?
                WHERE id = ?
            """, (status, local_path, error_message, now, download_id))
            conn.commit()

    def update_progress(self, download_id: int, downloaded_bytes: int) -> None:
        """Update download progress."""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE downloads
                SET downloaded_bytes = ?, updated_at = ?
                WHERE id = ?
            """, (downloaded_bytes, now, download_id))
            conn.commit()

    def get_pending(self) -> list[Download]:
        """Get all pending/incomplete downloads."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM downloads
                WHERE status IN ('pending', 'downloading', 'error')
                ORDER BY created_at DESC
            """).fetchall()
            return [Download(**dict(row)) for row in rows]

    def get_all(self, limit: int = 50) -> list[Download]:
        """Get recent downloads."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM downloads
                ORDER BY updated_at DESC
                LIMIT ?
            """, (limit,)).fetchall()
            return [Download(**dict(row)) for row in rows]

    def get_by_url(self, url: str) -> list[Download]:
        """Get downloads by URL."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM downloads WHERE url = ?
            """, (url,)).fetchall()
            return [Download(**dict(row)) for row in rows]

    def get_stats(self) -> dict[str, Any]:
        """Get download statistics."""
        with sqlite3.connect(self.db_path) as conn:
            stats = {}
            # Total counts by status
            rows = conn.execute("""
                SELECT status, COUNT(*) as count FROM downloads GROUP BY status
            """).fetchall()
            stats["by_status"] = {row[0]: row[1] for row in rows}

            # Total counts by type
            rows = conn.execute("""
                SELECT content_type, COUNT(*) as count FROM downloads GROUP BY content_type
            """).fetchall()
            stats["by_type"] = {row[0]: row[1] for row in rows}

            # Total count
            total = conn.execute("SELECT COUNT(*) FROM downloads").fetchone()[0]
            stats["total"] = total

            return stats
