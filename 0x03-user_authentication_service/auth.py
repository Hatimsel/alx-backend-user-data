#!/usr/bin/env python3
"""Authentication system"""
from db import DB
from user import User
from typing import Union
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """Hash the password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """"Register the User object to db"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {user.email} already exists')
        except Exception:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate credentials"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password):
                return True
        except Exception:
            pass
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a session id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get the user from a session_id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Update the user's session_id to None"""
        db = self._db

        try:
            db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update passord"""
        if reset_token and password:
            try:
                user = self._db.find_user_by(reset_token=reset_token)
                hashed_pwd = _hash_password(password)
                self._db.update_user(user.id, hashed_password=hashed_pwd,
                                     reset_token=None)
            except Exception:
                raise ValueError
        else:
            return None
