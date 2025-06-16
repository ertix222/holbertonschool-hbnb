#!/usr/bin/python3
from basemodel import BaseModel
import re
"""User"""


class User(BaseModel):
    """HBnB user class

    Args:
        BaseModel (class): Base class for all objects, that users inherit of
    """
    def __init__(self, first_name, last_name, email, is_admin=False):
        """User constructor

        Args:
            first_name (str): The user's first name
            last_name (str): The user's last name
            email (str): The user's email adress
            is_admin (bool, optional): _description_. Defaults to False.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        """User first name getter

        Returns:
            str: The user's first name (privates it)
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        """User first name setter

        Args:
            value (str): What should be the user's first name

        Raises:
            TypeError: If it's not a string or doesn't exist
            ValueError: If it's empty or longer than 50 characters
        """
        if not (value and isinstance(value, str)):
            raise TypeError("First name must be a string.")
        if value == "" or len(value) > 50:
            raise ValueError("You must enter a first name\
                between 1 and 50 characters.")
        self.__first_name = value

    @property
    def last_name(self):
        """User last name getter

        Returns:
            str: The user's last name (privates it)
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        """User last name setter

        Args:
            value (str): What should be the user's last name

        Raises:
            TypeError: If it's not a string or doesn't exist
            ValueError: If it's empty or longer than 50 characters
        """
        if not (value and isinstance(value, str)):
            raise TypeError("Last name must be a string.")
        if value == "" or len(value) > 50:
            raise ValueError("You must enter a last name\
                between 1 and 50 characters.")
        self.__last_name = value

    @property
    def email(self):
        """User email address getter

        Returns:
            str: The user's email address (privates it)
        """
        return self.__email

    @email.setter
    def email(self, value):
        """User email address setter

        Args:
            value (str): What should be the user's email

        Raises:
            TypeError: If it's not a string or doesn't exist
            ValueError: If it's empty or not in the right email format
        """
        if not (value and isinstance(value, str)):
            raise TypeError("Email must be a string.")
        if value == "" or not self.email_validator(value):
            raise ValueError("You must enter a valid email with this format:\
                example123@example.com).")
        self.__email = value

    @staticmethod
    def email_validator(value):
        """Email validator method. Simplifies the email validation.

        Args:
            value (str): What should be the user's email.

        Returns:
            bool: Whether the email is valid or not
        """
        return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                        value) is not None
