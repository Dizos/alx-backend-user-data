#!/usr/bin/env python3
"""
Authentication module
This module provides authentication-related utilities.
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with salt
    
    Args:
        password: The password string to hash
        
    Returns:
        Salted hash of the password as bytes
    """
    # Convert password string to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate salt and hash the password
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())
