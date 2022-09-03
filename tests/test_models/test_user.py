#!/usr/bin/python3

"""
File: test_user.py
Desc: This module contains all possible testcases for the user.py
      modlue in the models package. It uses the standard unittest.
Author: Gizachew Bayness (Elec Crazy) and Biruk Gelelcha
Date Created: Sep 2 2022
"""
import unittest
import models
from models.base_model import BaseModel
from models.user import User
from datetime import datetime as dt
from time import sleep as sp
import os


class TestUserObjectCreation(unittest.TestCase):
    """
    This class provides all possible test cases regarding object
    creation of class User.
    """

    def test_basic_creation(self):
        u = User()
        self.assertEqual(User, type(u))

    def test_if_parrent_class_is_BaseModel(self):
        self.assertIsInstance(User(), BaseModel)

    def test_two_objects_with_different_id(self):
        u1 = User()
        u2 = User()
        self.assertNotEqual(u1.id, u2.id)

    def test_if_id_is_string(self):
        u1 = User()
        self.assertEqual(type(u1.id), str)

    def test_type_of_created_at(self):
        u = User()
        self.assertEqual(dt, type(u.created_at))

    def test_type_of_updated_at(self):
        self.assertEqual(dt, type(User().updated_at))

    def test_the_stored_new_instance(self):
        u = User()
        self.assertIn(u, models.storage.all().values())

    def test_two_objects_with_different_created_at(self):
        u1 = User()
        u2 = User()
        self.assertGreater(u2.created_at, u1.created_at)

    def test_two_objects_with_different_updated_at(self):
        u1 = User()
        u2 = User()
        self.assertLess(u1.updated_at, u2.updated_at)

    def test_object_creation_with_only_args(self):
        u = User(None, 12, "hello")
        self.assertNotIn(None, models.storage.all().values())
        self.assertNotIn(12, models.storage.all().values())
        self.assertNotIn("hello", models.storage.all().values())

    def test_object_creation_with_args_and_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        u = User(22, id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(u.id, "000274")
        self.assertEqual(u.created_at, ts)
        self.assertEqual(u.updated_at, ts)

    def test_object_creation_with_only_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        u = User(id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(u.id, "000274")
        self.assertEqual(u.created_at, ts)
        self.assertEqual(u.updated_at, ts)

    def test_type_of_email(self):
        u = User()
        self.assertEqual(str, type(u.email))

    def test_type_of_password(self):
        u = User()
        self.assertEqual(str, type(u.password))

    def test_type_of_first_name(self):
        u = User()
        self.assertEqual(str, type(u.first_name))

    def test_type_of_last_name(self):
        u = User()
        self.assertEqual(type(u.last_name), str)

    def test_object_creation_with_None_values_kwargs(self):
        with self.assertRaises(TypeError):
            u = User(id=None, created_at=None, updated_at=None)


class TestUserStrMethod(unittest.TestCase):
    """
    This class provides all possible test cases for __str__ method
    of class User.
    """

    def test_simple_str_representation(self):
        u = User()
        u_str = u.__str__()
        self.assertIn("[User] ({})".format(u.id), u_str)

    def test_str_with_possible_attributes(self):
        d = dt.today()
        d_repr = repr(d)
        u = User("Elec Crazy")
        u.created_at = u.updated_at = d
        u_str = u.__str__()
        self.assertIn("[User] ({})".format(u.id), u_str)
        self.assertIn("'id': '{}'".format(u.id), u_str)
        self.assertIn("'created_at': " + d_repr, u_str)
        self.assertIn("'updated_at': " + d_repr, u_str)


class TestUserToDictMethod(unittest.TestCase):
    """
    This class provides all possible test cases for to_dict method
    of class User.
    """

    def test_to_dict_type(self):
        u = User()
        self.assertTrue(dict, type(u.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        u = User()
        self.assertIn("id", u.to_dict())
        self.assertIn("created_at", u.to_dict())
        self.assertIn("updated_at", u.to_dict())
        self.assertIn("__class__", u.to_dict())

    def test_to_dict_contains_added_attributes(self):
        u = User()
        u.name = "Elec Crazy"
        u.my_number = 98
        self.assertIn("name", u.to_dict())
        self.assertIn("my_number", u.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        u = User()
        u_dict = u.to_dict()
        self.assertEqual(str, type(u_dict["created_at"]))
        self.assertEqual(str, type(u_dict["updated_at"]))

    def test_to_dict_output(self):
        dts = dt.now()
        u = User()
        u.id = "123456"
        u.created_at = u.updated_at = dts
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dts.isoformat(),
            'updated_at': dts.isoformat()
        }
        self.assertDictEqual(u.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        u = User()
        self.assertNotEqual(u.to_dict(), u.__dict__)

    def test_to_dict_with_arg(self):
        u = User()
        with self.assertRaises(TypeError):
            u.to_dict(None)


class TestUserSaveMethod(unittest.TestCase):
    """
    This class provides all possible test cases for save method
    of class User.
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
        u = User()
        sp(0.05)
        first_updated_at = u.updated_at
        u.save()
        self.assertLess(first_updated_at, u.updated_at)

    def test_two_saves(self):
        u = User()
        sp(0.05)
        first_updated_at = u.updated_at
        u.save()
        self.assertLess(first_updated_at, u.updated_at)

    def test_two_saves(self):
        u = User()
        sp(0.05)
        first_updated_at = u.updated_at
        u.save()
        second_updated_at = u.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sp(0.05)
        u.save()
        self.assertLess(second_updated_at, u.updated_at)

    def test_save_with_arg(self):
        u = User()
        with self.assertRaises(TypeError):
            u.save(None)

    def test_save_updates_file(self):
        u = User()
        u.save()
        uid = "User." + u.id
        with open("file.json", "r") as f:
            self.assertIn(uid, f.read())


if __name__ == "__main__":
    unittest.main()
