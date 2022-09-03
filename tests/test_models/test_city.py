#!/usr/bin/python3

"""
File: test_city.py
Desc: This module contains all possible testcases for the city.py
      modlue in the models package. It uses the standard unittest.
Author: Gizachew Bayness (Elec Crazy) and Biruk Gelelcha
Date Created: Sep 2 2022
"""
import unittest
import models
from models.base_model import BaseModel
from models.city import City
from datetime import datetime as dt
from time import sleep as sp
import os


class TestStateObjectCreation(unittest.TestCase):
    """
    This class provides all possible test cases regarding object
    creation of class User.
    """

    def test_basic_creation(self):
        c = City()
        self.assertEqual(City, type(c))

    def test_if_parrent_class_is_BaseModel(self):
        self.assertIsInstance(City(), BaseModel)

    def test_two_objects_with_different_id(self):
        c1 = City()
        c2 = City()
        self.assertNotEqual(c1.id, c2.id)

    def test_if_id_is_string(self):
        c1 = City()
        self.assertEqual(type(c1.id), str)

    def test_type_of_created_at(self):
        c = City()
        self.assertEqual(dt, type(c.created_at))

    def test_type_of_updated_at(self):
        self.assertEqual(dt, type(City().updated_at))

    def test_the_stored_new_instance(self):
        c = City()
        self.assertIn(c, models.storage.all().values())

    def test_two_objects_with_different_created_at(self):
        c1 = City()
        c2 = City()
        self.assertGreater(c2.created_at, c1.created_at)

    def test_two_objects_with_different_updated_at(self):
        c1 = City()
        c2 = City()
        self.assertLess(c1.updated_at, c2.updated_at)

    def test_object_creation_with_only_args(self):
        c = City(None, 12, "hello")
        self.assertNotIn(None, models.storage.all().values())
        self.assertNotIn(12, models.storage.all().values())
        self.assertNotIn("hello", models.storage.all().values())

    def test_object_creation_with_args_and_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        c = City(22, id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(c.id, "000274")
        self.assertEqual(c.created_at, ts)
        self.assertEqual(c.updated_at, ts)

    def test_object_creation_with_only_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        c = City(id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(c.id, "000274")
        self.assertEqual(c.created_at, ts)
        self.assertEqual(c.updated_at, ts)

    def test_type_of_name(self):
        c = City()
        self.assertEqual(str, type(c.name))

    def test_type_of_state_id(self):
        c = City()
        self.assertEqual(str, type(c.state_id))

    def test_object_creation_with_None_values_kwargs(self):
        with self.assertRaises(TypeError):
            c = City(id=None, created_at=None, updated_at=None)


class TestStateStrMethod(unittest.TestCase):
    """
    This class provides all possible test cases for __str__ method
    of class State.
    """

    def test_simple_str_representation(self):
        c = City()
        c_str = c.__str__()
        self.assertIn("[City] ({})".format(c.id), c_str)

    def test_str_with_possible_attributes(self):
        d = dt.today()
        d_repr = repr(d)
        c = City("Elec Crazy")
        c.created_at = c.updated_at = d
        c_str = c.__str__()
        self.assertIn("[City] ({})".format(c.id), c_str)
        self.assertIn("'id': '{}'".format(c.id), c_str)
        self.assertIn("'created_at': " + d_repr, c_str)
        self.assertIn("'updated_at': " + d_repr, c_str)


class TestStateToDictMethod(unittest.TestCase):
    """
    This class provides all possible test cases for to_dict method
    of class State.
    """

    def test_to_dict_type(self):
        c = City()
        self.assertTrue(dict, type(c.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        c = City()
        self.assertIn("id", c.to_dict())
        self.assertIn("created_at", c.to_dict())
        self.assertIn("updated_at", c.to_dict())
        self.assertIn("__class__", c.to_dict())

    def test_to_dict_contains_added_attributes(self):
        c = City()
        c.name = "Crazy"
        c.my_number = 98
        self.assertIn("name", c.to_dict())
        self.assertIn("my_number", c.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        c = City()
        c_dict = c.to_dict()
        self.assertEqual(str, type(c_dict["created_at"]))
        self.assertEqual(str, type(c_dict["updated_at"]))

    def test_to_dict_output(self):
        dts = dt.now()
        c = City()
        c.id = "123456"
        c.created_at = c.updated_at = dts
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dts.isoformat(),
            'updated_at': dts.isoformat()
        }
        self.assertDictEqual(c.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        c = City()
        self.assertNotEqual(c.to_dict(), c.__dict__)

    def test_to_dict_with_arg(self):
        c = City()
        with self.assertRaises(TypeError):
            c.to_dict(None)


class TestStateSaveMethod(unittest.TestCase):
    """
    This class provides all possible test cases for save method
    of class State.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        c = City()
        sp(0.05)
        first_updated_at = c.updated_at
        c.save()
        self.assertLess(first_updated_at, c.updated_at)

    def test_two_saves(self):
        c = City()
        sp(0.05)
        first_updated_at = c.updated_at
        c.save()
        self.assertLess(first_updated_at, c.updated_at)

    def test_two_saves(self):
        c = City()
        sp(0.05)
        first_updated_at = c.updated_at
        c.save()
        second_updated_at = c.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sp(0.05)
        c.save()
        self.assertLess(second_updated_at, c.updated_at)

    def test_save_with_arg(self):
        c = City()
        with self.assertRaises(TypeError):
            c.save(None)

    def test_save_updates_file(self):
        c = City()
        c.save()
        cid = "City." + c.id
        with open("file.json", "r") as f:
            self.assertIn(cid, f.read())


if __name__ == "__main__":
    unittest.main()
