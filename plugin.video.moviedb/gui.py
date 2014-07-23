
#Default moviedb - Blazetamer


'''import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
from resources.modules import status
import downloader
import extract
import time,re
import datetime
import shutil
from resources.modules import tvshow
from metahandler import metahandlers
from resources.modules import main,flix
from resources.modules import moviedc
from resources.modules import sgate,streamlic
from resources.modules import chia, supertoons, phub
from resources.modules import chanufc, epornik, live
from resources.utils import autoupdate
from resources.utils import buggalo
from resources.modules import oneeighty,iwo
from resources.sports import espn

from addon.common.addon import Addon
from addon.common.net import Net
net = Net(http_debug=True)
        
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')'''

#==================Start GUI Setup============================================
import xbmc,xbmcgui,urllib,urllib2,os,sys,logging,array,re,time,datetime,random,string,StringIO,xbmcplugin,xbmcaddon
artp = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg', ''))

ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9
#class MyWindow(xbmcgui.Window):
class MyWindow( xbmcgui.WindowXMLDialog ): 
    #def __init__( self, *args, **kwargs ):
    def __init__( self, *args ):
        #self.shut = kwargs['close_time']   
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
        
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()
