#!/usr/bin/python3
"""
This module implements the storage funcitonality of the AirBnB project.
"""
from json import dump
from json import load
from os.path import exists
import sys
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    """
    This class serializes instances to a JSON file and
    deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key
        """
        name = type(obj).__name__
        key = name + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file
        """
        dict_object = {
                obj: FileStorage.__objects[obj].
                to_dict() for obj in FileStorage.__objects.keys()
                }
        with open(FileStorage.__file_path, "w", encoding="utf8") as fs:
            dump(dict_object, fs)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        """
        if exists(FileStorage.__file_path):
            with open(FileStorage.__file_path) as fs:
                dict_object = load(fs)
                for obj in dict_object.values():
                    name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(name)(**obj))
