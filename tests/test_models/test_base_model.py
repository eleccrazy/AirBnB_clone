#!/usr/bin/python3

"""
File: test_base_model.py
Desc: This module contains all possible testcases for the base_model.py
      modlue in the models package. It uses the standard unittest.
Author: Gizachew Bayness (Elec Crazy) and Biruk Gelelcha
Date Created: Sep 1 2022
"""
import unittest
import models
from models.base_model import BaseModel
from datetime import datetime as dt
from time import sleep as sp
import os


class TestBaseModelObjectCreation(unittest.TestCase):
    """
    This class provides all possible test cases regarding object
    creation of class BaseModel.
    """

    def test_basic_creation(self):
        b = BaseModel()
        self.assertEqual(BaseModel, type(b))

    def test_two_objects_with_different_id(self):
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def test_if_id_is_string(self):
        b1 = BaseModel()
        self.assertEqual(type(b1.id), str)

    def test_type_of_created_at(self):
        b = BaseModel()
        self.assertEqual(dt, type(b.created_at))

    def test_type_of_updated_at(self):
        self.assertEqual(dt, type(BaseModel().updated_at))

    def test_the_stored_new_instance(self):
        b = BaseModel()
        self.assertIn(b, models.storage.all().values())

    def test_two_objects_with_different_created_at(self):
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertGreater(b2.created_at, b1.created_at)

    def test_two_objects_with_different_updated_at(self):
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertLess(b1.updated_at, b2.updated_at)

    def test_object_creation_with_only_args(self):
        b = BaseModel(None, 12, "hello")
        self.assertNotIn(None, models.storage.all().values())
        self.assertNotIn(12, models.storage.all().values())
        self.assertNotIn("hello", models.storage.all().values())

    def test_object_creation_with_args_and_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        b = BaseModel(22, id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(b.id, "000274")
        self.assertEqual(b.created_at, ts)
        self.assertEqual(b.updated_at, ts)

    def test_object_creation_with_only_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        b = BaseModel(id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(b.id, "000274")
        self.assertEqual(b.created_at, ts)
        self.assertEqual(b.updated_at, ts)

    def test_object_creation_with_None_values_kwargs(self):
        with self.assertRaises(TypeError):
            b = BaseModel(id=None, created_at=None, updated_at=None)


class TestBaseModelStrMethod(unittest.TestCase):
    """
    This class provides all possible test cases for __str__ method
    of class BaseModel.
    """

    def test_simple_str_representation(self):
        b = BaseModel()
        b_str = b.__str__()
        self.assertIn("[BaseModel] ({})".format(b.id), b_str)

    def test_str_with_possible_attributes(self):
        d = dt.today()
        d_repr = repr(d)
        b = BaseModel("Elec Crazy")
        b.created_at = b.updated_at = d
        b_str = b.__str__()
        self.assertIn("[BaseModel] ({})".format(b.id), b_str)
        self.assertIn("'id': '{}'".format(b.id), b_str)
        self.assertIn("'created_at': " + d_repr, b_str)
        self.assertIn("'updated_at': " + d_repr, b_str)


class TestBaseModelToDictMethod(unittest.TestCase):
    """
    This class provides all possible test cases for to_dict method
    of class BaseModel.
    """

    def test_to_dict_type(self):
        b = BaseModel()
        self.assertTrue(dict, type(b.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        b = BaseModel()
        self.assertIn("id", b.to_dict())
        self.assertIn("created_at", b.to_dict())
        self.assertIn("updated_at", b.to_dict())
        self.assertIn("__class__", b.to_dict())

    def test_to_dict_contains_added_attributes(self):
        b = BaseModel()
        b.name = "Elec Crazy"
        b.my_number = 98
        self.assertIn("name", b.to_dict())
        self.assertIn("my_number", b.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        b = BaseModel()
        b_dict = b.to_dict()
        self.assertEqual(str, type(b_dict["created_at"]))
        self.assertEqual(str, type(b_dict["updated_at"]))

    def test_to_dict_output(self):
        dts = dt.now()
        b = BaseModel()
        b.id = "123456"
        b.created_at = b.updated_at = dts
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dts.isoformat(),
            'updated_at': dts.isoformat()
        }
        self.assertDictEqual(b.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        b = BaseModel()
        self.assertNotEqual(b.to_dict(), b.__dict__)

    def test_to_dict_with_arg(self):
        b = BaseModel()
        with self.assertRaises(TypeError):
            b.to_dict(None)


class TestBaseModelSaveMethod(unittest.TestCase):
    """
    This class provides all possible test cases for save method
    of class BaseModel.
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
        b = BaseModel()
        sp(0.05)
        first_updated_at = b.updated_at
        b.save()
        self.assertLess(first_updated_at, b.updated_at)

    def test_two_saves(self):
        b = BaseModel()
        sp(0.05)
        first_updated_at = b.updated_at
        b.save()
        second_updated_at = b.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sp(0.05)
        b.save()
        self.assertLess(second_updated_at, b.updated_at)

    def test_save_with_arg(self):
        b = BaseModel()
        with self.assertRaises(TypeError):
            b.save(None)

    def test_save_updates_file(self):
        b = BaseModel()
        b.save()
        bid = "BaseModel." + b.id
        with open("file.json", "r") as f:
            self.assertIn(bid, f.read())


if __name__ == "__main__":
    unittest.main()
