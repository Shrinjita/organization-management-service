import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class MongoManager:
    _client: Optional[MongoClient] = None
    _db = None
    
    @classmethod
    def get_client(cls) -> MongoClient:
        """Get MongoDB client, creating it if it doesn't exist"""
        if cls._client is None:
            # CRITICAL: Get URI from environment variable
            mongodb_uri = os.getenv(
                "MONGODB_URI", 
                "mongodb://localhost:27017/organization_db"  # Fallback for local development
            )
            
            # Log which URI we're using (hide password)
            safe_uri = mongodb_uri
            if "@" in safe_uri:
                # Hide password in logs
                safe_uri = "mongodb+srv://username:****@" + safe_uri.split("@")[-1]
            logger.info(f"🔗 Connecting to MongoDB: {safe_uri}")
            
            try:
                # Connect with timeout
                cls._client = MongoClient(
                    mongodb_uri,
                    serverSelectionTimeoutMS=10000,  # 10 second timeout
                    connectTimeoutMS=10000,
                    socketTimeoutMS=30000
                )
                
                # Test the connection
                cls._client.admin.command('ping')
                logger.info("✅ MongoDB connection successful")
                
            except ConnectionFailure as e:
                logger.error(f"❌ MongoDB connection failed: {e}")
                raise
            
            # Set database
            db_name = os.getenv("DATABASE_NAME", "organization_db")
            cls._db = cls._client[db_name]
            
        return cls._client
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls._db is None:
            cls.get_client()  # Ensure client is initialized
        return cls._db
    
    @classmethod
    def close_connection(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("🔌 MongoDB connection closed")

mongo_manager = MongoManager()