#!/usr/bin/env python3
"""
Session authentication module.
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User

class SessionAuth(Auth):
    """
    Session authentication class, inheriting from Auth.
    Manages session IDs mapped to user IDs.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user_id.

        Args:
            user_id (str, optional): The ID of the user. Defaults to None.

        Returns:
            str: The generated Session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the User ID associated with a given Session ID.

        Args:
            session_id (str, optional): The Session ID to look up. Defaults to None.

        Returns:
            str: The User ID associated with the Session ID, or None if invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Retrieves a User instance based on the session cookie value.

        Args:
            request: Flask request object.

        Returns:
            User: The User instance associated with the session cookie, or None if not found.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
