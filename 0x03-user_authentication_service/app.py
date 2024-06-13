#!/usr/bin/env python3
"""Flask app"""
from auth import Auth
import flask
from flask import (redirect, url_for, abort,
                   Flask, jsonify, request,
                   make_response, Response)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def root() -> Response:
    """Root route for our app"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'],
           strict_slashes=False)
def users() -> Response:
    """Register a user if not exists"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'],
           strict_slashes=False)
def login() -> Response:
    """Login the user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response()
        resp.set_cookie('session_id', session_id)

        return jsonify({'email': email, 'message': 'logged in'})
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'],
           strict_slashes=False)
def logout() -> Response:
    """Log out the user and destroy the session id"""
    session_id = request.cookies.get('session_id')
    # print(session_id)
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(int(user.id))
            return redirect(url_for(root))
    abort(403)


@app.route('/profile', strict_slashes=False)
def profile() -> Response:
    """Serve the profile page"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
