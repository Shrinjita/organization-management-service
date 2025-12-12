from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class OrganizationCreateSchema(BaseModel):
    organization_name: str = Field(..., min_length=1, max_length=100, description="Name of the organization")
    email: EmailStr = Field(..., description="Admin email address")
    password: str = Field(..., min_length=8, description="Admin password (min 8 characters)")

class OrganizationResponseSchema(BaseModel):
    id: str
    organization_name: str
    collection_name: str
    admin_email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrganizationUpdateSchema(BaseModel):
    organization_name: str = Field(..., description="Current organization name")
    new_organization_name: Optional[str] = Field(None, min_length=1, max_length=100, description="New organization name")
    email: Optional[EmailStr] = Field(None, description="New admin email")
    password: Optional[str] = Field(None, min_length=8, description="New admin password")

class OrganizationDeleteSchema(BaseModel):
    organization_name: str = Field(..., description="Name of organization to delete")

class OrganizationGetSchema(BaseModel):
    organization_name: str = Field(..., description="Name of organization to fetch")