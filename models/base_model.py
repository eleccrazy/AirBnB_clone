#!/usr/bin/python3
"""
This module contains a BaseModel class for the AirBnB project.
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    This class defines all common attributes/methods for other classes
    """
    def __init__(self, *args, **kwargs):
        """
        This method instantiates instance attributes.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == 'created_at' or key == 'updated_at':
                    self.__dict__[key] = datetime.strptime(
                            value, '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def __str__(self):
        """
        This method returns the string representation of the BaseModel object.
        """
        name = type(self).__name__
        return "[{}] ({}) {}".format(name, self.id, self.__dict__)

    def save(self):
        """
        This method updates the public instance attribute updated_at with the
        current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        This method  returns a dictionary containing all keys/values
        of __dict__ of the instance
        """
        a_dict = self.__dict__.copy()
        a_dict['__class__'] = type(self).__name__
        a_dict['created_at'] = a_dict['created_at'].isoformat()
        a_dict['updated_at'] = a_dict['updated_at'].isoformat()

        return a_dict
