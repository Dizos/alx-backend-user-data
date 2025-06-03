#!/usr/bin/env python3
"""
DB module for database operations
This module provides a DB class to interact with the database.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    Handles database operations and session management.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by arbitrary keyword arguments"""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the specified criteria")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes.
        
        Args:
            user_id: The id of the user to update
            **kwargs: Arbitrary keyword arguments of user attributes to update
            
        Returns:
            None
            
        Raises:
            ValueError: If an invalid attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"Invalid attribute: {key}")
                setattr(user, key, value)
            self._session.commit()
        except (NoResultFound, InvalidRequestError) as e:
            raise e
