#
#   test_config_path.py
#
from __future__ import print_function

import config_path

c = config_path.ConfigPath('foo', 'example.com', '.json')
print( repr(c) )
print( '_getFolderName: %r' % (c._getFolderName() ) )
print( '_getFileName: %r' % (c._getFileName() ) )

print( 'readFolderPath: %r' % (c.readFolderPath() ) )
print( 'saveFolderPath: %r' % (c.saveFolderPath() ) )
print( 'readFilePath: %r' % (c.readFilePath() ) )
print( 'saveFilePath: %r' % (c.saveFilePath() ) )
