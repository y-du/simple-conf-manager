"""
   Copyright 2018 Yann Dumont

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__version__ = '0.1.1'


import os, inspect, configparser


class Configuration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, conf_file, user_path=None, exit_after_create=True):
        self.__section_classes = {item.__name__: item for item in self.__class__.__dict__.values() if inspect.isclass(item) and issubclass(item, Section)}
        #self.__dict__ = {**self.__dict__ , **self.__sections}
        self.__conf_path = user_path if user_path else os.path.abspath(os.path.split(inspect.getfile(inspect.stack()[-1].frame))[0])
        self.__conf_file = conf_file
        self.__parser = configparser.ConfigParser()

        if not os.path.isfile(os.path.join(self.__conf_path, self.__conf_file)):
            print("Config file '{}' not found".format(self.__conf_file))
            for section in self.__section_classes.values():
                self.__parser[section.__name__] = self.__sectionClassToDict(section)
            self.__writeConfFile()
            print("Created config file '{}' at '{}'".format(self.__conf_file, self.__conf_path))
            if exit_after_create:
                exit()

        if not self.__parser.sections():
            try:
                print("Opening config file '{}' at '{}'".format(self.__conf_file, self.__conf_path))
                self.__parser.read(os.path.join(self.__conf_path, self.__conf_file))
                self.__loadConfig()
            except Exception as ex:
                print(ex)

    def __loadConfig(self):
        missing_sections, unknown_sections = self.__diff(self.__section_classes, self.__parser.sections())
        print("Checking sections ...")
        for key in unknown_sections:
            print("Ignoring unknown section '{}'".format(key))
            #self.__parser.remove_section(key)
        for key in missing_sections:
            print("Adding new section '{}'".format(key))
            self.__parser[key] = self.__sectionClassToDict(self.__section_classes[key])
            #self.__dict__[key] = self.__section_classes[key](self.__setKey)
        print("Checking keys ...")
        for key, section in self.__section_classes.items():
            #missing_keys, unknown_keys = self.__diff(self.__section_classes[key])
            print(self.__section_classes[key].__dict__)
            print(dict(self.__parser[key].items()))
        self.__writeConfFile()

    def __sectionClassToDict(self, cls):
        return {i: cls.__dict__[i] if type(cls.__dict__[i]) == str else str(cls.__dict__[i]) if cls.__dict__[i] else '' for i in cls.__dict__.keys() if not i.startswith('_')}

    def __diff(self, known, unknown):
        known_set = set(known)
        unknown_set = set(unknown)
        missing = known_set - unknown_set
        new = unknown_set - known_set
        return missing, new

    def __writeConfFile(self):
        try:
            with open(os.path.join(self.__conf_path, self.__conf_file), 'w') as cf:
                self.__parser.write(cf)
        except Exception as ex:
            print(ex)

    def __setKey(self, section, key, value):
        self.__parser.set(section=section, option=key, value=value if type(value) == str else str(value) if value else '')
        self.__writeConfFile()


class Section:

    def __init__(self, setCallbk):
        for key, value in [(key, value) for key, value in self.__class__.__dict__.items() if not key.startswith('_')]:
            self.__dict__[key] = value
        self.__dict__['setCallbk'] = setCallbk

    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            super().__setattr__(key, value)
            self.setCallbk(str(self.__class__.__name__), key, value)
        else:
            err_msg = "assignment of new attribute '{}' to '{}' not allowed".format(key, self.__class__.__qualname__)
            raise AttributeError(err_msg)
