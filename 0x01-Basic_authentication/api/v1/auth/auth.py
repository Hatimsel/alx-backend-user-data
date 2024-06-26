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
        for p in excluded_paths:
            if p[-1] == '*':
                if path.startswith(p[:-1]) or path + '/' == p:
                    return False
            elif path.startswith(p) or path + '/' == p:
                return False
        # elif path in excluded_paths or path + '/' in excluded_paths:
        #     return False
        return True

    def authorization_header(self, request=None) -> str:
        """Adds the Authorization header to the request"""
        if request is None:
            return None
        elif request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """The current user"""
        return None
