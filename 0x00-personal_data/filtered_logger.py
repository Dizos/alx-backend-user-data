#!/usr/bin/env python3
"""
Module to securely hash and validate passwords using bcrypt.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with a salt using bcrypt, returning the hashed password as bytes.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that a provided password matches the hashed password using bcrypt.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain-text password to validate.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
