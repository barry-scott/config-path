#
#   config_path
#
VERSION = '1.0.0'

import sys
import os

#
#   Factory to return the OS specific config path class
#
def ConfigPath( name, vender, appname ):
    if sys.platform == 'win32':
        # windows
        return WindowsConfigPath( name, appname )

    if sys.platform == 'darwin':
        # assume darwin mean macOS
        return MacOsConfigPath( name, vender )

    else:
        # assume all else are XDG compatable
        return XdgConfigPath( name, appname )

class ConfigPathBase(object):
    def __init__( self ):
        pass

    #
    #   to use a single config files use
    #   saveFilePath and readFilePath
    #
    def saveFilePath( self, mkdir=False ):
        raise NotImplementedError('saveFilePath')

    def readFilePath( self ):
        raise NotImplementedError('readFilePath')

    #
    #   to use a folder of config files use
    #   saveFolderPath and readFolderPath
    #
    def saveFolderPath( self, mkdir=False ):
        raise NotImplementedError('saveFolderPath')

    def readFolderPath( self ):
        raise NotImplementedError('readFolderPath')

class MacOsConfigPath(ConfigPathBase):
    # vender is a FQDN for the website of the vender for this app
    # example: sfind.barrys-emacs.org
    # name is the apps config filename
    # example: sfind.json
    def __init__( self, name, vender ):
        super(MacOsConfigPath, self).__init__()
        self.name = name
        self.vender = vender

    def saveFolderPath( self, mkdir=False ):
        return self.configFolderPath( mkdir )

    def readFolderPath( self ):
        return self.configFolderPath()

    def saveFilePath( self, mkdir=False ):
        return self.configFilePath( mkdir )

    def readFilePath( self ):
        config_path = self.configFilePath( False )
        if os.path.exists( config_path ):
            return config_path

        return None

    def configFolderPath( self, mkdir ):
        # any folder that do not exist will be created

        # change foo.org into org.foo
        reversed_vender = '.'.join( reversed( self.vender.split('.') ) )

        config_folder = os.path.join( self.getConfigFolder(), reversed_vender )

        if mkdir and not os.path.exists( config_folder ):
                os.makedirs( config_folder )

        return config_folder

    def configFilePath( self, mkdir ):
        # return the path to save the config data into
        config_path = os.path.join( self.getConfigFolder(), self.name )
        return config_path

    def getConfigFolder( self ):
        return os.path.join( os.environ['HOME'], 'Library/Preferences' )


class XdgConfigPath(ConfigPathBase):
    # if appname is given put the config in a folder of that name
    # name is the name of the config file
    def __init__( self, name, appname ):
        super(XdgConfigPath, self).__init__()
        self.name = name
        self.appname = appname

    def saveFolderPath( self, mkdir=False ):
        config_home = self.getConfigHome()
        config_folder = os.path.join( config_home, self.appname )

        if mkdir and not os.path.exists( config_folder ):
            os.makedirs( config_folder )

        return config_folder

    def readFolderPath( self, mkdir ):
        # return the path to read the folder that store config files.
        # any folder that do not exist will be created
        config_home = self.getConfigHome()
        config_folder = os.path.join( config_home, self.appname )

        if mkdir and not os.path.exists( config_folder ):
            os.makedirs( config_folder )

        return config_folder

    def saveFilePath( self, mkdir=False ):
        # return the path to save the config data into
        # any folder that do not exist will be created
        config_home = self.getConfigHome()
        config_path = os.path.join( config_home, self.name )
        if mkdir and not os.path.exists( config_home ):
            os.makedirs( config_home )

        return config_path

    def readFilePath( self ):
        # look for the config file in the config home then the config dirs
        # return the None is not found otherwise the config path.
        for config_dir in [self.getConfigHome()] + self.getConfigDirs():
            config_path = os.path.join( config_dir, self.name )
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
    def __init__( self, name, appname ):
        super(WindowsConfigPath, self).__init__()
        self.name = name
        self.appname = appname

        import ctypes
        import ctypes.wintypes

        CSIDL_APPDATA = 0x1a        # Application Data
        SHGFP_TYPE_CURRENT = 0      # Want current, not default value

        buf = ctypes.create_unicode_buffer( ctypes.wintypes.MAX_PATH )
        ctypes.windll.shell32.SHGetFolderPathW( 0, CSIDL_APPDATA, 0, SHGFP_TYPE_CURRENT, buf )

        self.config_folder = buf.value

    def getConfigFolder( self ):
        return self.config_folder

    def saveFolderPath( self, mkdir=False ):
        return self.configFolderPath( mkdir )

    def readFolderPath( self ):
        return self.configFolderPath()

    def saveFilePath( self, mkdir=False ):
        return self.configFilePath( mkdir )

    def readFilePath( self ):
        config_path = self.configFilePath( False )
        if os.path.exists( config_path ):
            return config_path

        return None

    def configFolderPath( self, mkdir ):
        # any folder that do not exist will be created
        config_folder = os.path.join( self.getConfigFolder(), self.name )

        if mkdir and not os.path.exists( config_folder ):
                os.makedirs( config_folder )

        return config_folder

    def configFilePath( self, mkdir ):
        # return the path to save the config data into
        config_path = os.path.join( self.getConfigFolder(), self.name )
        return config_path
