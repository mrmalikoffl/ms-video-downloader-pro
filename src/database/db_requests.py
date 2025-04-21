import sqlite3
from datetime import datetime, timedelta
from src.config import RATE_LIMIT_PER_HOUR
import logging

logger = logging.getLogger(__name__)

def record_request(user_id: int, platform: str):
    """Record a download request."""
    try:
        conn = sqlite3.connect("/app/downloads.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO requests (user_id, platform, timestamp) VALUES (?, ?, ?)",
            (user_id, platform, datetime.now())
        )
        conn.commit()
        logger.info(f"Recorded request for user {user_id} on platform {platform}")
    except sqlite3.Error as e:
        logger.error(f"Error recording request for user {user_id}: {e}")
        raise
    finally:
        conn.close()

def check_rate_limit(user_id: int) -> bool:
    """Check if the user is within the rate limit."""
    try:
        conn = sqlite3.connect("/app/downloads.db")
        c = conn.cursor()
        one_hour_ago = datetime.now() - timedelta(hours=1)
        c.execute(
            "SELECT COUNT(*) FROM requests WHERE user_id = ? AND timestamp > ?",
            (user_id, one_hour_ago)
        )
        count = c.fetchone()[0]
        return count < RATE_LIMIT_PER_HOUR
    except sqlite3.Error as e:
        logger.error(f"Error checking rate limit for user {user_id}: {e}")
        return False
    finally:
        conn.close()
