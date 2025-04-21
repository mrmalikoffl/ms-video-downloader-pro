import logging
import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    """Provide a database connection using a context manager."""
    conn = sqlite3.connect("/app/downloads.db")
    try:
        yield conn
    finally:
        conn.close()

def is_premium_user(user_id: int) -> bool:
    """Check if the user has an active premium subscription."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT expiration FROM premium_users WHERE user_id = ?",
                (user_id,)
            )
            result = cursor.fetchone()
            if result and result[0]:
                expiration = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
                return expiration > datetime.utcnow()
            return False
    except sqlite3.Error as e:
        logger.error(f"Error checking premium status for user {user_id}: {e}")
        return False

def grant_premium(user_id: int, days: int) -> str:
    """Grant premium status and return the expiration date."""
    try:
        expiration = datetime.utcnow() + timedelta(days=days)
        expiration_str = expiration.strftime("%Y-%m-%d %H:%M:%S.%f")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO premium_users (user_id, expiration) VALUES (?, ?)",
                (user_id, expiration_str)
            )
            conn.commit()
            logger.info(f"Granted premium status to user {user_id} until {expiration_str}")
            return expiration_str
    except sqlite3.Error as e:
        logger.error(f"Error granting premium status to user {user_id}: {e}")
        raise

def revoke_premium(user_id: int) -> bool:
    """Revoke premium status and return True if successful."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM premium_users WHERE user_id = ?",
                (user_id,)
            )
            conn.commit()
            if cursor.rowcount > 0:
                logger.info(f"Revoked premium status for user {user_id}")
                return True
            logger.info(f"No premium status found for user {user_id} to revoke")
            return False
    except sqlite3.Error as e:
        logger.error(f"Error revoking premium status for user {user_id}: {e}")
        raise

def get_premium_users_list() -> list:
    """Get list of premium users with active subscriptions."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, expiration FROM premium_users WHERE expiration > ?",
                (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"),)
            )
            users = cursor.fetchall()
            return [(user_id, expiration) for user_id, expiration in users]
    except sqlite3.Error as e:
        logger.error(f"Error fetching premium users list: {e}")
        return []
