#!/usr/bin/python3

"""
File: test_amenity.py
Desc: This module contains all possible testcases for the amenity.py
      modlue in the models package. It uses the standard unittest.
Author: Gizachew Bayness (Elec Crazy) and Biruk Gelelcha
Date Created: Sep 2 2022
"""
import unittest
import models
from models.base_model import BaseModel
from models.amenity import Amenity
from datetime import datetime as dt
from time import sleep as sp
import os


class TestUserObjectCreation(unittest.TestCase):
    """
    This class provides all possible test cases regarding object
    creation of class Amenity.
    """

    def test_basic_creation(self):
        a = Amenity()
        self.assertEqual(Amenity, type(a))

    def test_if_parrent_class_is_BaseModel(self):
        self.assertIsInstance(Amenity(), BaseModel)

    def test_two_objects_with_different_id(self):
        a1 = Amenity()
        a2 = Amenity()
        self.assertNotEqual(a1.id, a2.id)

    def test_if_id_is_string(self):
        a1 = Amenity()
        self.assertEqual(type(a1.id), str)

    def test_type_of_created_at(self):
        a = Amenity()
        self.assertEqual(dt, type(a.created_at))

    def test_type_of_updated_at(self):
        self.assertEqual(dt, type(Amenity().updated_at))

    def test_the_stored_new_instance(self):
        a = Amenity()
        self.assertIn(a, models.storage.all().values())

    def test_two_objects_with_different_created_at(self):
        a1 = Amenity()
        a2 = Amenity()
        self.assertGreater(a2.created_at, a1.created_at)

    def test_two_objects_with_different_updated_at(self):
        a1 = Amenity()
        a2 = Amenity()
        self.assertLess(a1.updated_at, a2.updated_at)

    def test_object_creation_with_only_args(self):
        a = Amenity(None, 12, "hello")
        self.assertNotIn(None, models.storage.all().values())
        self.assertNotIn(12, models.storage.all().values())
        self.assertNotIn("hello", models.storage.all().values())

    def test_object_creation_with_args_and_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        a = Amenity(22, id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(a.id, "000274")
        self.assertEqual(a.created_at, ts)
        self.assertEqual(a.updated_at, ts)

    def test_object_creation_with_only_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        a = Amenity(id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(a.id, "000274")
        self.assertEqual(a.created_at, ts)
        self.assertEqual(a.updated_at, ts)

    def test_type_of_name(self):
        a = Amenity()
        self.assertEqual(type(a.name), str)

    def test_object_creation_with_None_values_kwargs(self):
        with self.assertRaises(TypeError):
            a = Amenity(id=None, created_at=None, updated_at=None)


class TestAmenityStrMethod(unittest.TestCase):
    """
    This class provides all possible test cases for __str__ method
    of class Amenity.
    """

    def test_simple_str_representation(self):
        a = Amenity()
        a_str = a.__str__()
        self.assertIn("[Amenity] ({})".format(a.id), a_str)

    def test_str_with_possible_attributes(self):
        d = dt.today()
        d_repr = repr(d)
        a = Amenity("Elec Crazy")
        a.created_at = a.updated_at = d
        a_str = a.__str__()
        self.assertIn("[Amenity] ({})".format(a.id), a_str)
        self.assertIn("'id': '{}'".format(a.id), a_str)
        self.assertIn("'created_at': " + d_repr, a_str)
        self.assertIn("'updated_at': " + d_repr, a_str)


class TestAmenityToDictMethod(unittest.TestCase):
    """
    This class provides all possible test cases for to_dict method
    of class Amenity.
    """

    def test_to_dict_type(self):
        a = Amenity()
        self.assertTrue(dict, type(a.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        a = Amenity()
        self.assertIn("id", a.to_dict())
        self.assertIn("created_at", a.to_dict())
        self.assertIn("updated_at", a.to_dict())
        self.assertIn("__class__", a.to_dict())

    def test_to_dict_contains_added_attributes(self):
        a = Amenity()
        a.name = "Elec Crazy"
        a.my_number = 98
        self.assertIn("name", a.to_dict())
        self.assertIn("my_number", a.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        a = Amenity()
        a_dict = a.to_dict()
        self.assertEqual(str, type(a_dict["created_at"]))
        self.assertEqual(str, type(a_dict["updated_at"]))

    def test_to_dict_output(self):
        dts = dt.now()
        a = Amenity()
        a.id = "123456"
        a.created_at = a.updated_at = dts
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dts.isoformat(),
            'updated_at': dts.isoformat()
        }
        self.assertDictEqual(a.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        a = Amenity()
        self.assertNotEqual(a.to_dict(), a.__dict__)

    def test_to_dict_with_arg(self):
        a = Amenity()
        with self.assertRaises(TypeError):
            a.to_dict(None)


class TestAmenitySaveMethod(unittest.TestCase):
    """
    This class provides all possible test cases for save method
    of class Amenity.
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
        a = Amenity()
        sp(0.05)
        first_updated_at = a.updated_at
        a.save()
        self.assertLess(first_updated_at, a.updated_at)

    def test_two_saves(self):
        a = Amenity()
        sp(0.05)
        first_updated_at = a.updated_at
        a.save()
        self.assertLess(first_updated_at, a.updated_at)

    def test_two_saves(self):
        a = Amenity()
        sp(0.05)
        first_updated_at = a.updated_at
        a.save()
        second_updated_at = a.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sp(0.05)
        a.save()
        self.assertLess(second_updated_at, a.updated_at)

    def test_save_with_arg(self):
        a = Amenity()
        with self.assertRaises(TypeError):
            a.save(None)

    def test_save_updates_file(self):
        a = Amenity()
        a.save()
        aid = "Amenity." + a.id
        with open("file.json", "r") as f:
            self.assertIn(aid, f.read())


if __name__ == "__main__":
    unittest.main()
