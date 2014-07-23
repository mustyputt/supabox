# Autoupdate Module By: Blazetamer 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,time,shutil
import downloader
import extract
from addon.common.addon import Addon
addon_id = 'plugin.video.moviedb'
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
from addon.common.net import Net

net = Net()
settings = xbmcaddon.Addon(id='plugin.video.moviedb')
if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg', ''))
else:
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart/fanart.jpg', ''))
#====================Start update procedures=======================

def UPDATEFILES():
        #https://raw.githubusercontent.com/Blazetamer/cliqupdate/master/
        url='https://raw.githubusercontent.com/Blazetamer/cliqupdate/master/plugin.video.moviedb.zip'
        path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
        addonpath=xbmc.translatePath(os.path.join('special://','home/addons'))
        name= 'cliqupdatepackage.zip'
        lib=os.path.join(path,name)
        try: os.remove(lib)
        except: pass
        downloader.download(url, lib, '')
        extract.all(lib,addonpath,'')
        LogNotify('Update Complete', 'Resetting Menus', '5000', artwork+'/icon.png')
        return
        



def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")       
