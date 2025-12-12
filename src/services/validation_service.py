import re
from typing import Dict, Any, Optional
from src.utils.validators import validate_organization_name, validate_email
from src.utils.logger import logger

class ValidationService:
    """Service for validating inputs"""
    
    @staticmethod
    def validate_organization_create(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate organization creation data"""
        # Validate organization name
        if not validate_organization_name(data.get("organization_name", "")):
            return False, "Invalid organization name"
        
        # Validate email
        if not validate_email(data.get("email", "")):
            return False, "Invalid email address"
        
        # Validate password
        password = data.get("password", "")
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        # Check for whitespace in organization name
        org_name = data["organization_name"]
        if org_name.startswith(" ") or org_name.endswith(" "):
            return False, "Organization name cannot start or end with spaces"
        
        # Check for consecutive spaces
        if "  " in org_name:
            return False, "Organization name cannot contain consecutive spaces"
        
        return True, None
    
    @staticmethod
    def validate_organization_update(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate organization update data"""
        # Validate current organization name
        if not data.get("organization_name"):
            return False, "Current organization name is required"
        
        # Validate new organization name if provided
        new_name = data.get("new_organization_name")
        if new_name and not validate_organization_name(new_name):
            return False, "Invalid new organization name"
        
        # Validate new email if provided
        new_email = data.get("email")
        if new_email and not validate_email(new_email):
            return False, "Invalid email address"
        
        # Validate new password if provided
        new_password = data.get("password")
        if new_password and len(new_password) < 8:
            return False, "New password must be at least 8 characters"
        
        return True, None
    
    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize input data"""
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Trim whitespace
                sanitized[key] = value.strip()
                
                # Prevent XSS (simplified)
                sanitized[key] = re.sub(r'<script.*?>.*?</script>', '', sanitized[key], flags=re.IGNORECASE)
            else:
                sanitized[key] = value
        
        return sanitized