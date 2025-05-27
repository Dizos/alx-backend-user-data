#!/usr/bin/env python3
"""
Basic Authentication module for the API.
Provides a class for handling basic authentication.
"""

import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    A class for Basic Authentication, inheriting from Auth.
    Handles extraction and decoding of Base64 Authorization headers.
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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode a Base64 Authorization header for Basic Authentication.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded UTF-8 string, or None if:
                 - base64_authorization_header is None
                 - base64_authorization_header is not a string
                 - base64_authorization_header is not valid Base64
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
