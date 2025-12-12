import re
from typing import Optional

def validate_organization_name(name: str) -> bool:
    """Validate organization name format"""
    if not name or len(name) > 100:
        return False
    
    # Allow alphanumeric, spaces, hyphens, and underscores
    pattern = r'^[a-zA-Z0-9 _-]+$'
    return bool(re.match(pattern, name))

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_collection_name(name: str) -> str:
    """Sanitize organization name for MongoDB collection name"""
    # Convert to lowercase, replace spaces with underscores
    sanitized = name.lower().replace(' ', '_')
    # Remove any invalid characters
    sanitized = re.sub(r'[^a-z0-9_]', '', sanitized)
    # Ensure it starts with a letter
    if sanitized and not sanitized[0].isalpha():
        sanitized = 'org_' + sanitized
    return sanitized