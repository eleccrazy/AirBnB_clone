import unittest
from console import HBNBCommand
from unittest.mock import patch
import sys
from io import StringIO


class TestConsolePrompt(unittest.TestCase):
    """
    This class provides all possible test cases regarding prompt
    response of class HBNBCommand.
    """
    def test_prompt_output(self):
        self.assertEqual(HBNBCommand.prompt, "(hbnb) ")

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())
