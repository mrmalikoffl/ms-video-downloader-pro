import sqlite3

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect("downloads.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            user_id INTEGER,
            platform TEXT,
            timestamp DATETIME
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS premium_users (
            user_id INTEGER PRIMARY KEY,
            expiration DATETIME
        )
    """)
    conn.commit()
    conn.close()