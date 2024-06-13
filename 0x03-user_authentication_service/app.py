#!/usr/bin/env python3
"""Flask app"""
from auth import Auth
from user import User
import flask
from flask import (redirect, abort,
                   Flask, jsonify, request,
                   make_response)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def root() -> str:
    """Root route for our app"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'],
           strict_slashes=False)
def users() -> str:
    """Register a user if not exists"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'],
           strict_slashes=False)
def login():
    """POST Login the user endpoint"""
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email,
                                      "message": "logged in"}))
        resp.set_cookie('session_id', session_id)

        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'],
           strict_slashes=False)
def logout():
    """Log out the user and destroy the session id"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
    abort(403)


@app.route('/profile', strict_slashes=False)
def profile() -> str:
    """Serve the profile page"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'],
           strict_slashes=False)
def get_reset_password_token() -> str:
    """Get reset password token"""
    email = request.form.get('email', '')
    session = AUTH._db._session

    user = session.query(User).filter_by(email=email).first()
    if user:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    abort(403)


@app.route('/reset_password', methods=['PUT'],
           strict_slashes=False)
def update_password() -> str:
    """Update password end-point"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
