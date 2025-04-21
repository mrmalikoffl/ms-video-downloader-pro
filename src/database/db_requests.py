import logging
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ConnectionError, OperationFailure
from src.config import RATE_LIMIT_PER_HOUR

logger = logging.getLogger(__name__)

def get_mongo_collection():
    """Connect to MongoDB and return the requests collection."""
    try:
        mongo_uri = os.getenv("MONGODB_URI")
        if not mongo_uri:
            raise ValueError("MONGODB_URI environment variable not set")
        client = MongoClient(mongo_uri)
        db = client["telegram_bot"]
        collection = db["requests"]
        collection.create_index("user_id")  # Index for faster queries
        return collection
    except ConnectionError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def record_request(user_id: int, platform: str):
    """Record a download request."""
    try:
        collection = get_mongo_collection()
        request = {
            "user_id": user_id,
            "platform": platform,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        }
        collection.insert_one(request)
        logger.info(f"Recorded request for user {user_id} on platform {platform}")
    except OperationFailure as e:
        logger.error(f"Error recording request for user {user_id}: {e}")
        raise

def check_rate_limit(user_id: int) -> bool:
    """Check if the user is within the rate limit."""
    try:
        collection = get_mongo_collection()
        one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S.%f")
        count = collection.count_documents({
            "user_id": user_id,
            "timestamp": {"$gt": one_hour_ago}
        })
        return count < RATE_LIMIT_PER_HOUR
    except OperationFailure as e:
        logger.error(f"Error checking rate limit for user {user_id}: {e}")
        return False
