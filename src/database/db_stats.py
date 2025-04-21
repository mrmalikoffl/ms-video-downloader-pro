import logging
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

logger = logging.getLogger(__name__)

def get_mongo_collection(collection_name: str):
    """Connect to MongoDB and return the specified collection."""
    try:
        mongo_uri = os.getenv("MONGODB_URI")
        if not mongo_uri:
            raise ValueError("MONGODB_URI environment variable not set")
        client = MongoClient(mongo_uri)
        db = client["telegram_bot"]
        return db[collection_name]
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def get_stats(user_id: int = None) -> dict:
    """Get usage stats."""
    try:
        requests_collection = get_mongo_collection("requests")
        premium_collection = get_mongo_collection("premium_users")
        stats = {"total_downloads": 0, "requests_this_hour": 0}

        # Total downloads
        query = {"user_id": user_id} if user_id else {}
        stats["total_downloads"] = requests_collection.count_documents(query)

        # Platform-specific downloads
        platforms = ["youtube", "instagram", "twitter", "tiktok", "x"]
        for platform in platforms:
            platform_query = {"platform": platform}
            if user_id:
                platform_query["user_id"] = user_id
            stats[platform] = requests_collection.count_documents(platform_query)

        # Requests this hour (user-specific)
        if user_id:
            one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S.%f")
            stats["requests_this_hour"] = requests_collection.count_documents({
                "user_id": user_id,
                "timestamp": {"$gt": one_hour_ago}
            })

        # Premium users (bot-wide)
        if not user_id:
            current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
            stats["premium_users"] = premium_collection.count_documents({
                "expiration": {"$gt": current_time}
            })

        return stats
    except OperationFailure as e:
        logger.error(f"Error fetching stats for user {user_id}: {e}")
        return {"total_downloads": 0, "requests_this_hour": 0}

def get_users_list() -> list:
    """Get list of all users."""
    try:
        collection = get_mongo_collection("requests")
        users = collection.distinct("user_id")
        return users
    except OperationFailure as e:
        logger.error(f"Error fetching users list: {e}")
        return []
