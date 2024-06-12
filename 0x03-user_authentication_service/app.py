#!/usr/bin/env python3
"""Flask app"""
from auth import Auth
from flask import abort, Flask, jsonify, request, make_response

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def root():
    """Root route for our app"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'],
           strict_slashes=False)
def users():
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
def login():
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
