#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt
from bcrypt import hashpw, checkpw


def hash_password(password: str) -> bytes:
    """
    Takes one string argument name password and
    returns a salted, hashed password, which is a
    byte string.
    """
    password = bytes(password, 'utf-8')
    return hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checking the validity of a password"""
    return checkpw(password.encode('utf-8'), hashed_password)
