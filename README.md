simple-conf-manager
=======

Define configuration structures, read and write config files and access your configuration via an object tree that plays well with IDE code completion.

---

+ [Description](#description)
+ [Requirements](#requirements)
+ [Installation](#installation)
+ [Usage](#usage)
    + [Defining configurations](#defining-configurations)
    + [Initializing configurations](#initializing-configurations)

---

Description
---

The standard python 'configparser' package is great at what it does, reading from and writing to configuration files, but falls short in terms of usability when employed in larger projects.
Keys defined in a config file must be provided as strings allowing for errors to creep in if config data must be accessed from different locations.
Importing numerous global values as a workaround is a nuisance and brings it's own set of drawbacks like writing to a config file during runtime and having to manage both the global variable and the config file.

With `simple-conf-manager` the configuration is defined as a "structure" in your code and is accessible for IDE code completion mechanisms, thus ruling out having to guess config keys during implementation.
Configurations are stored as object trees during runtime, values reside in attributes and can be changed with a simple assignment statement. Every change is directly written to the config file.


Requirements
----

Python 3.5 or later.


Installation
----

Install the `simple-conf-manager` package via pip by issuing the following command with the desired release `vX.X.X`: 

`pip install git+https://github.com/y-du/simple-conf-manager.git@vX.X.X` 

Upgrade to new version: 

`pip install --upgrade git+https://github.com/y-du/simple-conf-manager.git@vX.X.X`

Uninstall: 

`pip uninstall sepl-connector-client`


Usage
----

#### Defining configurations

#### Initializing configurations

