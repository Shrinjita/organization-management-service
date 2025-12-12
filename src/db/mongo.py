from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBManager:
    _client = None
    _master_db = None
    
    @classmethod
    def get_client(cls):
        """Get or create MongoDB client"""
        if cls._client is None:
            try:
                cls._client = MongoClient(
                    settings.mongodb_uri,
                    serverSelectionTimeoutMS=5000,
                    maxPoolSize=50
                )
                # Test connection
                cls._client.admin.command('ping')
                logger.info("✅ MongoDB connected successfully")
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                logger.error(f"❌ MongoDB connection failed: {e}")
                raise
        return cls._client
    
    @classmethod
    def get_master_db(cls):
        """Get master database"""
        if cls._master_db is None:
            client = cls.get_client()
            cls._master_db = client[settings.master_db_name]
        return cls._master_db
    
    @classmethod
    def get_database(cls, db_name: str):
        """Get specific database by name"""
        client = cls.get_client()
        return client[db_name]
    
    @classmethod
    def get_organization_collection(cls, org_name: str):
        """Get or create organization-specific collection"""
        master_db = cls.get_master_db()
        
        # Get organization metadata
        org_data = master_db.organizations.find_one({"organization_name": org_name})
        if not org_data:
            raise ValueError(f"Organization '{org_name}' not found")
        
        # Use master database for all collections (simplified architecture)
        # In production, you might want separate databases
        collection_name = f"org_{org_name.lower().replace(' ', '_')}"
        return master_db[collection_name]
    
    @classmethod
    def close_connection(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._master_db = None
            logger.info("MongoDB connection closed")

# Global instance
mongo_manager = MongoDBManager()