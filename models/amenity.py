#!/usr/bin/python3
"""
This module defines a class called Amenity that inherits
from the BaseModel class
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    This class represents an Amenity object and inherits from
    a BaseModel class.
    """
    name = ""
