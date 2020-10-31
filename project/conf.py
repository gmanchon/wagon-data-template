

from collections.abc import Mapping

from colorama import Fore, Style

import yaml
import copy


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
    loads project and defaults yaml configuration files
    and provides a validated configuration object
    allows the objects consuming the configuration
    to easilly access the conf parameters in nested objects attributes
    """

    def __init__(self, project_conf_path, defaults_conf_path):
        """
        loads configuration from project and defaults yaml files
        processes validated conf
        """

        self.project_conf = self.__load_yaml_conf(project_conf_path)
        self.defaults_conf = self.__load_yaml_conf(defaults_conf_path)
        self.conf = copy.deepcopy(self.defaults_conf)
        self.__validate_conf(self.project_conf, self.conf)

    def __repr__(self):

        # getting representation of project, defaults and validated conf
        project_repr = repr(self.project_conf).split('\n')
        defaults_repr = repr(self.defaults_conf).split('\n')
        conf_repr = repr(self.conf).split('\n')

        # showing representation of validated configuration
        representation = []

        for conf_line in conf_repr:

            # checking if line is shared
            line_in_project = conf_line in project_repr
            line_in_defaults = conf_line in defaults_repr

            # appending representation
            if line_in_defaults:
                if line_in_project:
                    representation.append(conf_line)
                else:
                    representation.append(Fore.MAGENTA + conf_line
                                          + Style.RESET_ALL)
            else:
                representation.append(Fore.CYAN + conf_line + Style.RESET_ALL)

        return "\n".join(representation)

    def __load_yaml_conf(self, file_path):

        # yaml allows to benefit from an organised structure (a dictionary)
        # allowing to pass the conf to the consuming objects
        # conversion to the ConfStruct class allows
        # to access easilly conf elements using the dot notation

        # load conf file
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)

        # convert conf dictionary into ConfStruct object
        conf = ConfStruct(**config)

        return conf

    def __validate_conf(self, project_conf, defaults_conf):
        """
        processes conf object by iterating through defaults conf object
        and replacing values by project conf values when available
        """

        # iterate through defaults conf object
        for key, value in defaults_conf.__dict__.items():

            # checking whether key contains conf struct
            if isinstance(value, ConfStruct):

                # retrieve corresponding project conf
                if hasattr(project_conf, key):

                    # iterate recursively through conf struct representation
                    self.__validate_conf(getattr(project_conf, key), value)

            else:

                # validate other datatypes against project conf
                if hasattr(project_conf, key):

                    # validate project conf data type
                    if type(getattr(project_conf, key)) == type(value):

                        # replace defaults value with project value
                        setattr(defaults_conf, key, getattr(project_conf, key))

        # handle additional confs from project
        for key, value in project_conf.__dict__.items():

            # checking whether key exists in defaults
            if not hasattr(defaults_conf, key):

                # setting missing key
                setattr(defaults_conf, key, getattr(project_conf, key))
