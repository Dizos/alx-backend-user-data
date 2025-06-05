#!/usr/bin/env python3
"""
Authentication module
This module provides authentication-related utilities and the Auth class.
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt

def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with salt"""
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database."""
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials
        
        Args:
            email: User's email address
            password: Password to validate
            
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            # Find user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        
        # Check password if user exists
        password_bytes = password.encode('utf-8')
        hashed_password = user.hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_password)
