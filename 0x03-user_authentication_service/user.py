#!/usr/bin/env python3
"""User class"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

Base = declarative_base()


class User(Base):
    """Class User Mapped to table users"""
    __tablename__ = 'users'
    # ids = 0

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    # @property
    # def incr_ids(self):
    #     """Increments ids"""
    #     self.ids += 1

    # def __init__(self, email: str, hashed_password: str,
    #              session_id: str=None, reset_token: str =None):
    #     """Instantiate an new instnace of the class"""
    #     self.id = self.ids + 1
    #     self.incr_ids
    #     self.email = email
    #     self.hashed_password = hashed_password
    #     self.session_id = session_id
    #     self.reset_token = reset_token
