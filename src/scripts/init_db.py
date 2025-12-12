#!/usr/bin/env python3
"""
Database initialization script.
Creates necessary collections and indexes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.db.mongo import mongo_manager
from src.models.organization import OrganizationModel
from src.models.admin_user import AdminUserModel
from src.utils.logger import logger

def initialize_database():
    """Initialize database with required collections and indexes"""
    try:
        logger.info("Starting database initialization...")
        
        # Get master database
        master_db = mongo_manager.get_master_db()
        
        # Create collections if they don't exist
        collections_to_create = ["organizations", "admin_users"]
        existing_collections = master_db.list_collection_names()
        
        for collection in collections_to_create:
            if collection not in existing_collections:
                master_db.create_collection(collection)
                logger.info(f"Created collection: {collection}")
        
        # Create indexes
        OrganizationModel.create_indexes()
        AdminUserModel.create_indexes()
        
        logger.info("✅ Database initialization completed successfully")
        
        # Print collection info
        collections = master_db.list_collection_names()
        logger.info(f"Available collections: {collections}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False

def create_sample_data():
    """Create sample organization for testing"""
    try:
        from src.services.organization_service import OrganizationService
        from datetime import datetime
        
        sample_org = {
            "organization_name": "SampleOrganization",
            "email": "admin@sample.org",
            "password": "SamplePass123"
        }
        
        # Check if sample already exists
        master_db = mongo_manager.get_master_db()
        existing = master_db.organizations.find_one(
            {"organization_name": "SampleOrganization"}
        )
        
        if not existing:
            result = OrganizationService.create_organization(sample_org)
            logger.info(f"✅ Created sample organization: {result}")
        else:
            logger.info("ℹ Sample organization already exists")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to create sample data: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Organization Management Service - Database Initialization")
    print("=" * 60)
    
    if initialize_database():
        print("\nWould you like to create sample data? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice == 'y':
            create_sample_data()
        
        print("\n✅ Database setup completed!")
        print("\nYou can now start the application with:")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("\nAccess the API documentation at:")
        print("  http://localhost:8000/docs")
    else:
        print("\n❌ Database initialization failed!")
        sys.exit(1)