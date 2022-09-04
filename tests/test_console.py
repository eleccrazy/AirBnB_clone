#!/usr/bin/python3

"""
File: test_console.py
Desc: This module contains all possible testcases for the console.py
      modlue. It uses the standard unittest.
Author: Gizachew Bayness (Elec Crazy) and Biruk Gelelcha
Date Created: Sep 4 2022
"""
import unittest
from console import HBNBCommand
from unittest.mock import patch
import sys
from io import StringIO


class TestConsolePromport(unittest.TestCase):
    """
    This class provides all possible test cases regarding prompt
    response of class HBNBCommand.
    """
    def test_output(self):
        self.assertEqual(HBNBCommand.prompt, "(hbnb) ")

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())
