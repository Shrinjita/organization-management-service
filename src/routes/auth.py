from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from src.schemas.admin import AdminLoginSchema, TokenResponseSchema
from src.services.admin_service import AdminService
from src.utils.jwt import verify_token
import logging

router = APIRouter(prefix="/admin", tags=["Authentication"])
security = HTTPBearer()
logger = logging.getLogger(__name__)

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated admin"""
    token = credentials.credentials
    admin_info = verify_token(token)
    
    if not admin_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Make sure all required fields are present
    required_fields = ["admin_id", "email", "organization_id", "organization_name"]
    for field in required_fields:
        if field not in admin_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Malformed token: missing {field}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    return admin_info

@router.post("/login", response_model=TokenResponseSchema)
async def admin_login(login_data: AdminLoginSchema):
    """
    Admin login endpoint.
    
    - **email**: Admin email address
    - **password**: Admin password
    
    Returns JWT token with admin and organization info.
    """
    try:
        result = await AdminService.login_admin(
            email=login_data.email,
            password=login_data.password
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.get("/verify")
async def verify_admin_token(current_admin: dict = Depends(get_current_admin)):
    """
    Verify admin token.
    
    Returns current admin information if token is valid.
    """
    return {
        "message": "Token is valid",
        "admin": {
            "id": current_admin.get("admin_id"),
            "email": current_admin.get("email"),
            "organization_id": current_admin.get("organization_id"),
            "organization_name": current_admin.get("organization_name")
        }
    }