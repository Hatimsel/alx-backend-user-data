#!/usr/bin/env python3
"""Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication"""
        if path is None or excluded_paths is None:
            return True
        elif path in excluded_paths or path + '/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Adds the Authorization header to the request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """The current user"""
        return None
