from entertainment.filestore import FileStore
fs = FileStore()
if not fs.check_file_store('http://xty.me/xunitytalk'):
    fs.add_file_store('[B][COLOR steelblue]X[/COLOR][COLOR white]UNITYTALK[/COLOR][/B] [COLOR gray]PLAYLIST DIRECTORY[/COLOR]', '', 'https://raw.githubusercontent.com/Coolwavexunitytalk/images/2f125e294033cc32ccdc867a60ca249d4e30f76c/xunitytalk%20playlist.png', 'playlist', 'xbmcplx', 'XBMC PLX', 'http://xty.me/xunitytalk' )
