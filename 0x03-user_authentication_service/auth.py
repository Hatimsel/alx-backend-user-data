#!/usr/bin/env python3
"""Authentication system"""
from db import DB
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """Hash the password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """"Register the User object to db"""
        session = self._db._session

        user = session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError(f'User {user.email} already exists')

        hashed_pwd = _hash_password(password)
        new_user = User(email=email, hashed_password=hashed_pwd)

        session.add(new_user)
        session.commit()

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate credentials"""
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True

        return False

    @property
    def _generate_uuid(self):
        """Generate a new uuid"""
        return str(uuid.uuid4())
