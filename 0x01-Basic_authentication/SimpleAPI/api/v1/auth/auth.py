#!/usr/bin/env python3
"""Auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class Auth"""
    def require_auth(self, path: str, excluded_paths:List[str]) -> bool:
        """Checks is a path requires authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Adds the Authorization header to the request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """The current user"""
        return None
