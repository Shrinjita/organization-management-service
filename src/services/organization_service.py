from typing import Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from src.models.organization import OrganizationModel, OrganizationCreate
from src.models.admin_user import AdminUserModel, AdminUserCreate
from src.db.mongo import mongo_manager
from src.utils.password import hash_password
from src.utils.validators import sanitize_collection_name
from src.utils.logger import logger
from src.services.validation_service import ValidationService
from src.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationNotFoundError,
    UnauthorizedAccessError,
    ValidationError
)
import os

class OrganizationService:
    """Service for organization management"""
    
    @staticmethod
    async def create_organization(org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new organization"""
        try:
            # Validate input
            is_valid, error_message = ValidationService.validate_organization_create(org_data)
            if not is_valid:
                raise ValueError(error_message)
            
            # Sanitize input
            org_data = ValidationService.sanitize_input(org_data)
            # Check if organization already exists
            existing_org = OrganizationModel.find_by_name(org_data["organization_name"])
            if existing_org:
                raise ValueError(f"Organization '{org_data['organization_name']}' already exists")
            
            # Check if admin email already exists
            existing_admin = AdminUserModel.find_by_email(org_data["email"])
            if existing_admin:
                raise ValueError(f"Admin email '{org_data['email']}' already exists")
            
            # Generate collection name
            collection_name = f"org_{sanitize_collection_name(org_data['organization_name'])}"
            
            # Create admin user first
            admin_user_data = {
                "email": org_data["email"],
                "hashed_password": hash_password(org_data["password"]),
                "organization_name": org_data["organization_name"],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_active": True
            }
            
            admin_result = AdminUserModel.create(admin_user_data)
            admin_id = str(admin_result.inserted_id)
            
            # Create organization
            organization_data = {
                "organization_name": org_data["organization_name"],
                "collection_name": collection_name,
                "admin_email": org_data["email"],
                "admin_user_id": admin_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            org_result = OrganizationModel.create(organization_data)
            org_id = str(org_result.inserted_id)
            
            # Create organization-specific collection
            master_db = mongo_manager.get_master_db()
            org_collection = master_db[collection_name]
            
            # Initialize collection with basic schema
            org_collection.insert_one({
                "_id": ObjectId(),
                "org_id": org_id,
                "metadata": {
                    "created_at": datetime.utcnow(),
                    "schema_version": "1.0"
                },
                "data": {}
            })
            
            logger.info(f"Created organization '{org_data['organization_name']}' with collection '{collection_name}'")
            
            return {
                "id": org_id,
                "organization_name": org_data["organization_name"],
                "collection_name": collection_name,
                "admin_email": org_data["email"],
                "admin_id": admin_id,
                "created_at": organization_data["created_at"]
            }
            
        except Exception as e:
            logger.error(f"Error creating organization: {str(e)}")
            raise
    
    @staticmethod
    async def get_organization(organization_name: str) -> Optional[Dict[str, Any]]:
        """Get organization by name"""
        try:
            org_data = OrganizationModel.find_by_name(organization_name)
            if not org_data:
                return None
            
            # Convert ObjectId to string
            org_data["id"] = str(org_data["_id"])
            del org_data["_id"]
            
            return org_data
            
        except Exception as e:
            logger.error(f"Error fetching organization: {str(e)}")
            raise
    
    @staticmethod
    async def update_organization(update_data: Dict[str, Any], current_admin_email: str) -> Dict[str, Any]:
        """Update organization details"""
        try:
            org_name = update_data["organization_name"]
            
            # Verify current admin owns the organization
            org_data = OrganizationModel.find_by_name(org_name)
            if not org_data:
                raise ValueError(f"Organization '{org_name}' not found")
            
            if org_data["admin_email"] != current_admin_email:
                raise ValueError("Unauthorized: Admin does not own this organization")
            
            updates = {}
            
            # Check if new organization name is provided and unique
            new_name = update_data.get("new_organization_name")
            if new_name and new_name != org_name:
                existing = OrganizationModel.find_by_name(new_name)
                if existing:
                    raise ValueError(f"Organization name '{new_name}' already exists")
                
                # Generate new collection name
                new_collection_name = f"org_{sanitize_collection_name(new_name)}"
                
                # Check if collection name is unique
                master_db = mongo_manager.get_master_db()
                if new_collection_name in master_db.list_collection_names():
                    raise ValueError(f"Collection name '{new_collection_name}' already exists")
                
                # Rename collection
                old_collection_name = org_data["collection_name"]
                master_db[old_collection_name].rename(new_collection_name)
                
                updates["organization_name"] = new_name
                updates["collection_name"] = new_collection_name
            
            # Update admin email if provided
            new_email = update_data.get("email")
            if new_email and new_email != org_data["admin_email"]:
                existing_admin = AdminUserModel.find_by_email(new_email)
                if existing_admin:
                    raise ValueError(f"Email '{new_email}' already in use")
                
                # Update admin user email
                AdminUserModel.update(org_data["admin_user_id"], {"email": new_email})
                updates["admin_email"] = new_email
            
            # Update admin password if provided
            new_password = update_data.get("password")
            if new_password:
                AdminUserModel.update(org_data["admin_user_id"], {
                    "hashed_password": hash_password(new_password)
                })
            
            if updates:
                updates["updated_at"] = datetime.utcnow()
                OrganizationModel.update(org_name, updates)
            
            return {"message": "Organization updated successfully", **updates}
            
        except Exception as e:
            logger.error(f"Error updating organization: {str(e)}")
            raise
    
    @staticmethod
    async def delete_organization(organization_name: str, admin_email: str) -> Dict[str, Any]:
        """Delete organization and its collection"""
        try:
            # Verify organization exists
            org_data = OrganizationModel.find_by_name(organization_name)
            if not org_data:
                raise ValueError(f"Organization '{organization_name}' not found")
            
            # Verify admin owns the organization
            if org_data["admin_email"] != admin_email:
                raise ValueError("Unauthorized: Admin does not own this organization")
            
            master_db = mongo_manager.get_master_db()
            
            # Delete organization collection
            collection_name = org_data["collection_name"]
            if collection_name in master_db.list_collection_names():
                master_db[collection_name].drop()
                logger.info(f"Dropped collection '{collection_name}'")
            
            # Delete admin user
            AdminUserModel.delete(org_data["admin_user_id"])
            
            # Delete organization record
            OrganizationModel.delete(organization_name)
            
            logger.info(f"Deleted organization '{organization_name}' and all associated data")
            
            return {"message": f"Organization '{organization_name}' deleted successfully"}
            
        except Exception as e:
            logger.error(f"Error deleting organization: {str(e)}")
            raise
    @staticmethod
    def is_test_mode():
        """Check if we're running in test mode"""
        return os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("TEST_MODE")