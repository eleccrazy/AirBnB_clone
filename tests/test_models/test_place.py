#!/usr/bin/python3

"""
File: test_place.py
Desc: This module contains all possible testcases for the place.py
      modlue in the models package. It uses the standard unittest.
Author: Gizachew Bayness (Elec Crazy) and Biruk Gelelcha
Date Created: Sep 2 2022
"""
import unittest
import models
from models.base_model import BaseModel
from models.place import Place
from datetime import datetime as dt
from time import sleep as sp
import os


class TestPlaceObjectCreation(unittest.TestCase):
    """
    This class provides all possible test cases regarding object
    creation of class Place.
    """

    def test_basic_creation(self):
        p = Place()
        self.assertEqual(Place, type(p))

    def test_if_parrent_class_is_BaseModel(self):
        self.assertIsInstance(Place(), BaseModel)

    def test_two_objects_with_different_id(self):
        p1 = Place()
        p2 = Place()
        self.assertNotEqual(p1.id, p2.id)

    def test_if_id_is_string(self):
        p1 = Place()
        self.assertEqual(type(p1.id), str)

    def test_type_of_created_at(self):
        p = Place()
        self.assertEqual(dt, type(p.created_at))

    def test_type_of_updated_at(self):
        self.assertEqual(dt, type(Place().updated_at))

    def test_the_stored_new_instance(self):
        p = Place()
        self.assertIn(p, models.storage.all().values())

    def test_two_objects_with_different_created_at(self):
        p1 = Place()
        p2 = Place()
        self.assertGreater(p2.created_at, p1.created_at)

    def test_two_objects_with_different_updated_at(self):
        p1 = Place()
        p2 = Place()
        self.assertLess(p1.updated_at, p2.updated_at)

    def test_object_creation_with_only_args(self):
        p = Place(None, 12, "hello")
        self.assertNotIn(None, models.storage.all().values())
        self.assertNotIn(12, models.storage.all().values())
        self.assertNotIn("hello", models.storage.all().values())

    def test_object_creation_with_args_and_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        p = Place(22, id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(p.id, "000274")
        self.assertEqual(p.created_at, ts)
        self.assertEqual(p.updated_at, ts)

    def test_object_creation_with_only_kwargs(self):
        ts = dt.now()
        iso = ts.isoformat()
        p = Place(id="000274", created_at=iso, updated_at=iso)
        self.assertEqual(p.id, "000274")
        self.assertEqual(p.created_at, ts)
        self.assertEqual(p.updated_at, ts)

    def test_type_of_name(self):
        p = Place()
        self.assertEqual(type(p.name), str)

    def test_type_of_city_id(self):
        p = Place()
        self.assertEqual(type(p.city_id), str)

    def test_type_of_user_id(self):
        self.assertEqual(type(Place().city_id), str)

    def test_type_of_description(self):
        self.assertEqual(type(Place().description), str)

    def test_type_of_number_rooms(self):
        self.assertEqual(int, type(Place().number_rooms))

    def test_type_of_number_bathrooms(self):
        self.assertEqual(int, type(Place().number_bathrooms))

    def test_type_of_max_guest(self):
        self.assertEqual(int, type(Place().max_guest))

    def test_type_of_price_by_night(self):
        self.assertEqual(type(Place().price_by_night), int)

    def test_type_of_latitude(self):
        self.assertEqual(type(Place().latitude), float)

    def test_type_of_longitude(self):
        self.assertEqual(type(Place().longitude), float)

    def test_type_of_amenity_ids(self):
        self.assertEqual(type(Place().amenity_ids), list)

    def test_object_creation_with_None_values_kwargs(self):
        with self.assertRaises(TypeError):
            p = Place(id=None, created_at=None, updated_at=None)


class TestPlaceStrMethod(unittest.TestCase):
    """
    This class provides all possible test cases for __str__ method
    of class Place.
    """

    def test_simple_str_representation(self):
        p = Place()
        p_str = p.__str__()
        self.assertIn("[Place] ({})".format(p.id), p_str)

    def test_str_with_possible_attributes(self):
        d = dt.today()
        d_repr = repr(d)
        p = Place("Elec Crazy")
        p.created_at = p.updated_at = d
        p_str = p.__str__()
        self.assertIn("[Place] ({})".format(p.id), p_str)
        self.assertIn("'id': '{}'".format(p.id), p_str)
        self.assertIn("'created_at': " + d_repr, p_str)
        self.assertIn("'updated_at': " + d_repr, p_str)


class TestPlaceToDictMethod(unittest.TestCase):
    """
    This class provides all possible test cases for to_dict method
    of class Place.
    """

    def test_to_dict_type(self):
        p = Place()
        self.assertTrue(dict, type(p.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        p = Place()
        self.assertIn("id", p.to_dict())
        self.assertIn("created_at", p.to_dict())
        self.assertIn("updated_at", p.to_dict())
        self.assertIn("__class__", p.to_dict())

    def test_to_dict_contains_added_attributes(self):
        p = Place()
        p.name = "Elec Crazy"
        p.my_number = 98
        self.assertIn("name", p.to_dict())
        self.assertIn("my_number", p.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        p = Place()
        p_dict = p.to_dict()
        self.assertEqual(str, type(p_dict["created_at"]))
        self.assertEqual(str, type(p_dict["updated_at"]))

    def test_to_dict_output(self):
        dts = dt.now()
        p = Place()
        p.id = "123456"
        p.created_at = p.updated_at = dts
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dts.isoformat(),
            'updated_at': dts.isoformat()
        }
        self.assertDictEqual(p.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        p = Place()
        self.assertNotEqual(p.to_dict(), p.__dict__)

    def test_to_dict_with_arg(self):
        p = Place()
        with self.assertRaises(TypeError):
            p.to_dict(None)


class TestPlaceSaveMethod(unittest.TestCase):
    """
    This class provides all possible test cases for save method
    of class Place.
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
        p = Place()
        sp(0.05)
        first_updated_at = p.updated_at
        p.save()
        self.assertLess(first_updated_at, p.updated_at)

    def test_two_saves(self):
        p = Place()
        sp(0.05)
        first_updated_at = p.updated_at
        p.save()
        self.assertLess(first_updated_at, p.updated_at)

    def test_two_saves(self):
        p = Place()
        sp(0.05)
        first_updated_at = p.updated_at
        p.save()
        second_updated_at = p.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sp(0.05)
        p.save()
        self.assertLess(second_updated_at, p.updated_at)

    def test_save_with_arg(self):
        p = Place()
        with self.assertRaises(TypeError):
            p.save(None)

    def test_save_updates_file(self):
        p = Place()
        p.save()
        pid = "Place." + p.id
        with open("file.json", "r") as f:
            self.assertIn(pid, f.read())


if __name__ == "__main__":
    unittest.main()
