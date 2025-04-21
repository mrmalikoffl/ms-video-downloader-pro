import sqlite3
import json
import logging

logger = logging.getLogger(__name__)

def export_sqlite_to_json():
    try:
        conn = sqlite3.connect("/app/downloads.db")
        cursor = conn.cursor()

        # Export premium_users
        cursor.execute("SELECT user_id, expiration FROM premium_users")
        premium_rows = cursor.fetchall()
        premium_data = [{"user_id": row[0], "expiration": row[1]} for row in premium_rows]
        with open("premium_users.json", "w") as f:
            json.dump(premium_data, f, indent=4)
        logger.info("Exported premium_users to premium_users.json")

        # Export requests
        cursor.execute("SELECT user_id, platform, timestamp FROM requests")
        request_rows = cursor.fetchall()
        request_data = [
            {"user_id": row[0], "platform": row[1], "timestamp": row[2]}
            for row in request_rows
        ]
        with open("requests.json", "w") as f:
            json.dump(request_data, f, indent=4)
        logger.info("Exported requests to requests.json")

    except sqlite3.Error as e:
        logger.error(f"Error exporting SQLite data: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    export_sqlite_to_json()
