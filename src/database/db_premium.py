import sqlite3
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def is_premium_user(user_id: int) -> bool:
    """Check if the user has an active premium subscription."""
    try:
        conn = sqlite3.connect("/app/downloads.db")
        c = conn.cursor()
        c.execute(
            "SELECT expiration FROM premium_users WHERE user_id = ?",
            (user_id,)
        )
        result = c.fetchone()
        if result and result[0]:
            expiration = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
            return expiration > datetime.now()
        return False
    except sqlite3.Error as e:
        logger.error(f"Error checking premium status for user {user_id}: {e}")
        return False
    finally:
        conn.close()

def grant_premium(user_id: int, days: int):
    """Grant premium status."""
    try:
        expiration = datetime.now() + timedelta(days=days)
        conn = sqlite3.connect("/app/downloads.db")
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO premium_users (user_id, expiration) VALUES (?, ?)",
            (user_id, expiration)
        )
        conn.commit()
        logger.info(f"Granted premium status to user {user_id} until {expiration}")
    except sqlite3.Error as e:
        logger.error(f"Error granting premium status to user {user_id}: {e}")
        raise
    finally:
        conn.close()

def revoke_premium(user_id: int):
    """Revoke premium status."""
    try:
        conn = sqlite3.connect("/app/downloads.db")
        c = conn.cursor()
        c.execute(
            "DELETE FROM premium_users WHERE user_id = ?",
            (user_id,)
        )
        conn.commit()
        logger.info(f"Revoked premium status for user {user_id}")
    except sqlite3.Error as e:
        logger.error(f"Error revoking premium status for user {user_id}: {e}")
        raise
    finally:
        conn.close()

def get_premium_users_list() -> list:
    """Get list of premium users."""
    try:
        conn = sqlite3.connect("/app/downloads.db")
        c = conn.cursor()
        c.execute(
            "SELECT user_id, expiration FROM premium_users WHERE expiration > ?",
            (datetime.now(),)
        )
        users = c.fetchall()
        return users
    except sqlite3.Error as e:
        logger.error(f"Error fetching premium users list: {e}")
        return []
    finally:
        conn.close()
