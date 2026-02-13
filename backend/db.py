import sqlite3
from pathlib import Path
from typing import Dict, List, Any

DB_PATH = Path(__file__).resolve().parent / "sentinel.db"

def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            url TEXT NOT NULL,
            final_url TEXT NOT NULL,
            score INTEGER NOT NULL,
            level TEXT NOT NULL,
            category TEXT NOT NULL,
            confidence REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_scan(row: Dict[str, Any]) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO scans (ts, url, final_url, score, level, category, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row["ts"], row["url"], row["final_url"],
        int(row["score"]), row["level"], row["category"], float(row["confidence"])
    ))
    conn.commit()
    conn.close()

def fetch_scans(limit: int = 200) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT ts, url, final_url, score, level, category, confidence
        FROM scans
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def delete_all() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM scans")
    conn.commit()
    conn.close()

