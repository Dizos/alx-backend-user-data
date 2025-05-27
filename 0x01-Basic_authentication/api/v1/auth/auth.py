#!/usr/bin/env python3
"""
Authentication module for the API.
Provides a base class for managing API authentication.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    A base class for API authentication management.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
                  - Returns True if path is None.
                  - Returns True if excluded_paths is None or empty.
                  - Returns False if path (slash-tolerant) is in excluded_paths.
                  - Returns True if path is not in excluded_paths.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        
        # Normalize path and excluded_paths by removing trailing slashes
        normalized_path = path.rstrip('/')
        normalized_excluded = [p.rstrip('/') for p in excluded_paths]
        
        return normalized_path not in normalized_excluded

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from the request.

        Args:
            request: Flask request object (default: None).

        Returns:
            str: The value of the Authorization header, or None if request is None
                 or the header is missing.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current authenticated user.

        Args:
            request: Flask request object (default: None).

        Returns:
            TypeVar('User'): None (placeholder implementation).
        """
        return None
