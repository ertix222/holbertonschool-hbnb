#!/usr/bin/python3
from basemodel import BaseModel
"""Place"""


class Place(BaseModel):
    """HBnB place class

    Args:
        BaseModel (class): Base class for all objects, that places inherit of
    """
    def __init__(self, title, price, latitude, longitude, owner,
                 description=""):
        """Place constructor

        Args:
            title (str): The place's name or title
            price (str): The price per night for the place
            latitude (float): Latitude coordinate for the place location
                between -90.0 and 90.0
            longitude (float): Latitude coordinate for the place location
                between -180.0 and 180.0
            owner (User): The user owning the place
            description (str, optional): The place description
                Defaults to empty.
        """
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        super().__init__()

    @property
    def title(self):
        """Place title getter

        Returns:
            str: The place's title
        """
        return self.__title

    @title.setter
    def title(self, value):
        """Place title setter (privates it)

        Args:
            value (str): What should be the place's title

        Raises:
            TypeError: If it's not a string or doesn't exist
            ValueError: If it's empty or longer than 100 characters
        """
        if not (value and isinstance(value, str)):
            raise TypeError("Place title must be a string.")
        if value == "" or len(value) > 100:
            raise ValueError("Place title must be\
                between 1 and 100 characters.")
        self.__title = value

    @property
    def description(self):
        """Place description getter

        Returns:
            str: The place's description
        """
        return self.__description

    @description.setter
    def description(self, value):
        """Place description setter (privates it)

        Args:
            value (str): What should be the place's description

        Raises:
            TypeError: If it's not a string or doesn't exist
        """
        if not (value and isinstance(value, str)):
            raise TypeError("Place description must be a string.")
        self.__description = value
