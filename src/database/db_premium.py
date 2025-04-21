import logging
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

logger = logging.getLogger(__name__)

def get_mongo_collection():
    """Connect to MongoDB and return the premium_users collection."""
    try:
        mongo_uri = os.getenv("MONGODB_URI")
        if not mongo_uri:
            raise ValueError("MONGODB_URI environment variable not set")
        client = MongoClient(mongo_uri)
        db = client["telegram_bot"]
        collection = db["premium_users"]
        collection.create_index("user_id", unique=True)
        return collection
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def is_premium_user(user_id: int) -> bool:
    """Check if the user has an active premium subscription."""
    try:
        collection = get_mongo_collection()
        user = collection.find_one({"user_id": user_id})
        if user and "expiration" in user:
            expiration = datetime.strptime(user["expiration"], "%Y-%m-%d %H:%M:%S.%f")
            return expiration > datetime.utcnow()
        return False
    except OperationFailure as e:
        logger.error(f"Error checking premium status for user {user_id}: {e}")
        return False

def grant_premium(user_id: int, days: int) -> str:
    """Grant premium status and return the expiration date."""
    try:
        expiration = datetime.utcnow() + timedelta(days=days)
        expiration_str = expiration.strftime("%Y-%m-%d %H:%M:%S.%f")
        collection = get_mongo_collection()
        collection.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id, "expiration": expiration_str}},
            upsert=True
        )
        logger.info(f"Granted premium status to user {user_id} until {expiration_str}")
        return expiration_str
    except OperationFailure as e:
        logger.error(f"Error granting premium status to user {user_id}: {e}")
        raise

def revoke_premium(user_id: int) -> bool:
    """Revoke premium status and return True if successful."""
    try:
        collection = get_mongo_collection()
        result = collection.delete_one({"user_id": user_id})
        if result.deleted_count > 0:
            logger.info(f"Revoked premium status for user {user_id}")
            return True
        logger.info(f"No premium status found for user {user_id} to revoke")
        return False
    except OperationFailure as e:
        logger.error(f"Error revoking premium status for user {user_id}: {e}")
        raise

def get_premium_users_list() -> list:
    """Get list of premium users with active subscriptions."""
    try:
        collection = get_mongo_collection()
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        users = collection.find({"expiration": {"$gt": current_time}})
        return [(user["user_id"], user["expiration"]) for user in users]
    except OperationFailure as e:
        logger.error(f"Error fetching premium users list: {e}")
        return []
