#!/usr/bin/env python3
"""BasicAuth class"""
from .auth import Auth
#from auth import Auth


class BasicAuth(Auth):
    """Basic Auth class"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract the Authorization header"""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]
