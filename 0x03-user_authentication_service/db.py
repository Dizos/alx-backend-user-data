#!/usr/bin/env python3
"""
DB module for database operations
This module provides a DB class to handle database operations.
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User

class DB:
    """DB class for database operations
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        
        Args:
            email: User's email address
            hashed_password: Hashed password for the user
            
        Returns:
            The created User object
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments
        
        Args:
            kwargs: Arbitrary keyword arguments to filter users
            
        Returns:
            The first found User object matching the criteria
            
        Raises:
            NoResultFound: When no user is found
            InvalidRequestError: When wrong query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with these criteria")
        except InvalidRequestError as e:
            raise InvalidRequestError("Invalid query arguments") from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes
        
        Args:
            user_id: ID of the user to update
            kwargs: Arbitrary keyword arguments of user attributes to update
            
        Raises:
            ValueError: If an argument doesn't correspond to a user attribute
        """
        # List of valid user attributes
        valid_attributes = ['email', 'hashed_password', 'session_id', 'reset_token']
        
        # Check if all kwargs keys are valid attributes
        for key in kwargs:
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")
        
        try:
            # Find the user by ID
            user = self.find_user_by(id=user_id)
            
            # Update user attributes
            for key, value in kwargs.items():
                setattr(user, key, value)
            
            # Commit changes to database
            self._session.commit()
        except (NoResultFound, InvalidRequestError) as e:
            # Re-raise the exception since we're not handling it here
            raise e
