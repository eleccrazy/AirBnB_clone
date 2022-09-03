#!/usr/bin/python3
"""
This module defines a class called Review that inherits
from the BaseModel class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    This class represents a Review object and inherits from
    a BaseModel class.
    """
    place_id = ""
    user_id = ""
    text = ""
