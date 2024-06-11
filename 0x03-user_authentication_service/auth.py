#!/usr/bin/env python3
"""Authentication system"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash the password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
