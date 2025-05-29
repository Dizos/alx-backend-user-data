#!/usr/bin/env python3
"""
Base authentication class.
"""
from flask import request
from typing import List, TypeVar
from os import getenv

class Auth:
    """
    Base class for authentication mechanisms.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The request path.
            excluded_paths (List[str]): List of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        path = path.rstrip('/')
        for excluded in excluded_paths:
            if excluded.rstrip('/').startswith(path) or path.startswith(excluded.rstrip('/')):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: Flask request object.

        Returns:
            str: The Authorization header value or None if not present.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user (to be implemented by subclasses).

        Args:
            request: Flask request object.

        Returns:
            User: The authenticated user or None.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Retrieves the value of the session cookie from the request.

        Args:
            request: Flask request object.

        Returns:
            str: The value of the cookie named by SESSION_NAME, or None if not found.
        """
        if request is None:
            return None
        session_name = getenv("SESSION_NAME")
        return request.cookies.get(session_name)
