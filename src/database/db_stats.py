import sqlite3
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def get_stats(user_id: int = None) -> dict:
    """Get usage stats."""
    try:
        conn = sqlite3.connect("/app/downloads.db")
        c = conn.cursor()
        
        # Total downloads
        query = "SELECT COUNT(*) FROM requests"
        if user_id:
            query += " WHERE user_id = ?"
            c.execute(query, (user_id,) if user_id else ())
        else:
            c.execute(query)
        total_downloads = c.fetchone()[0]
        
        # Platform-specific downloads
        platforms = ["youtube", "instagram", "twitter"]
        stats = {"total_downloads": total_downloads, "requests_this_hour": 0}
        for platform in platforms:
            query = f"SELECT COUNT(*) FROM requests WHERE platform = ?"
            if user_id:
                query += " AND user_id = ?"
                c.execute(query, (platform, user_id) if user_id else (platform,))
            else:
                c.execute(query, (platform,))
            stats[platform] = c.fetchone()[0]
        
        # Requests this hour (user-specific)
        if user_id:
            one_hour_ago = datetime.now() - timedelta(hours=1)
            c.execute(
                "SELECT COUNT(*) FROM requests WHERE user_id = ? AND timestamp > ?",
                (user_id, one_hour_ago)
            )
            stats["requests_this_hour"] = c.fetchone()[0]
        
        # Premium users (bot-wide)
        if not user_id:
            c.execute(
                "SELECT COUNT(*) FROM premium_users WHERE expiration > ?",
                (datetime.now(),)
            )
            stats["premium_users"] = c.fetchone()[0]
        
        return stats
    except sqlite3.Error as e:
        logger.error(f"Error fetching stats for user {user_id}: {e}")
        return {"total_downloads": 0, "requests_this_hour": 0}
    finally:
        conn.close()

def get_users_list() -> list:
    """Get list of all users."""
    try:
        conn = sqlite3.connect("/app/downloads.db")
        c = conn.cursor()
        c.execute("SELECT DISTINCT user_id FROM requests")
        users = [row[0] for row in c.fetchall()]
        return users
    except sqlite3.Error as e:
        logger.error(f"Error fetching users list: {e}")
        return []
    finally:
        conn.close()
