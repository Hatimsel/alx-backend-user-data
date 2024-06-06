#!/usr/bin/env python3
"""BasicAuth class"""
from .auth import Auth
from models.user import User
from api.v1.views import session_views
from flask import jsonify, request
from models.user import User
from os import getenv
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


@session_views.route('/auth_session/login', methods=['POST'],
                     strict_slashes=False)
def login():
    """"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if isinstance(user[0], User):
        if user[0].is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user[0].id)
            return_value = jsonify(user[0].to_json())
            return_value.set_cookie(getenv('SESSION_NAME'), session_id)

            return return_value
    return jsonify({"error": "wrong password"}), 400
