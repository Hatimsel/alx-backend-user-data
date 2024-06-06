#!/usr/bin/env python3
""" Module of session_auth views
"""
from api.v1.views import session_views
from flask import abort, jsonify, request, abort
from models.user import User
from os import getenv


@session_views.route('/auth_session/login', methods=['POST'],
                     strict_slashes=False)
def login():
    """log the user in"""
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
    return jsonify({"error": "wrong password"}), 401


@session_views.route('/api/v1/auth_session/logout', methods=['DELETE'],
                     strict_slashes=False)
def delete_session():
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
