#!/usr/bin/env python3
"""BasicAuth class"""
from .auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Auth class"""
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """Extract the Authorization header"""
        if authorization_header is None or type(authorization_header)\
                is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Decode base64 authorization header"""
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_auth = base64.b64decode(base64_authorization_header.
                                            encode('utf-8'))
            return decoded_auth.decode('utf-8')
        except (TypeError, ValueError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extract user credentials"""
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(':')[0]
        password = decoded_base64_authorization_header.split(':')[1]

        return (email, password)
