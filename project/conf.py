

from collections.abc import Mapping

import yaml


# https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
class ConfStruct:
    """
    converts a dictionary into nested objects having attributes
    containing the values of the dictionary
    given `d = { "a": { "b": { "c": True, "d": [1, 2, 3], "e": ", "f": 5 } } }`
    `s = ConfStruct(**d)` allows to access conf using the dot notation `s.a.b.d`
    """

    def __init__(self, **entries):
        """
        iterates through the provided dictionary
        non mapping data types are stored in instance variables
        mapping data types are stored as conf structs in instance variables
        """

        # convert dictionary parameter into nested objects and attributes
        for key, value in entries.items():

            # checking whether key contains a dictionary
            if isinstance(value, Mapping):

                # iterate recursively through sub dictionary
                # and store resulting object into structure
                self.__dict__[key] = ConfStruct(**value)

            else:

                # other datatypes are stored as provided
                # into the structure
                self.__dict__[key] = value

    def __repr__(self):
        """
        builds a visual representation of the loaded data
        using the example in the initializer:
        `a.b.c = True
        a.b.d = [1, 2, 3]
        a.b.e = ''
        a.b.f = 5`
        """

        representation = ""

        # iterate through instance variables
        for key, value in self.__dict__.items():

            # checking whether key contains conf struct
            if isinstance(value, ConfStruct):

                # iterate recursively through conf struct representation
                representation += f"\n{key}.".join(repr(value).split("\n"))

            else:

                # other datatypes are displayed using default repr
                representation += f"\n{key} = {repr(value)}"

        return representation


class ConfLoader():
    """
    loads yaml configuration file and returns an object
    allowing the objects consuming the configuration
    to easilly access the conf parameters in nested objects attributes
    """

    def __init__(self, yaml_path):

        self.yaml_path = yaml_path
        self.conf = self.__load_yaml_conf(yaml_path)

    def __repr__(self):

        # showing representation of loaded configuration
        return repr(self.conf)

    def __load_yaml_conf(self, yaml_path):

        # yaml allows to benefit from an organised structure (a dictionary)
        # allowing to pass the conf to the consuming objects
        # conversion to the ConfStruct class allows
        # to access easilly conf elements using the dot notation

        # load conf file
        with open(yaml_path, "r") as file:
            config = yaml.safe_load(file)

        # convert conf dictionary into ConfStruct object
        conf = ConfStruct(**config)

        return conf
