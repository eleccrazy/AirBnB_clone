#!/usr/bin/python3
"""
This module contains the the entry point of the command interpreter
for the AirBnB project.
"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


def build_args(line):
    """
    This function builds the custome command line arguments.
    """
    return line.split()


class HBNBCommand(cmd.Cmd):
    """
    Console for AirBnB project
    """
    prompt = "(hbnb) "

    classes = [
            'BaseModel', 'User', 'State', 'City',
            'Amenity', 'Place', 'Review'
            ]

    def do_quit(self, line):
        """
        Quits the program
        """
        return True

    def do_EOF(self, line):
        """
        Quits the program with EOF
        """
        print("")
        return True

    def do_create(self, line):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id.
        """
        args = build_args(line)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            print(eval(args[0])().id)
            storage.save()

    def do_show(self, line):
        """
        Prints the string representation of an instance based on the
        class name and id
        """
        args = build_args(line)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[f"{args[0]}.{args[1]}"])

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        """
        args = build_args(line)

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[f"{args[0]}.{args[1]}"]
            storage.save()

    def do_all(self, line):
        """
        Prints all string representation of all instances based
        or not on the class name.
        """
        args = build_args(line)

        if len(args) > 0:
            if args[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
        else:
            obj_list = []
            for o in storage.all().values():
                if len(args) > 1 and args[0] == type(o).__name__:
                    obj_list.append(o.__str__())
                elif len(args) == 0:
                    obj_list.append(o.__str__())
            print(obj_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        """


if __name__ == '__main__':
    HBNBCommand().cmdloop()
