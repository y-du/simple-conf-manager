simple-conf-manager
=======

Define configuration structures, read and write config files and access your configuration via an object tree that plays well with IDE code completion.

---

+ [Description](#description)
+ [Quick start](#quick-start)
+ [Requirements](#requirements)
+ [Installation](#installation)
+ [Usage](#usage)
    + [Defining configurations](#defining-configurations)
    + [Initializing configurations](#initializing-configurations)
    + [Setting and getting values](#setting-and-getting-values)
    + [Overriding values via environment variables](#overriding-values-via-environment-variables)
    + [Logging](#logging)

---

Description
---

The standard python `configparser` package is great at what it does, reading from and writing to configuration files, but falls short in terms of usability when employed in larger projects.
Keys defined in a config file must be provided as strings, increasing the risk of errors if config data must be accessed from different locations.
Importing numerous global values as a workaround is a nuisance and brings it's own set of drawbacks like writing to a config file during runtime and having to manage both the global variable and the config file.

With `simple-conf-manager` the configuration is defined as a "structure" in your code and is accessible by IDE code completion mechanisms, thus ruling out having to guess config keys during implementation.
Configurations are stored as object trees during runtime, values reside in attributes and can be changed with a simple assignment statement. Every change is seamlessly written to the underlying config file.
See [Usage](#usage) for more information.


Quick start
---

    from simple_conf import configuration, section
    
    @configuration
    class MyConf:

        @section
        class MySection:
            val_1 = 123
            val_2 = "test"
            val_3 = True

    conf = MyConf("test.conf")
    
    print(conf.MySection.val_1) # -> 123
    conf.MySection.val_1 = 456  # set attribute and write to test.conf
    print(conf.MySection.val_1) # -> 456

Requirements
----

Python 3.5 or later.


Installation
----

Install the `simple-conf-manager` package via pip by issuing the following command with the desired release `X.X.X`: 

- `pip install git+https://github.com/y-du/simple-conf-manager.git@X.X.X` 

Upgrade to new version: 

- `pip install --upgrade git+https://github.com/y-du/simple-conf-manager.git@X.X.X`

Uninstall: 

- `pip uninstall simple-conf-manager`


Usage
----

#### Defining configurations

To create a configuration create a `class` and decorate it with `@configuration`.
Within this class you add sections to your configuration by creating further classes and decorating them with `@section`.
Sections house the keys and default values in the form of class attributes.
There's no limit to how many configurations you create just make sure to use different config files.

    from simple_conf import configuration, section
    
    @configuration
    class MyConf:

        @section
        class MySection:
            key = "value"


#### Initializing configurations

To use your configuration you must instantiate it first. 
Multiple instantiations of the same configuration will always yield the same instance. 
By using the `@configuration` decorator the init signature changes:

    conf = MyConf(conf_file, user_path=None, ext_aft_crt=True, pers_def=True, load=True)

- `conf_file` required, name of the config file as a string.

- `user_path` by default config files are created in the current working dictionary, provide a custom path as a string if a different location is desired.

- `ext_aft_crt` exit the script after config file creation, set to `False` if execution should continue.

- `pers_def` if a key's value is removed from the config file and a default value exists write back the default value, if the value is to remain empty set to `False`.

- `load` if set to `False` loading from the configuration file can be deferred and triggered manually with the provided `loadConfig` function at a later point in time.
    
        my_conf = MyConf("my_conf.conf", load=False)
        
        # do something
        # my_conf will access the default values of MyConf during this time
        
        loadConfig(my_conf) 


#### Setting and getting values

During runtime values are stored in attributes housed in objects representing the respective sections.
Setting and getting values is straightforward:
 
    configuration.section.key = "value" # set

    value = configuration.section.key   # get

Possible types are: `str`, `int`, `float`, `complex`, `bool`, `NoneType`. Other types will be treated as strings.


#### Overriding values via environment variables

Values of keys can be temporarily overridden by setting environment variables with the following naming scheme:

`CONFIGURATION_SECTION="key_1:value;key_2:value; ... key_x:value"`

During initialization `simple-conf-manager` will check if matching environment variables exist and set the values for the provided keys.
Not all keys of a section must be provided but it's important to delimit keys and their values with `:` and key-value pairs with `;`.

For example if `key_a` and `key_b` of the below configuration are to be overridden:

    @configuration
    class MyConf:

        @section
        class MySection:
            key_a = "Ham"
            key_b = False
            key_c = 123

The corresponding environment variable should be defined as follows:

`MYCONF_MYSECTION="key_a:Spam;key_b:True"`


#### Logging

If your project uses the python `logging` facility you can combine the output produced by `simple-conf-manager` with your log output.

Retrieve the "simple-conf" logger via:

    logger = logging.getLogger("simple-conf")

Add your handler to the logger and optionally set the desired level:

    logger.addHandler(your_handler)
    logger.setLevel(logging.INFO)   # optional
