from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from src.models.admin_user import AdminUserModel
from src.models.organization import OrganizationModel
from src.utils.password import verify_password
from src.utils.jwt import create_access_token
from src.config.settings import settings
from src.utils.logger import logger

class AdminService:
    """Service for admin authentication and management"""
    
    @staticmethod
    async def authenticate_admin(email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate admin user"""
        try:
            # Find admin user
            admin_user = AdminUserModel.find_by_email(email)
            if not admin_user:
                return None
            
            # Verify password
            if not verify_password(password, admin_user["hashed_password"]):
                return None
            
            # Check if admin is active
            if not admin_user.get("is_active", True):
                raise ValueError("Admin account is deactivated")
            
            # Get organization info
            org_data = OrganizationModel.find_by_name(admin_user["organization_name"])
            if not org_data:
                raise ValueError("Organization not found")
            
            return {
                "admin_id": str(admin_user["_id"]),
                "email": admin_user["email"],
                "organization_id": str(org_data["_id"]),
                "organization_name": org_data["organization_name"]
            }
            
        except Exception as e:
            logger.error(f"Authentication error for {email}: {str(e)}")
            return None
    
    @staticmethod
    async def login_admin(email: str, password: str) -> Optional[Dict[str, Any]]:
        """Login admin and return JWT token"""
        try:
            # Authenticate admin
            admin_info = await AdminService.authenticate_admin(email, password)
            if not admin_info:
                return None
            
            # Create access token
            token_data = {
                "sub": admin_info["admin_id"],
                "email": admin_info["email"],
                "org_id": admin_info["organization_id"],
                "org_name": admin_info["organization_name"]
            }
            
            access_token = create_access_token(token_data)
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "organization_id": admin_info["organization_id"],
                "admin_id": admin_info["admin_id"],
                "organization_name": admin_info["organization_name"]
            }
            
        except Exception as e:
            logger.error(f"Login error for {email}: {str(e)}")
            return None
    
    @staticmethod
    async def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return admin info"""
        try:
            from src.utils.jwt import verify_token as verify_jwt_token
            payload = verify_jwt_token(token)
            if not payload:
                return None
            
            # Check if admin still exists and is active
            admin_user = AdminUserModel.find_by_id(payload["sub"])
            if not admin_user or not admin_user.get("is_active", True):
                return None
            
            return {
                "admin_id": payload["sub"],
                "email": payload["email"],
                "organization_id": payload["org_id"],
                "organization_name": payload["org_name"]
            }
            
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            return None