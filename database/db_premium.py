import sqlite3
from datetime import datetime, timedelta

def is_premium_user(user_id: int) -> bool:
    """Check if the user has an active premium subscription."""
    conn = sqlite3.connect("downloads.db")
    c = conn.cursor()
    c.execute(
        "SELECT expiration FROM premium_users WHERE user_id = ?",
        (user_id,)
    )
    result = c.fetchone()
    conn.close()
    if result and result[0]:
        expiration = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
        return expiration > datetime.now()
    return False

def grant_premium(user_id: int, days: int):
    """Grant premium status."""
    expiration = datetime.now() + timedelta(days=days)
    conn = sqlite3.connect("downloads.db")
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO premium_users (user_id, expiration) VALUES (?, ?)",
        (user_id, expiration)
    )
    conn.commit()
    conn.close()

def revoke_premium(user_id: int):
    """Revoke premium status."""
    conn = sqlite3.connect("downloads.db")
    c = conn.cursor()
    c.execute(
        "DELETE FROM premium_users WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()

def get_premium_users_list() -> list:
    """Get list of premium users."""
    conn = sqlite3.connect("downloads.db")
    c = conn.cursor()
    c.execute(
        "SELECT user_id, expiration FROM premium_users WHERE expiration > ?",
        (datetime.now(),)
    )
    users = c.fetchall()
    conn.close()
    return users