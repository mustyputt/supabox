#Eporn module by Blazetamer

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
import downloader
from resources.modules import tvshow
from metahandler import metahandlers
from resources.modules import main
from resources.modules import moviedc
from resources.modules import sgate
from resources.modules import chia
from resources.modules import chanufc
from resources.utils import buggalo
try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon

try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net        
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
net = Net(http_debug=True)
base_url = 'http://www.epornik.com'

artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

#========================DLStuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
repourl = addon.queries.get('repourl', '')





def CATEGORIES():
        addDir('Videos',base_url + '/search.php','epornikIndex',artwork + 'eporn.jpg')
        addDir('Search','none','epornikSearch',artwork + '/main/search.png')

def INDEX(url):
   try:        
        np_url = ''
        link = net.http_GET(url).content
        match=re.compile('<a href=".+?">.+?</a>\n                        </div>\n                        <div class="img_preview_item"> <a href="(.+?)"><img src="(.+?)" width=".+?" height=".+?" alt="(.+?)" /></a>').findall(link)
        urln = url        

        for url,thumbnail,name in match:
                
                if name == 'evil 4 2010':
                        continue
                if name == 'evil 3 2007':
                        continue
                if name == 'evil 2 2004':
                        continue
                if name == 'evil 1':
                        continue
                if name == 'lkesi 4':
                        continue
                else:
                        url = base_url + url
                        thumbnail = base_url + thumbnail
                        
                        link = net.http_GET(url).content
                        match=re.compile('"file","(.+?)"').findall(link)
                        addDir(name,match[0],'pornresolve',thumbnail)
                        
        link = net.http_GET(urln).content                
        np=re.compile("<a href='(.+?)' id='next'>Next</a>").findall(link)
        for nurl in np:
                if len(np) > 0:
                        np_url = base_url + '/' + np[0]
                        addDir('[COLOR blue]Next Page>>[/COLOR]',np_url,'epornikIndex', artwork + '/main/next.png')
        main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()        

                                   
def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '/search.php?q=' + search + '&x=-1085&y=-177'
                
                INDEX(url)


#=================================Local Functions=================
def addDir(name,url,mode,thumb):
     #name = main.nameCleaner(name)
     if thumb == '':
          thumb = artwork + '/main/noepisode.png'
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,  'types':'movie'}
     addon.add_directory(params, {'title':name}, img= thumb, fanart= thumb)                


def PORNRESOLVE(name,url,thumb):
   try:        
     meta = 0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
     
             
     params = {'url':url, 'name':name, 'thumb':thumb}
     if meta == 0:
          addon.add_video_item(params, {'title':name}, img=thumb)
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)

     else:
          addon.add_video_item(params, {'title':name}, img=meta['cover_url'])
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=meta['cover_url'])
          liz.setInfo('video',infoLabels=meta)

     xbmc.sleep(1000)
        
     xbmc.Player ().play(url, liz, False)
   except Exception:
        buggalo.onExceptionRaised()     

