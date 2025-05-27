#!/usr/bin/env python3
"""
Basic Authentication module for the API.
Provides a class for handling basic authentication.
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    A class for Basic Authentication, inheriting from Auth.
    Handles extraction of Base64 part from Authorization header.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header value.

        Returns:
            str: The Base64 part after 'Basic ', or None if:
                 - authorization_header is None
                 - authorization_header is not a string
                 - authorization_header doesn't start with 'Basic '
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]
