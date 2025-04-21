import sqlite3
import logging

logger = logging.getLogger(__name__)

def init_db():
    """Initialize the SQLite database."""
    try:
        conn = sqlite3.connect("/app/downloads.db")
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
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    finally:
        conn.close()
