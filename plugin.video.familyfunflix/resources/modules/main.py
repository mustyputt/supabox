# -*- coding: cp1252 -*-
# Main Module by: Blazetamer

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon
from metahandler import metahandlers


from addon.common.addon import Addon

from addon.common.net import Net


net = Net()


import threading

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer
import time

# Cache  
cache = StorageServer.StorageServer("familyfunflix", 0)

settings = xbmcaddon.Addon(id='plugin.video.familyfunflix')     
addon_id = 'plugin.video.familyfunflix'
addon = Addon(addon_id, sys.argv)
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')

print 'Mode is: ' + mode
print 'Url is: ' + url
print 'Name is: ' + name
print 'Thumb is: ' + thumb
print 'Extension is: ' + ext
print 'File Type is: ' + console
print 'DL Folder is: ' + dlfoldername
print 'Favtype is: ' + favtype
print 'Main Image is: ' + mainimg


download_path = settings.getSetting('download_folder')



     



# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
net = Net()


def nameCleaner(name):
          name = name.replace('&#8211;','')
          name = name.replace("&#8217;","")
          name = name.replace("&#039;s","'s")
          return(name)
     


#Metadata    
grab=metahandlers.MetaData()

def GRABMETA(name,year):
        meta = grab.get_meta('movie',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels
        
        







     
#******************For Movie Download*********************************
def addDLDir(name,url,mode,thumb,labels,dlfoldername,favtype,mainimg):
        contextMenuItems = []
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype, 'mainimg':mainimg}
        contextMenuItems.append(('[COLOR gold]Download Stream File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'directresolvedl', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)                             
       




     

        
     
# HELPDIR



def addHELPDir(name,url,mode,iconimage,fanart,description,filetype):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def add2HELPDir(name,url,mode,iconimage,fanart,description,filetype):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok          

     
# Standard addDir
def addDir(name,url,mode,thumb,labels,favtype):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype, 'mainimg':mainimg}
        contextMenuItems = []
        sitethumb = thumb
        sitename = name
        #Added fanart variable to prevent a referenced before assignment error
        #fanart = ''
  
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = str(data['backdrop_url'])
        except:
                name = sitename
                  
        if thumb == '':
                thumb = sitethumb
                  
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&favtype="+urllib.quote_plus(favtype)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movies':
                contextMenuItems.append(('[COLOR gold]Movie Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'tv':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype, 'mainimg':mainimg}
        #addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb, fanart=fanart) 
  
        #Changed return from ok to 0
        return ok







#Resolve Functions
     
def RESOLVE(name,url,thumb):
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=thumb,thumbnailImage=thumb); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         AUTO_VIEW('')

#Resolve 2 

def RESOLVE2(name,url,thumb):
         
     data=0
     try:
          data = GRABMETA(movie_name,year)
     except:
           data=0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host() 
             
     params = {'url':url, 'name':name, 'thumb':thumb}
     if data == 0:
          addon.add_video_item(params, {'title':name}, img=thumb)
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)

     else:
          addon.add_video_item(params, {'title':name}, img=data['cover_url'])
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=data['cover_url'])
          liz.setInfo('video',infoLabels=data)

     xbmc.sleep(1000)
        
     xbmc.Player ().play(url, liz, False)

#AutoView
def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view') )
                       
                        

                              
                                
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )

        


     





                              



