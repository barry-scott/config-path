# config-path
Python library to work with path to config folders and files in an OS independent way

~~~~
from config_path import ConfigPath

conf_path = ConfigPath( 'widget.json', 'widget.example.com', 'widget' )
~~~~

## filename to save config into

~~~~
path = conf_path.saveFilePath( mkdir=True )
~~~~

## filename to read config from

~~~~
path = conf_path.readFilePath()
if path is not None:
    # read the config
~~~~
