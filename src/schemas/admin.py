from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class AdminLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="Admin email address")
    password: str = Field(..., description="Admin password")

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    organization_id: str
    admin_id: str

class ErrorResponseSchema(BaseModel):
    detail: str
    error_code: Optional[str] = None