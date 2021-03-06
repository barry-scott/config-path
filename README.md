# config-path
Python library to work out witch path to use for configuration folders
and files in an operating system independent way.

Each operating system has particular conventions for where an application is expected
to stores it configuration. The information provided to ConfigPath is used
to figure out an appropiate file path or folder path for the application's
configuration data.

Supports Windows, macOS and most unix systems using the 'XDG Base Directory Specification'.

~~~~
ConfigPath( appname, vendor, filetype )
~~~~

The `vendor` should be the domain name of the application provider.
The `appname` is the name the application is know by.
The `filetype` is the use as the suffix for a config file.
Typical filetypes are .json, .ini, .xml, etc.

For example the widget application from example.com that uses a JSON
configuration file:

~~~~
from config_path import ConfigPath
conf_path = ConfigPath( 'example.com', 'widget', '.json' )
~~~~

## single configuration file

~~~~
path = conf_path.saveFilePath( mkdir=False )
~~~~

`saveFilePath` returns the path where the configuation file should be written to.

When `mkdir` is True the parent directory of the path will be created if it does not exist.

Note: the path returned from `saveFilePath()` can be different from the
path returned by `readFilePath()`.

~~~~
path = conf_path.readFilePath()
if path is not None:
    # path exists and config can be read
~~~~

`readFilePath` returns the path to an existing configuration file, otherwise None
is returned. Typcially an application will use its default configuration if there
is no existing configuration file.

Note: the path returned from `readFilePath()` can be different from the
path returned by `saveFilePath()`.

For example readFilePath may return a system wide default config until the appliaction
saves a users specific configuration file.

## multiple configuration files

~~~~
path = conf_path.saveFolderPath( mkdir=False )
~~~~

`saveFolderPath` returns the path to the folder that the application should
save its configuration files into. The naming of the file is left to the application logic.

The path is a `pathlib.Path()` object for python 3 and a string for python 2

When `mkdir` is True the parent directory of the path will be created
if it does not exist.

Note: the path returned from `saveFolderPath()` can be different from the
path returned by `readFolderPath()`.

~~~~
path = conf_path.readFolderPath( mkdir=False )
~~~~

`readFolderPath` returns the path to the folder that the application should use
to read its configuration files.

The path is a `pathlib.Path()` object for python 3 and a string for python 2

When `mkdir` is True the parent directory of the path will be created
if it does not exist.

Note: the path returned from `readFolderPath()` can be different from the
path returned by `saveFolderPath()`.

## macOS conventions

On macOS configuration files are called preferences. They are expected to be stored in the
~/Library/Preferences folder using a file name that uses a reversed domain name.

For a file that will be `{reversed-vendor}.{appname}{filetype}` using the above example:
`com.example.widget.json`.

When a folder is required the folder will be  `{reversed-vendor}.{appname}`.
For example: `com.example.widget`.

## windows conventions

On Windows configuration files are stored in a folder that is return from a WIN32 API call.
Exactly which folder is used has changed over time between Windows versions and maybe
language dependent.

config_path uses the convention of combining the `appname` and `vendor` to create a
path that is expected to be unique.

For a file that will be `{reversed-vendor}.{appname}{filetype}` using the above example:
`com.example.widget.json`.

When a folder is required the folder will be  `{reversed-vendor}.{appname}`.
For example: `com.example.widget`.

## all others conventions

For all systems that are not macOS or Windows config-path follows
the 'XDG Base Directory Specification' for configuration data.

XDG allows for system configuration and user configuration files.
The default user configuration folder is `~/.config`.
The default system configuration folder is `/etc/xdg`.

For a file that will be `{reversed-vendor}.{appname}{filetype}` using the above example:
`com.example.widget.json`.

When a folder is required the folder will be  `{reversed-vendor}.{appname}`.
For example: `com.example.widget`.
