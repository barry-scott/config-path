'''
    config_path - work out which path to use for configuration folders
    and files in an operating system independent way.

    Each operating system has particular conventions for where an application
    is expected to stores it configuration. The information provided to
    ConfigPath is used to figure out an appropiate file path or folder
    path for the application's configuration data.

    Supports Windows, macOS and most unix systems using the
    'XDG Base Directory Specification'.
'''

VERSION = '1.0.2'

__all__ = ('VERSION', 'ConfigPath')

import platform
import os

try:
    import pathlib
    Path = pathlib.Path

except ImportError:
    def Path( p ):
        return p


class ConfigPath(object):
    def __new__( cls, appname, vendor, filetype ):
        if platform.win32_ver()[0] != '':
            # windows
            return super( ConfigPath, cls ).__new__( WindowsConfigPath )

        if platform.mac_ver()[0] != '':
            # macOS
            return super( ConfigPath, cls ).__new__( MacOsConfigPath )

        else:
            # assume all else are XDG compatable
            return super( ConfigPath, cls ).__new__( XdgConfigPath )

    def __init__( self, appname, vendor, filetype ):
        '''
        The `vendor` should be the domain name of the application provider.
        The `appname` is the name the application is know by.
        The `filetype` is the use as the suffix for a config file.
        Typical filetypes are .json, .ini, .xml, etc.

            cfg_path = ConfigPath( 'widget-app', 'example.com', '.json' )
        '''
        self._config_naming_variables = {
            'appname': appname,
            'vendor': vendor,
            'filetype': filetype,
            }

        # change foo.org into org.foo
        reversed_vendor = '.'.join( reversed( vendor.split('.') ) )
        self._config_naming_variables[ 'rev-vendor' ] = reversed_vendor

        self._config_file_fmt = '%(rev-vendor)s.%(appname)s%(filetype)s'
        self._config_folder_fmt = '%(rev-vendor)s.%(appname)s'

    def __repr__( self ):
        return '<%s: appname %r vendor %r filetype %r>' % (
                self.__class__.__name__,
                self._config_naming_variables[ 'appname' ],
                self._config_naming_variables[ 'vendor' ],
                self._config_naming_variables[ 'filetype' ])

    def _getFolderName( self ):
        return self._config_folder_fmt % self._config_naming_variables

    def _getFileName( self ):
        return self._config_file_fmt % self._config_naming_variables

    def _getRootConfigFolder( self ):
        raise NotImplementedError('_getRootConfigFolder')

    def saveFolderPath( self, mkdir=False ):
        '''return the path to the folder to use to save config files into.

        The path is a pathlib.Path() object for python 3 and a string for python 2.

        When `mkdir` is True the parent directory of the path will be created
        if it does not exist.

        Note: the path returned from saveFolderPath() can be different from the
        path returned by readFolderPath().
        '''
        return Path( self._configFolderPath( mkdir ) )

    def readFolderPath( self, mkdir=False ):
        '''return the path to the folder to use to read config files from

        The path is a pathlib.Path() object for python 3 and a string for python 2.

        When `mkdir` is True the parent directory of the path will be created
        if it does not exist.

        Note: the path returned from readFolderPath() can be different from the
        path returned by saveFolderPath().
        '''

        return Path( self._configFolderPath( mkdir ) )

    def saveFilePath( self, mkdir=False ):
        '''return the path to the file to use to save config data into

        The path is a pathlib.Path() object for python 3 and a string for python 2.

        When `mkdir` is True the parent directory of the path will be created
        if it does not exist.

        Note: the path returned from saveFilePath() can be different from the
        path returned by readFilePath().
        '''

        return Path( self._configFilePath( mkdir ) )

    def readFilePath( self ):
        '''return the path to the file to use to read config data from if the file exists
        otherwise None is returned.

        The path is a pathlib.Path() object for python 3 and a string for python 2.

        When `mkdir` is True the parent directory of the path will be created
        if it does not exist.

        Note: the path returned from readFilePath() can be different from the
        path returned by saveFilePath().
        '''

        config_path = self._configFilePath( False )
        if os.path.exists( config_path ):
            return Path( config_path )

        return None

    def _configFolderPath( self, mkdir ):
        # any folder that do not exist will be created
        config_folder = os.path.join( self._getRootConfigFolder(), self._getFolderName() )

        if mkdir and not os.path.exists( config_folder ):
            os.makedirs( config_folder )

        return config_folder

    def _configFilePath( self, mkdir ):
        # return the path to save the config data into
        config_path = os.path.join( self._getRootConfigFolder(), self._getFileName() )
        return config_path


class MacOsConfigPath(ConfigPath):
    def __init__( self, appname, vendor, filetype ):
        super(MacOsConfigPath, self).__init__( appname, vendor, filetype )

    def _getRootConfigFolder( self ):
        return os.path.join( os.environ['HOME'], 'Library/Preferences' )


class XdgConfigPath(ConfigPath):
    def __init__( self, appname, vendor, filetype ):
        super(XdgConfigPath, self).__init__( appname, vendor, filetype )

    def _getRootConfigFolder( self ):
        return self.getConfigHome()

    def readFilePath( self ):
        # look for the config file in the config home then the config dirs
        # return the None is not found otherwise the config path.
        for config_dir in [self.getConfigHome()] + self.getConfigDirs():
            config_path = os.path.join( config_dir, self._getFileName() )
            if os.path.exists( config_path ):
                return Path( config_path )

        return None

    def getConfigHome( self ):
        return self.getEnvVar( 'XDG_CONFIG_HOME', os.path.join( os.environ['HOME'], '.config' ) )

    def getConfigDirs( self ):
        return self.getEnvVar( 'XDG_CONFIG_DIRS', '/etc/xdg' ).split(':')

    def getEnvVar( self, name, default ):
        # XDG says if missing or empty use the default
        value = os.environ.get( name, '' )
        if value != '':
            return value
        return default


class WindowsConfigPath(ConfigPath):
    # if appname is given put the config in a folder of that name
    # name is the name of the config file
    def __init__( self, appname, vendor, filetype ):
        super(WindowsConfigPath, self).__init__( appname, vendor, filetype )

        import ctypes
        import ctypes.wintypes

        CSIDL_APPDATA = 0x1a        # Application Data
        SHGFP_TYPE_CURRENT = 0      # Want current, not default value

        buf = ctypes.create_unicode_buffer( ctypes.wintypes.MAX_PATH )
        ctypes.windll.shell32.SHGetFolderPathW( 0, CSIDL_APPDATA, 0, SHGFP_TYPE_CURRENT, buf )

        self.config_folder = buf.value

    def _getRootConfigFolder( self ):
        return self.config_folder
