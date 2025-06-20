#!/usr/bin/python3
"""Place module"""
from .basemodel import BaseModel
from .user import User


class Place(BaseModel):
    """HBnB place class

    Args:
        BaseModel (class): Base class for all objects,
            that places inherit of
    """
    def __init__(self, title, price, latitude, longitude, owner_id,
                 description=""):
        """Place constructor

        Args:
            title (str): The place's name or title
            price (float): The price per night for the place
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
        self.owner_id = owner_id
        super().__init__()

        self.owner.add_place(self)
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        """Place title getter

        Returns:
            str: The place's title
        """
        return self.__title

    @title.setter
    def title(self, value):
        """Place title setter

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
        """Place description setter

        Args:
            value (str): What should be the place's description

        Raises:
            TypeError: If it's not a string or doesn't exist
        """
        if not (value and isinstance(value, str)):
            raise TypeError("Place description must be a string.")
        self.__description = value

    @property
    def price(self):
        """Place price getter

        Returns:
            float: The place's price
        """
        return self.__price

    @price.setter
    def price(self, value):
        """Place price setter

        Args:
            value (float): What should be the place's price

        Raises:
            TypeError: If it's not a float or doesn't exist
            ValueError: If it's negative or zero
        """
        if not (value and (isinstance(value, float)
                           or isinstance(value, int))):
            raise TypeError("Place price must be a float number.")
        if value < 0:
            raise ValueError("Place price must be positive.")
        self.__price = value

    @property
    def latitude(self):
        """Place latitude getter

        Returns:
            float: The place's latitude (north to south)
        """
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """Place latitude setter

        Args:
            value (float): What should be the place's latitude

        Raises:
            TypeError: If it's not a float or doesn't exist
            ValueError: If it's outside of the -90~90 degrees range
        """
        if not (value and isinstance(value, float)):
            raise TypeError("Place latitude must be a float number.")
        if not (-90.0 < value <= 90.0):
            raise ValueError("Place latitude must be between -90.0 and 90.0.")
        self.__latitude = value

    @property
    def longitude(self):
        """Place longitude getter

        Returns:
            float: The place's longitude (meridian)
        """
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """Place longitude setter

        Args:
            value (float): What should be the place's longitude

        Raises:
            TypeError: If it's not a float or doesn't exist
            ValueError: If it's outside of the -180~180 degrees range
        """
        if not (value and isinstance(value, float)):
            raise TypeError("Place longitude must be a float number.")
        if not (-180.0 < value <= 180.0):
            raise ValueError("Place longitude must be\
between -180.0 and 180.0.")
        self.__longitude = value

    @property
    def owner(self):
        """Place owner getter

        Returns:
            User: The place's owner
        """
        return self.__owner

    @owner.setter
    def owner(self, value):
        """Place owner setter (privates it)

        Args:
            value (User): What should be the place's owner

        Raises:
            TypeError: If it's not a user or doesn't exist
        """
        if not (value and isinstance(value, User)):
            raise TypeError("Place owner must be an existing user.")
        self.__owner = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def list_amenities(self):
        """List of amenities associated with the place"""
        for i in self.amenities:
            print(i)
