import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import socket
import xbmcaddon
import cookielib
import urllib2

settings = xbmcaddon.Addon(id='script.module.watchhistory')
language = settings.getLocalizedString
version = "0.1.0"
plugin = "WatchHistory-" + version
core = ""
common = ""
downloader = ""
dbg = False
dbglevel = 3

#print 'in wh service'
import watchhistory

print 'Watch History Module and Service: Auto Cleanup - Start'
wh = watchhistory.WatchHistory('script.module.watchhistory')
wh.cleanup_history()
print 'Watch History Module and Service: Auto Cleanup - End'