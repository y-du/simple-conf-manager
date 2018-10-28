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

__version__ = '0.2.5'
__title__ = 'simple-conf-manager'
__description__ = ''
__url__ = 'https://github.com/y-du/simple-conf-manager'
__author__ = 'Yann Dumont'
__license__ = 'Apache License 2.0'
__copyright__ = 'Copyright (c) 2018 Yann Dumont'


import os, inspect, configparser


class _Configuration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, conf_file, user_path=None, ext_aft_crt=True):
        sections = {item.__name__: item(self.__setKey) for item in self.__class__.__dict__.values() if inspect.isclass(item) and issubclass(item, _Section)}
        self.__dict__ = {**self.__dict__ , **sections}
        self.__conf_path = user_path if user_path else os.path.abspath(os.path.split(inspect.getfile(inspect.stack()[-1].frame))[0])
        self.__conf_file = conf_file
        self.__parser = configparser.ConfigParser()

        if not os.path.isfile(os.path.join(self.__conf_path, self.__conf_file)):
            print("Config file '{}' not found".format(self.__conf_file))
            for key, section in sections.items():
                self.__parser.add_section(key)
                for ky, value in {k: v for k, v in sections[key].__dict__.items() if not k.startswith('_')}.items():
                    self.__parser.set(section=key, option=ky, value=self.__dumpValue(value))
            self.__writeConfFile()
            print("Created config file '{}' at '{}'".format(self.__conf_file, self.__conf_path))
            if ext_aft_crt:
                exit()

        if not self.__parser.sections():
            try:
                print("Opening config file '{}' at '{}'".format(self.__conf_file, self.__conf_path))
                self.__parser.read(os.path.join(self.__conf_path, self.__conf_file))
                self.__loadConfig(sections)
            except Exception as ex:
                print(ex)

    def __loadConfig(self, sections):
        missing_sections, unknown_sections, known_sections = self.__diff(sections, self.__parser.sections())
        print("Checking sections ...")
        for key in unknown_sections:
            print("Ignoring unknown section '{}'".format(key))
        for key in missing_sections:
            print("Adding new section '{}'".format(key))
            self.__parser.add_section(key)
            for ky, value in {k: v for k, v in sections[key].__dict__.items() if not k.startswith('_')}.items():
                self.__parser.set(section=key, option=ky, value=self.__dumpValue(value))
        for key in known_sections:
            print("Checking keys of section '{}'".format(key))
            missing_keys, unknown_keys, known_keys = self.__diff([ky for ky in sections[key].__dict__.keys() if not ky.startswith('_')], tuple(self.__parser[key].keys()))
            for ky in unknown_keys:
                print("Ignoring unknown key '{}' in section '{}'".format(ky, key))
            for ky in missing_keys:
                print("Adding new key '{}' in section '{}'".format(ky, key))
                self.__parser.set(section=key, option=ky, value=self.__dumpValue(sections[key].__dict__[ky]))
            for ky in known_keys:
                print("Retrieving value of key '{}' in section '{}'".format(ky, key))
                value = self.__loadValue(self.__parser.get(section=key, option=ky))
                if type(value) != type(None):
                    sections[key].__dict__[ky] = value
        self.__writeConfFile()

    def __dumpValue(self, value):
        return str(value) if type(value) != type(None) else ''

    def __loadValue(self, value: str):
        if len(value) == 0:
            return None
        elif value.isalpha():
            if value in 'True':
                return True
            elif value in 'False':
                return False
            else:
                return value
        else:
            try:
                return int(value)
            except ValueError:
                pass
            try:
                return float(value)
            except ValueError:
                pass
            try:
                return complex(value)
            except ValueError:
                pass
            return value

    def __sectionToDict(self, section):
        return {key: section.__dict__[key] if type(section.__dict__[key]) == str else str(section.__dict__[key]) if section.__dict__[key] else '' for key in section.__dict__.keys() if not key.startswith('_')}

    def __diff(self, known, unknown):
        known_set = set(known)
        unknown_set = set(unknown)
        missing = known_set - unknown_set
        new = unknown_set - known_set
        intersection = known_set.intersection(unknown_set)
        return missing, new, intersection

    def __writeConfFile(self):
        try:
            with open(os.path.join(self.__conf_path, self.__conf_file), 'w') as cf:
                self.__parser.write(cf)
        except Exception as ex:
            print(ex)

    def __setKey(self, section, key, value):
        self.__parser.set(section=section, option=key, value=self.__dumpValue(value))
        self.__writeConfFile()


def configuration(cls):
    attr_dict = cls.__dict__.copy()
    del attr_dict['__dict__']
    del attr_dict['__weakref__']
    sub_cls = type(cls.__name__, (_Configuration,), attr_dict)
    sub_cls.__qualname__ = cls.__qualname__
    return sub_cls

class _Section:

    def __init__(self, setCallbk):
        for key, value in [(key, value) for key, value in self.__class__.__dict__.items() if not key.startswith('_')]:
            self.__dict__[key] = value
        self.__dict__['_setCallbk'] = setCallbk

    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            super().__setattr__(key, value)
            self._setCallbk(str(self.__class__.__name__), key, value)
        else:
            err_msg = "assignment of new attribute '{}' to '{}' not allowed".format(key, self.__class__.__qualname__)
            raise AttributeError(err_msg)

def section(cls):
    attr_dict = cls.__dict__.copy()
    del attr_dict['__dict__']
    del attr_dict['__weakref__']
    sub_cls = type(cls.__name__, (_Section, ), attr_dict)
    sub_cls.__qualname__ = cls.__qualname__
    return sub_cls
