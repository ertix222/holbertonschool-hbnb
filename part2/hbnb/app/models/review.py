#!/usr/bin/python3
"""Review module"""
from .basemodel import BaseModel
from .user import User
from .place import Place


class Review(BaseModel):
    """HBnB review class

    Args:
        BaseModel (class): Base class for all objects, that reviews inherit of
    """
    def __init__(self, text, rating, place, user):
        """Review constructor

        Args:
            text (str): The review's text
            rating (float): The rating of the place given by the user
            user (User): The user writing the review
            place (Place): The place the review is about
        """
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        super().__init__()

    @property
    def text(self):
        """Review text getter

        Returns:
            str: The review's text
        """
        return self.__text

    @text.setter
    def text(self, value):
        """Review text setter

        Args:
            value (str): What should be the review's text

        Raises:
            TypeError: If it's not a string or doesn't exist
            ValueError: If it's empty
        """
        if not (value and isinstance(value, str)):
            raise TypeError("Review text must be a string.")
        if value == "":
            raise ValueError("Review text must not be textless")
        self.__text = value

    @property
    def rating(self):
        """Review rating getter

        Returns:
            int: The review's rating
        """
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Review rating setter

        Args:
            value (int): What should be the review's rating

        Raises:
            TypeError: If it's a float, not an int or doesn't exist
            ValueError: If it's not between 1 and 5
        """
        if not (value and isinstance(value, int)) or isinstance(value, float):
            raise TypeError("Review rating must be an integer.")
        if not (1 <= value <= 5):
            raise ValueError("Review rating must be between 1 and 5.")
        self.__rating = value

    @property
    def place(self):
        """Reviewed place getter

        Returns:
            Place: The place where the review is posted on
        """
        return self.__place

    @place.setter
    def place(self, value):
        """Reviewed place setter (privates it)

        Args:
            value (Place): What should be the reviewed place

        Raises:
            TypeError: If it's not a place or doesn't exist
        """
        if not (value and isinstance(value, Place)):
            raise TypeError("Only places can be reviewed.")
        self.__place = value

    @property
    def user(self):
        """Review writer user getter

        Returns:
            User: The review's writer
        """
        return self.__user

    @user.setter
    def user(self, value):
        """Review writer user setter (privates it)

        Args:
            value (User): What should be the review's writer

        Raises:
            TypeError: If it's not a user or doesn't exist
        """
        if not (value and isinstance(value, User)):
            raise TypeError("Review writer must be an existing user.")
        self.__user = value
