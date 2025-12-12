from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from src.db.mongo import mongo_manager
from typing import List, Dict, Any, Optional

class AdminUserBase(BaseModel):
    email: EmailStr
    password: str
    organization_id: str
    
class AdminUserCreate(AdminUserBase):
    pass

class AdminUserInDB(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    hashed_password: str
    organization_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AdminUserResponse(BaseModel):
    id: str
    email: EmailStr
    organization_id: str
    created_at: datetime
    
    class Config:
        json_encoders = {ObjectId: str}

class AdminUserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    organization_id: str
    admin_id: str

class TokenData(BaseModel):
    admin_id: Optional[str] = None
    organization_id: Optional[str] = None
    email: Optional[str] = None

class AdminUserModel:
    """AdminUser model for database operations"""
    
    @staticmethod
    def get_collection():
        return mongo_manager.get_master_db().admin_users
    
    @staticmethod
    def create_indexes():
        """Create necessary indexes"""
        collection = AdminUserModel.get_collection()
        collection.create_index("email", unique=True)
        collection.create_index("organization_id")
    
    @staticmethod
    def find_by_email(email: str):
        return AdminUserModel.get_collection().find_one({"email": email})
    
    @staticmethod
    def find_by_id(user_id: str):
        return AdminUserModel.get_collection().find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def create(user_data: dict):
        return AdminUserModel.get_collection().insert_one(user_data)
    
    @staticmethod
    def update(user_id: str, update_data: dict):
        return AdminUserModel.get_collection().update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    
    @staticmethod
    def delete(user_id: str):
        return AdminUserModel.get_collection().delete_one(
            {"_id": ObjectId(user_id)}
        )