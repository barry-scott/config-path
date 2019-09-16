#
#   config_path
#
VERSION = '1.0.0'

import sys
import os

#
#   Factory to return the OS specific config path class
#
def ConfigPath( appname, vendor, filetype ):
    if sys.platform == 'win32':
        # windows
        return WindowsConfigPath( appname, vendor, filetype )

    if sys.platform == 'darwin':
        # assume darwin mean macOS
        return MacOsConfigPath( appname, vendor, filetype )

    else:
        # assume all else are XDG compatable
        return XdgConfigPath( appname, vendor, filetype )

class ConfigPathBase(object):
    def __init__( self, appname, vendor, filetype, config_file_fmt, config_folder_fmt ):
        self._config_naming_variables = {
            'appname': appname,
            'vendor': vendor,
            'filetype': filetype,
            }
        self._config_file_fmt = config_file_fmt
        self._config_folder_fmt = config_folder_fmt

    def _getFolderName( self ):
        return self._config_folder_fmt % self._config_naming_variables

    def _getFileName( self ):
        return self._config_file_fmt % self._config_naming_variables

    def _getRootConfigFolder( self ):
        raise NotImplementedError('_getRootConfigFolder')

    #
    #   to use a folder of config files use
    #   saveFolderPath and readFolderPath
    #
    def saveFolderPath( self, mkdir=False ):
        return self.configFolderPath( mkdir )

    def readFolderPath( self, mkdir=False ):
        return self.configFolderPath( mkdir )

    #
    #   to use a single config files use
    #   saveFilePath and readFilePath
    #
    def saveFilePath( self, mkdir=False ):
        return self.configFilePath( mkdir )

    def readFilePath( self ):
        config_path = self.configFilePath( False )
        if os.path.exists( config_path ):
            return config_path

        return None

    def configFolderPath( self, mkdir ):
        # any folder that do not exist will be created
        config_folder = os.path.join( self._getRootConfigFolder(), self._getFolderName() )

        if mkdir and not os.path.exists( config_folder ):
            os.makedirs( config_folder )

        return config_folder

    def configFilePath( self, mkdir ):
        # return the path to save the config data into
        config_path = os.path.join( self._getRootConfigFolder(), self._getFileName() )
        return config_path

class MacOsConfigPath(ConfigPathBase):
    # vendor is a FQDN for the website of the vendor for this app
    # example: sfind.barrys-emacs.org
    # name is the apps config filename
    # example: sfind.json
    def __init__( self, appname, vendor, filetype ):
        super(MacOsConfigPath, self).__init__(
            appname, vendor, filetype,
            '%(rev-vendor)s.%(appname)s%(filetype)s',
            '%(rev-vendor)s.%(appname)s' )

        # change foo.org into org.foo
        reversed_vendor = '.'.join( reversed( self.vendor.split('.') ) )

        self._config_naming_variables[ 'rev-vendor' ] = reversed_vendor

    def _getRootConfigFolder( self ):
        return os.path.join( os.environ['HOME'], 'Library/Preferences' )

class XdgConfigPath(ConfigPathBase):
    # if appname is given put the config in a folder of that name
    # name is the name of the config file
    def __init__( self, appname, vendor, filetype ):
        super(XdgConfigPath, self).__init__(
            appname, vendor, filetype,
            '%(appname)s.%(vendor)s%(filetype)s',
            '%(appname)s.%(vendor)s' )

    def _getRootConfigFolder( self ):
        return self.getConfigHome()

    def readFilePath( self ):
        # look for the config file in the config home then the config dirs
        # return the None is not found otherwise the config path.
        for config_dir in [self.getConfigHome()] + self.getConfigDirs():
            config_path = os.path.join( config_dir, self._getFileName() )
            if os.path.exists( config_path ):
                return config_path

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

class WindowsConfigPath(ConfigPathBase):
    # if appname is given put the config in a folder of that name
    # name is the name of the config file
    def __init__( self, appname, vendor, filetype ):
        super(WindowsConfigPath, self).__init__(
            appname, vendor, filetype,
            '%(appname)s.%(vendor)s%(filetype)s',
            '%(appname)s.%(vendor)s' )

        import ctypes
        import ctypes.wintypes

        CSIDL_APPDATA = 0x1a        # Application Data
        SHGFP_TYPE_CURRENT = 0      # Want current, not default value

        buf = ctypes.create_unicode_buffer( ctypes.wintypes.MAX_PATH )
        ctypes.windll.shell32.SHGetFolderPathW( 0, CSIDL_APPDATA, 0, SHGFP_TYPE_CURRENT, buf )

        self.config_folder = buf.value

    def _getRootConfigFolder( self ):
        return self.config_folder
