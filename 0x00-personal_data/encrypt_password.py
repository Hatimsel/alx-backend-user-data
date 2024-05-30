#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str):
    """
    Takes one string argument name password and
    returns a salted, hashed password, which is a
    byte string.
    """
    password = bytes(password, 'utf-8')
    return hashpw(password, bcrypt.gensalt())
