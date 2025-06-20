#!/usr/bin/env python3
"""
Authentication module
This module provides authentication-related utilities and the Auth class.
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid

def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with salt"""
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())

def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation"""
    return str(uuid.uuid4())

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
        """Validate user credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        
        password_bytes = password.encode('utf-8')
        hashed_password = user.hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_password)

    def create_session(self, email: str) -> str:
        """Create a new session for a user
        
        Args:
            email: User's email address
            
        Returns:
            The session ID if user exists, None otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
