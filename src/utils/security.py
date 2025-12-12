import secrets
import string
from typing import Optional

def generate_secure_password(length: int = 12) -> str:
    """Generate a secure random password"""
    if length < 8:
        length = 8
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_-+=<>?"
    
    # Ensure at least one character from each set
    password_chars = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(special)
    ]
    
    # Fill the rest with random choices from all sets
    all_chars = lowercase + uppercase + digits + special
    password_chars.extend(secrets.choice(all_chars) for _ in range(length - 4))
    
    # Shuffle the characters
    secrets.SystemRandom().shuffle(password_chars)
    
    return ''.join(password_chars)

def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Check for character variety
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_-+=<>?" for c in password)
    
    if not (has_lower and has_upper and has_digit):
        return False, "Password must contain uppercase, lowercase, and digits"
    
    # Check for common patterns (simplified)
    common_patterns = ["123456", "password", "qwerty", "admin"]
    if any(pattern in password.lower() for pattern in common_patterns):
        return False, "Password contains common pattern"
    
    return True, None