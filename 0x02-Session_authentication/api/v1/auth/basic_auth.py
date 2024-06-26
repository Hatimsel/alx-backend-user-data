#!/usr/bin/env python3
"""BasicAuth class"""
from .auth import Auth
from models.user import User
from typing import TypeVar
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
        credentials = decoded_base64_authorization_header.split(':', 1)
        email = credentials[0]
        password = credentials[1]

        return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Rerieving the user from credentials"""
        if not isinstance(user_email, str):
            return None
        if User.count() > 0:
            user = User.search({"email": user_email})
            if user:
                if user[0].is_valid_password(user_pwd):
                    return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overload AUth and retrieve the
        User instance for a request
        """
        if request:
            authorization_header = request.headers['Authorization']
            base64_auth_header = self.extract_base64_authorization_header(
                authorization_header
                )
            decoded_auth_header = self.decode_base64_authorization_header(
                base64_auth_header
                )
            user_credentials = self.extract_user_credentials(
                decoded_auth_header
                )
            user = self.user_object_from_credentials(
                user_credentials[0], user_credentials[1]
                )

            return user if user else None
