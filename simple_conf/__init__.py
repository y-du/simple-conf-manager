"""
   Copyright 2019 Yann Dumont

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

__version__ = '0.5.0'
__title__ = 'simple-conf-manager'
__description__ = 'Define configuration structures, read and write config files and access your configuration via an object tree that plays well with IDE code completion.'
__url__ = 'https://github.com/y-du/simple-conf-manager'
__author__ = 'Yann Dumont'
__license__ = 'Apache License 2.0'
__copyright__ = 'Copyright (c) 2018 Yann Dumont'


from ._manager import configuration, section, initConfig
