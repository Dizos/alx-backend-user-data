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
            excluded_paths (List[str]): List of paths that do not require authentication,
                                       may end with '*' to match any suffix.

        Returns:
            bool: True if authentication is required, False otherwise.
                  - Returns True if path is None.
                  - Returns True if excluded_paths is None or empty.
                  - Returns False if path (slash-tolerant) matches an excluded path
                    or starts with a prefix from an excluded path ending with '*'.
                  - Returns True otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Normalize path by removing trailing slash
        normalized_path = path.rstrip('/')

        for excluded in excluded_paths:
            # Normalize excluded path
            normalized_excluded = excluded.rstrip('/')
            # Check for wildcard
            if normalized_excluded.endswith('*'):
                prefix = normalized_excluded[:-1]
                if normalized_path.startswith(prefix):
                    return False
            elif normalized_path == normalized_excluded:
                return False

        return True

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
