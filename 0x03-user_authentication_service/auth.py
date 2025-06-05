#!/usr/bin/env python3
"""
Authentication module
This module provides authentication-related utilities and the Auth class.
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound

def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with salt
    
    Args:
        password: The password string to hash
        
    Returns:
        Salted hash of the password as bytes
    """
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """Initialize a new Auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        
        Args:
            email: User's email address
            password: User's plain text password
            
        Returns:
            The created User object
            
        Raises:
            ValueError: If a user with the email already exists
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User doesn't exist - proceed with registration
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password.decode('utf-8'))
