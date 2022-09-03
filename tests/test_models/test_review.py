#!/usr/bin/python3

"""
File: test_review.py
Desc: This module contains all possible testcases for the review.py
      modlue in the models package. It uses the standard unittest.
Author: Gizachew Bayness (Elec Crazy) and Biruk Gelelcha
Date Created: Sep 3 2022
"""
import unittest
import models
from models.base_model import BaseModel
from models.review import Review
from datetime import datetime as dt
from time import sleep as sp
import os


class TestReviewObjectCreation(unittest.TestCase):
    """
    This class provides all possible test cases regarding object
    creation of class Review.
    """

    def test_basic_creation(self):
        r = Review()
        self.assertEqual(Review, type(r))

    def test_if_parrent_class_is_BaseModel(self):
        self.assertIsInstance(Review(), BaseModel)

    def test_two_objects_with_different_id(self):
        r1 = Review()
        r2 = Review()
        self.assertNotEqual(r1.id, r2.id)

    def test_if_id_is_string(self):
        r1 = Review()
        self.assertEqual(type(r1.id), str)

    def test_type_of_created_at(self):
        r = Review()
        self.assertEqual(dt, type(r.created_at))

    def test_type_of_updated_at(self):
        self.assertEqual(dt, type(Review().updated_at))

    def test_the_stored_new_instance(self):
        r = Review()
        self.assertIn(r, models.storage.all().values())

    def test_two_objects_with_different_created_at(self):
        r1 = Review()
        r2 = Review()
        self.assertGreater(r2.created_at, r1.created_at)

    def test_two_objects_with_different_updated_at(self):
        r1 = Review()
        r2 = Review()
        self.assertLess(r1.updated_at, r2.updated_at)

    def test_object_creation_with_only_args(self):
        r = Review(None, 12, "hello")
        self.assertNotIn(None, models.storage.all().values())
        self.assertNotIn(12, models.storage.all().values())
        self.assertNotIn("hello", models.storage.all().values())

    def test_object_creation_with_args_and_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        r = Review(22, id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(r.id, "000274")
        self.assertEqual(r.created_at, ts)
        self.assertEqual(r.updated_at, ts)

    def test_object_creation_with_only_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        r = Review(id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(r.id, "000274")
        self.assertEqual(r.created_at, ts)
        self.assertEqual(r.updated_at, ts)

    def test_type_of_text(self):
        r = Review()
        self.assertEqual(str, type(r.text))

    def test_type_of_place_id(self):
        self.assertEqual(type(Review().place_id), str)

    def test_type_of_user_id(self):
        self.assertEqual(type(Review().user_id), str)

    def test_object_creation_with_None_values_kwargs(self):
        with self.assertRaises(TypeError):
            r = Review(id=None, created_at=None, updated_at=None)


class TestReviewStrMethod(unittest.TestCase):
    """
    This class provides all possible test cases for __str__ method
    of class Review.
    """

    def test_simple_str_representation(self):
        r = Review()
        r_str = r.__str__()
        self.assertIn("[Review] ({})".format(r.id), r_str)

    def test_str_with_possible_attributes(self):
        d = dt.today()
        d_repr = repr(d)
        r = Review("Elec Crazy")
        r.created_at = r.updated_at = d
        r_str = r.__str__()
        self.assertIn("[Review] ({})".format(r.id), r_str)
        self.assertIn("'id': '{}'".format(r.id), r_str)
        self.assertIn("'created_at': " + d_repr, r_str)
        self.assertIn("'updated_at': " + d_repr, r_str)


class TestReviewToDictMethod(unittest.TestCase):
    """
    This class provides all possible test cases for to_dict method
    of class Review.
    """

    def test_to_dict_type(self):
        r = Review()
        self.assertTrue(dict, type(r.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        r = Review()
        self.assertIn("id", r.to_dict())
        self.assertIn("created_at", r.to_dict())
        self.assertIn("updated_at", r.to_dict())
        self.assertIn("__class__", r.to_dict())

    def test_to_dict_contains_added_attributes(self):
        r = Review()
        r.name = "Crazy"
        r.my_number = 98
        self.assertIn("name", r.to_dict())
        self.assertIn("my_number", r.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        r = Review()
        r_dict = r.to_dict()
        self.assertEqual(str, type(r_dict["created_at"]))
        self.assertEqual(str, type(r_dict["updated_at"]))

    def test_to_dict_output(self):
        dts = dt.now()
        r = Review()
        r.id = "123456"
        r.created_at = r.updated_at = dts
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dts.isoformat(),
            'updated_at': dts.isoformat()
        }
        self.assertDictEqual(r.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        r = Review()
        self.assertNotEqual(r.to_dict(), r.__dict__)

    def test_to_dict_with_arg(self):
        r = Review()
        with self.assertRaises(TypeError):
            r.to_dict(None)


class TestReviewSaveMethod(unittest.TestCase):
    """
    This class provides all possible test cases for save method
    of class Review.
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
        r = Review()
        sp(0.05)
        first_updated_at = r.updated_at
        r.save()
        self.assertLess(first_updated_at, r.updated_at)

    def test_two_saves(self):
        r = Review()
        sp(0.05)
        first_updated_at = r.updated_at
        r.save()
        self.assertLess(first_updated_at, r.updated_at)

    def test_two_saves(self):
        r = Review()
        sp(0.05)
        first_updated_at = r.updated_at
        r.save()
        second_updated_at = r.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sp(0.05)
        r.save()
        self.assertLess(second_updated_at, r.updated_at)

    def test_save_with_arg(self):
        r = Review()
        with self.assertRaises(TypeError):
            r.save(None)

    def test_save_updates_file(self):
        r = Review()
        r.save()
        rid = "Review." + r.id
        with open("file.json", "r") as f:
            self.assertIn(rid, f.read())


if __name__ == "__main__":
    unittest.main()
