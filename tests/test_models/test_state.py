#!/usr/bin/python3

"""
File: test_state.py
Desc: This module contains all possible testcases for the state.py
      modlue in the models package. It uses the standard unittest.
Author: Gizachew Bayness (Elec Crazy) and Biruk Gelelcha
Date Created: Sep 2 2022
"""
import unittest
import models
from models.base_model import BaseModel
from models.state import State
from datetime import datetime as dt
from time import sleep as sp
import os


class TestStateObjectCreation(unittest.TestCase):
    """
    This class provides all possible test cases regarding object
    creation of class User.
    """

    def test_basic_creation(self):
        s = State()
        self.assertEqual(State, type(s))

    def test_if_parrent_class_is_BaseModel(self):
        self.assertIsInstance(State(), BaseModel)

    def test_two_objects_with_different_id(self):
        s1 = State()
        s2 = State()
        self.assertNotEqual(s1.id, s2.id)

    def test_if_id_is_string(self):
        s1 = State()
        self.assertEqual(type(s1.id), str)

    def test_type_of_created_at(self):
        s = State()
        self.assertEqual(dt, type(s.created_at))

    def test_type_of_updated_at(self):
        self.assertEqual(dt, type(State().updated_at))

    def test_the_stored_new_instance(self):
        s = State()
        self.assertIn(s, models.storage.all().values())

    def test_two_objects_with_different_created_at(self):
        s1 = State()
        s2 = State()
        self.assertGreater(s2.created_at, s1.created_at)

    def test_two_objects_with_different_updated_at(self):
        s1 = State()
        s2 = State()
        self.assertLess(s1.updated_at, s2.updated_at)

    def test_object_creation_with_only_args(self):
        s = State(None, 12, "hello")
        self.assertNotIn(None, models.storage.all().values())
        self.assertNotIn(12, models.storage.all().values())
        self.assertNotIn("hello", models.storage.all().values())

    def test_object_creation_with_args_and_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        s = State(22, id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(s.id, "000274")
        self.assertEqual(s.created_at, ts)
        self.assertEqual(s.updated_at, ts)

    def test_object_creation_with_only_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        s = State(id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(s.id, "000274")
        self.assertEqual(s.created_at, ts)
        self.assertEqual(s.updated_at, ts)

    def test_type_of_name(self):
        s = State()
        self.assertEqual(str, type(s.name))

    def test_object_creation_with_None_values_kwargs(self):
        with self.assertRaises(TypeError):
            s = State(id=None, created_at=None, updated_at=None)


class TestStateStrMethod(unittest.TestCase):
    """
    This class provides all possible test cases for __str__ method
    of class State.
    """

    def test_simple_str_representation(self):
        s = State()
        s_str = s.__str__()
        self.assertIn("[State] ({})".format(s.id), s_str)

    def test_str_with_possible_attributes(self):
        d = dt.today()
        d_repr = repr(d)
        s = State("Elec Crazy")
        s.created_at = s.updated_at = d
        s_str = s.__str__()
        self.assertIn("[State] ({})".format(s.id), s_str)
        self.assertIn("'id': '{}'".format(s.id), s_str)
        self.assertIn("'created_at': " + d_repr, s_str)
        self.assertIn("'updated_at': " + d_repr, s_str)


class TestStateToDictMethod(unittest.TestCase):
    """
    This class provides all possible test cases for to_dict method
    of class State.
    """

    def test_to_dict_type(self):
        s = State()
        self.assertTrue(dict, type(s.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        s = State()
        self.assertIn("id", s.to_dict())
        self.assertIn("created_at", s.to_dict())
        self.assertIn("updated_at", s.to_dict())
        self.assertIn("__class__", s.to_dict())

    def test_to_dict_contains_added_attributes(self):
        s = State()
        s.name = "Crazy"
        s.my_number = 98
        self.assertIn("name", s.to_dict())
        self.assertIn("my_number", s.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        s = State()
        s_dict = s.to_dict()
        self.assertEqual(str, type(s_dict["created_at"]))
        self.assertEqual(str, type(s_dict["updated_at"]))

    def test_to_dict_output(self):
        dts = dt.now()
        s = State()
        s.id = "123456"
        s.created_at = s.updated_at = dts
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dts.isoformat(),
            'updated_at': dts.isoformat()
        }
        self.assertDictEqual(s.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        s = State()
        self.assertNotEqual(s.to_dict(), s.__dict__)

    def test_to_dict_with_arg(self):
        s = State()
        with self.assertRaises(TypeError):
            s.to_dict(None)


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
        s = State()
        sp(0.05)
        first_updated_at = s.updated_at
        s.save()
        self.assertLess(first_updated_at, s.updated_at)

    def test_two_saves(self):
        s = State()
        sp(0.05)
        first_updated_at = s.updated_at
        s.save()
        self.assertLess(first_updated_at, s.updated_at)

    def test_two_saves(self):
        s = State()
        sp(0.05)
        first_updated_at = s.updated_at
        s.save()
        second_updated_at = s.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sp(0.05)
        s.save()
        self.assertLess(second_updated_at, s.updated_at)

    def test_save_with_arg(self):
        s = State()
        with self.assertRaises(TypeError):
            s.save(None)

    def test_save_updates_file(self):
        s = State()
        s.save()
        sid = "State." + s.id
        with open("file.json", "r") as f:
            self.assertIn(sid, f.read())


if __name__ == "__main__":
    unittest.main()
