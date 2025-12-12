from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import Dict, Any
from src.schemas.organization import (
    OrganizationCreateSchema,
    OrganizationResponseSchema,
    OrganizationUpdateSchema,
    OrganizationDeleteSchema,
    OrganizationGetSchema
)
from src.services.organization_service import OrganizationService
from src.routes.auth import get_current_admin
import logging

router = APIRouter(prefix="/org", tags=["Organization Management"])
logger = logging.getLogger(__name__)

@router.post("/create", response_model=OrganizationResponseSchema)
async def create_organization(
    org_data: OrganizationCreateSchema,
    background_tasks: BackgroundTasks
):
    """
    Create a new organization.
    
    - **organization_name**: Name of the organization (must be unique)
    - **email**: Admin email address (must be unique)
    - **password**: Admin password (min 8 characters)
    
    Creates a new MongoDB collection for the organization and sets up admin user.
    """
    try:
        result = await OrganizationService.create_organization(org_data.dict())
        
        # Log creation in background
        background_tasks.add_task(
            logger.info,
            f"Organization created: {org_data.organization_name} by {org_data.email}"
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating organization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create organization"
        )

@router.get("/get", response_model=OrganizationResponseSchema)
async def get_organization(
    org_name: str,
    current_admin: Dict[str, Any] = Depends(get_current_admin)
):
    """
    Get organization details by name.
    
    - **organization_name**: Name of the organization to fetch
    
    Returns organization metadata from Master Database.
    """
    try:
        org_data = await OrganizationService.get_organization(org_name)
        
        if not org_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization '{org_name}' not found"
            )
        
        # Check if current admin has access to this organization
        if current_admin["organization_name"] != org_data["organization_name"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this organization"
            )
        
        return org_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching organization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch organization details"
        )

@router.put("/update")
async def update_organization(
    update_data: OrganizationUpdateSchema,
    current_admin: Dict[str, Any] = Depends(get_current_admin)
):
    """
    Update organization details.
    
    - **organization_name**: Current organization name
    - **new_organization_name** (optional): New organization name
    - **email** (optional): New admin email
    - **password** (optional): New admin password
    
    Updates organization metadata and handles collection renaming if needed.
    """
    try:
        # Verify current admin owns the organization
        if current_admin["organization_name"] != update_data.organization_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: You can only update your own organization"
            )
        
        result = await OrganizationService.update_organization(
            update_data.dict(exclude_none=True),
            current_admin["email"]
        )
        
        return {"message": "Organization updated successfully", **result}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating organization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update organization"
        )

@router.delete("/delete")
async def delete_organization(
    delete_data: OrganizationDeleteSchema,
    current_admin: Dict[str, Any] = Depends(get_current_admin)
):
    """
    Delete an organization.
    
    - **organization_name**: Name of organization to delete
    
    Deletes organization metadata and its dynamic collection.
    Only authenticated admin of the organization can delete it.
    """
    try:
        # Verify current admin owns the organization
        if current_admin["organization_name"] != delete_data.organization_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: You can only delete your own organization"
            )
        
        result = await OrganizationService.delete_organization(
            delete_data.organization_name,
            current_admin["email"]
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting organization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete organization"
        )

@router.get("/list")
async def list_organizations(
    current_admin: Dict[str, Any] = Depends(get_current_admin)
):
    """
    List organizations (for demonstration - in production would be admin-only).
    
    Returns basic info about all organizations.
    """
    try:
        from src.db.mongo import mongo_manager
        master_db = mongo_manager.get_master_db()
        
        # Get all organizations (limited for security)
        organizations = list(master_db.organizations.find(
            {}, 
            {"organization_name": 1, "admin_email": 1, "created_at": 1}
        ).limit(50))
        
        # Convert ObjectId to string
        for org in organizations:
            org["id"] = str(org.pop("_id"))
        
        return {
            "count": len(organizations),
            "organizations": organizations
        }
        
    except Exception as e:
        logger.error(f"Error listing organizations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list organizations"
        )