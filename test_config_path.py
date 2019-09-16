import config_path

c = config_path.ConfigPath('foo', 'example.com', '.json')
print( '_getFolderName', c._getFolderName() )
print( '_getFileName', c._getFileName() )

print( 'readFolderPath', c.readFolderPath() )
print( 'saveFolderPath', c.saveFolderPath() )
print( 'readFilePath', c.readFilePath() )
print( 'saveFilePath', c.saveFilePath() )
