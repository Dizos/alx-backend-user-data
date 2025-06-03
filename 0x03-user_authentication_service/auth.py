#!/usr/bin/env python3
"""
Authentication module with session creation
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth instance"""
        self._db = DB()

    def _generate_uuid(self) -> str:
        """Generate a new UUID string"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> Optional[str]:
        """
        Create a new session for a user
        
        Args:
            email: User's email address
            
        Returns:
            str: Session ID if user exists, None otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = self._hash_password(password)
            return self._db.add_user(email, hashed_pwd.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            stored_pwd = user.hashed_password.encode('utf-8')
            input_pwd = password.encode('utf-8')
            return bcrypt.checkpw(input_pwd, stored_pwd)
        except NoResultFound:
            return False
