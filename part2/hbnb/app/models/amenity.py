#!/usr/bin/python3
from .basemodel import BaseModel
"""Amenity module"""


class Amenity(BaseModel):
    """HBnB amenity class

    Args:
        BaseModel (class): Base class for all objects,
            that amenities inherit of
    """
    def __init__(self, name):
        """Amenity constructor

        Args:
            name (str): The amenity's name
        """
        self.name = name
        super().__init__()

        self.places = []

    @property
    def name(self):
        """Amenity name getter

        Returns:
            str: The amenity's name
        """
        return self.__name

    @name.setter
    def name(self, value):
        """Amenity name setter

        Args:
            value (str): What should be the amenity's name

        Raises:
            TypeError: If it's not a string or doesn't exist
            ValueError: If it's empty or longer than 50 characters
        """
        if not (value and isinstance(value, str)):
            raise TypeError("Amenity name must be a non-empty string.")
        if value == "" or len(value) > 50:
            raise ValueError("Amenity name must be\
between 1 and 50 characters.")
        self.__name = value

    def add_place(self, place):
        """Add a place to the amenity."""
        self.places.append(place)

    def __str__(self):
        """String representation of the amenity

        Returns:
            str: The string representation of the amenity
        """
        return "<{}>".format(self.__name)
