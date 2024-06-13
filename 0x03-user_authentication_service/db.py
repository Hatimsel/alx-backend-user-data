#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import Union


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a User object to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs: dict) -> Union[User, None]:
        """
        Take arbitrary keyword args and return the
        first row found in the users table
        """
        session = self._session

        query = session.query(User)
        for k, v in kwargs.items():
            if hasattr(User, k):
                query = query.filter(getattr(User, k) == v)

            else:
                raise InvalidRequestError('Invalid')
        user = query.first()
        if user:
            return user
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user object"""
        session = self._session
        user = self.find_user_by(id=user_id)

        if user:
            for k, v in kwargs.items():
                if hasattr(user, k):
                    setattr(user, k, v)
                    session.commit()
                else:
                    raise ValueError
