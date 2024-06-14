#!/usr/bin/env python3
"""
Main file
"""
import requests

url = 'http://0.0.0.0:5000/'


def register_user(email: str, passord: str) -> None:
    """Test register user endpoint"""
    resp = requests.post(f'{url}users', data={'email': email,
                                              'password': passord})
    assert resp.status_code == 200

def log_in_wrong_password(email: str, password: str) -> None:
    """Test log in with wrong pass"""
    resp = requests.post(f'{url}sessions', data={'email': email,
                                              'password': password})
    assert resp.status_code == 401

def log_in(email: str, password: str) -> str:
    """Test log in"""
    resp = requests.post(f'{url}sessions', data={'email': email,
                                              'password': password})
    assert resp.status_code == 200
    assert 'session_id' in resp.cookies

    return resp.cookies.get('session_id')

def profile_unlogged() -> None:
    """Test profile endpoint without being logged in"""
    resp = requests.get(f'{url}profile')

    assert resp.status_code == 403

def profile_logged(session_id: str) -> None:
    """Test profile endpoint logged in"""
    resp = requests.get(f'{url}profile', cookies={'session_id': session_id})

    assert resp.status_code == 200

def log_out(session_id: str) -> None:
    """Test login out"""
    resp = requests.delete(f'{url}sessions', cookies={'session_id': session_id})

    assert resp.status_code == 200

def reset_password_token(email: str) -> str:
    """Test reset token enpoint"""
    resp = requests.post(f'{url}reset_password',
                         data={'email': email})
    
    assert resp.status_code == 200
    return resp.cookies.get('session_id')

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update pass endpoint"""
    resp = requests.put(f'{url}reset_password', data={'email': email,
                        'reset_token': reset_token,
                        'new_password': new_password})
    
    assert resp.status_code == 200

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    # print(session_id)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
