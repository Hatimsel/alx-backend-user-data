#!/usr/bin/env python3
"""BasicAuth class"""
from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Class SessionAuth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user id based on the session id"""
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a User instance based on a cookie value"""
        if request:
            cookie_value = self.session_cookie(request)
            user_id = self.user_id_by_session_id.get(cookie_value)
            user = User.get(user_id)

            return user

    def destroy_session(self, request=None):
        """Delete the user session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
