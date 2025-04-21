import sqlite3
from datetime import datetime, timedelta
from src.config import RATE_LIMIT_PER_HOUR

def record_request(user_id: int, platform: str):
    """Record a download request."""
    conn = sqlite3.connect("downloads.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO requests (user_id, platform, timestamp) VALUES (?, ?, ?)",
        (user_id, platform, datetime.now())
    )
    conn.commit()
    conn.close()

def check_rate_limit(user_id: int) -> bool:
    """Check if the user is within the rate limit."""
    conn = sqlite3.connect("downloads.db")
    c = conn.cursor()
    one_hour_ago = datetime.now() - timedelta(hours=1)
    c.execute(
        "SELECT COUNT(*) FROM requests WHERE user_id = ? AND timestamp > ?",
        (user_id, one_hour_ago)
    )
    count = c.fetchone()[0]
    conn.close()
    return count < RATE_LIMIT_PER_HOUR