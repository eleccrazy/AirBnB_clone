#!/usr/bin/python3
"""
This module contains the the entry point of the command interpreter
for the AirBnB project.
"""
import re
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
    This function builds custom command line arguments for further
    processing.
    """
    return line.split()


def make_str_without_quotes(string):
    """
    This function reconstructes the str without quote
    """
    ret = ""
    for ch in string:
        if ch != "\"":
            ret += ch
    return ret


class HBNBCommand(cmd.Cmd):
    """
    Console for AirBnB project
    """
    prompt = "(hbnb) "

    classes = [
            'BaseModel', 'User', 'State', 'City',
            'Amenity', 'Place', 'Review'
            ]

    def emptyline(self):
        """
        Do nothing with empty line.
        """
        pass

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

        if len(args) > 0 and args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for o in storage.all().values():
                if len(args) > 0 and args[0] == type(o).__name__:
                    obj_list.append(o.__str__())
                elif len(args) == 0:
                    obj_list.append(o.__str__())
            print(obj_list)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        """
        args = build_args(line)
        obj_dict = storage.all()

        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args) == 4:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = valtype(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            for k, v in eval(args[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_instance_counter(self, line):
        """
        Counts the number of instances of a class
        """
        number_of_instances = 0
        for instance in storage.all().values():
            if build_args(line)[0] == type(instance).__name__:
                number_of_instances += 1

        print(number_of_instances)

    def default(self, line):
        """
        Method called on an input line when the command prefix is not
        recognized.
        """
        cmd_dict = {
                "all": self.do_all,
                "count": self.do_instance_counter,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "update": self.do_update,
                }

        pattern = re.compile(r"^(\w+)\.(\w+)\((.*)\)")
        matches = re.findall(pattern, line)
        if (not matches or len(matches[0]) < 2 or
                matches[0][0] not in HBNBCommand.classes or
                matches[0][1] not in cmd_dict.keys()):
            super().default(line)
            return

        if matches[0][1] == "all" or matches[0][1] == "count":
            cmd_dict[matches[0][1]](matches[0][0])
        elif matches[0][1] == "destroy" or matches[0][1] == "show":
            obj_id = matches[0][2][1:-1]
            cmd_dict[matches[0][1]](matches[0][0] + " " + obj_id)
        elif matches[0][1] == "update":
            pattern = re.compile(r"\"(.+?)\", (.+)")
            sub_match = re.match(pattern, matches[0][2]).groups()
            if sub_match[1][0] != '{':
                key_value = sub_match[1].split(", ")
                key = make_str_without_quotes(key_value[0])
                val = make_str_without_quotes(key_value[1])
                param = "{} {} {} {}".format(
                        matches[0][0], sub_match[0], key, val)
                cmd_dict[matches[0][1]](param)
            else:
                dict_repr = eval(sub_match[1])
                for k, v in dict_repr.items():
                    param = "{} {} {} {}".format(
                            matches[0][0], sub_match[0], k, v)
                    cmd_dict[matches[0][1]](param)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
