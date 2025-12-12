from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from src.db.mongo import mongo_manager

class OrganizationBase(BaseModel):
    organization_name: str = Field(..., min_length=1, max_length=100)
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8)
    
class OrganizationCreate(OrganizationBase):
    pass

class OrganizationInDB(BaseModel):
    id: str = Field(alias="_id")
    organization_name: str
    collection_name: str
    admin_user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class OrganizationResponse(BaseModel):
    id: str
    organization_name: str
    collection_name: str
    admin_email: str
    created_at: datetime
    
    class Config:
        json_encoders = {ObjectId: str}

class OrganizationUpdate(BaseModel):
    new_organization_name: Optional[str] = Field(None, min_length=1, max_length=100)
    admin_email: Optional[EmailStr] = None
    admin_password: Optional[str] = Field(None, min_length=8)

class OrganizationModel:
    """Organization model for database operations"""
    
    @staticmethod
    def get_collection():
        return mongo_manager.get_master_db().organizations
    
    @staticmethod
    def create_indexes():
        """Create necessary indexes"""
        collection = OrganizationModel.get_collection()
        collection.create_index("organization_name", unique=True)
        collection.create_index("admin_email", unique=True)
        collection.create_index("collection_name", unique=True)
    
    @staticmethod
    def find_by_name(organization_name: str):
        return OrganizationModel.get_collection().find_one(
            {"organization_name": organization_name}
        )
    
    @staticmethod
    def find_by_email(email: str):
        return OrganizationModel.get_collection().find_one(
            {"admin_email": email}
        )
    
    @staticmethod
    def create(organization_data: dict):
        return OrganizationModel.get_collection().insert_one(organization_data)
    
    @staticmethod
    def update(organization_name: str, update_data: dict):
        return OrganizationModel.get_collection().update_one(
            {"organization_name": organization_name},
            {"$set": update_data}
        )
    
    @staticmethod
    def delete(organization_name: str):
        return OrganizationModel.get_collection().delete_one(
            {"organization_name": organization_name}
        )