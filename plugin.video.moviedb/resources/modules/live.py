
#  Live Streams Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main,math

from metahandler import metahandlers
from resources.utils import buggalo
import urlresolver
import ninestreams

from addon.common.addon import Addon
addon_id = 'plugin.video.moviedb'

from addon.common.net import Net
net = Net()
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer




#addon = Addon(addon_id, sys.argv)
addon = main.addon
# Cache  
streamcache = StorageServer.StorageServer("MovieDBfavs", 0)
standardstreamcache = StorageServer.StorageServer("MovieDBSTfavs", 0)

mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
desc = addon.queries.get('desc', '')
gomode = addon.queries.get('gomode', '')


# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg', ''))
else:
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart/fanart.jpg', ''))
grab=metahandlers.MetaData()
net = Net()
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link




def LIVECATS(url):
   try:        
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                addDir(name,url,mode,thumb,desc,thumb)
        #addDir('User Submitted Playlists' ,'http://goo.gl/JQzOhw','database',artwork +'submitted.jpg','User Submitted Playlists ',fanart)        
        main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()        
        
def COMMONSTREAMS(url):
   try:        
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
        for name,url,thumb in match:
                addDir(name,url,'livecatslist',thumb,'',thumb)                        
        main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()

def USERSTREAMS(url):
   try:
             link=OPEN_URL(url).replace('\n','').replace('\r','')
             match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
             for name,url,thumb in match:
                     addDir(name,url,'ninelists',thumb,'',thumb)
             match=re.compile('<name>(.+?)</name><thumbnail>(.+?)</thumbnail><link>(.+?)</link>').findall(link)
             for name,thumb,url in match:
                     addDir(name,url,'ninelists',thumb,'',thumb)
             match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
             for name,url,thumb in match:
                     addDir(name,url,'ninelists',thumb,'',thumb)         
             main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()

        
        
def USERSUB(url):
   try:        
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><submitted>(.+?)</submitted>').findall(link)
        for name,url,thumb,date in match:
                 addDir(name,url,'livecatslist',thumb,'',thumb)                        
        main.AUTO_VIEW('movies')        
   except Exception:
        buggalo.onExceptionRaised()


        
def LIVECATSLIST(url):
   try:        
        mainurl=url
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                #addDir(name,url,mode,thumb,desc,thumb)                        
                addSTFavDir(name,url,mode,thumb,'','',isFolder=False, isPlayable=True)
        link=OPEN_URL(mainurl).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
        for name,url,thumb in match:
                #addDir(name,url,'liveresolve',thumb,'',thumb)       
                addSTFavDir(name,url,'liveresolve',thumb,'','',isFolder=False, isPlayable=True)

        main.AUTO_VIEW('movies')   
   except Exception:
        buggalo.onExceptionRaised()


def ILIVERESOLVE(name,url,iconimage):
         liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
 
         liz.setInfo( type="Video", infoLabels={ "Title": name} )
         liz.setPath(url)

         xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
         


def LIVERESOLVE(name,url,thumb):
         params = {'url':url, 'name':name, 'thumb':thumb}
         addon.add_video_item(params, {'title':name}, img=thumb)
         liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
         #xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)
         

  

def addDir(name,url,mode,thumb,desc,favtype):
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg'
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addListDir(name,url,mode,cat,thumb,lang):
        
        params = {'url':url,'mode':mode, 'cat':cat, 'name':name, 'thumb':thumb, 'lang':lang}        
        desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg'
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
#==============================Attempt to scrape Ilive.to==============================================================

def ILIVEMAIN():
     try:

               #addDir('Language','LANG','ilivelistslang',artwork+'/ilive.png','','')
               addDir('All','all','ilivelists',artwork+'/ilive.png','','')
               link=OPEN_URL('http://www.mobileonline.tv/index.php')
               match=re.compile('class="contentLink">(.+?)</a>').findall(link)
               for cats in match:
                    if 'Home' not in cats and 'Account' not in cats and 'Premium' not in cats :
                         addDir(cats,cats,'ilivelists',artwork+'/ilive.png','','')
               
               '''addDir('All','all','ilivelists',artwork+'/ilive.png','All English Streams available from iLive','')
               addDir('Animation','Animation','ilivelists',artwork+'/ilive.png','Animation Stream Listings','')
               addDir('Entertainment','Entertainment','ilivelists',artwork+'/ilive.png','All Entertainment Streams from iLive','')
               addDir('Family','Family','ilivelists',artwork+'/ilive.png','All Family Streams from iLive','')
               addDir('Gaming','Gaming','ilivelists',artwork+'/ilive.png','All Gaming Streams from iLive','')
               addDir('General','general','ilivelists',artwork+'/ilive.png','General Streams','')
               addDir('Life Casting','Life Casting','ilivelists',artwork+'/ilive.png','All Entertainment Streams from iLive','')
               addDir('Live Sports','Live Sport','ilivelists',artwork+'/ilive.png','Live Sports Streams from iLive','')
               addDir('Mobile','Mobile','ilivelists',artwork+'/ilive.png','Live Mobile Streams from iLive','')
               addDir('Movies','Movies','ilivelists',artwork+'/ilive.png','Movie Streams from iLive','')
               addDir('Music','Music','ilivelists',artwork+'/ilive.png','Current Listed Music Streams','')
               addDir('News','News','ilivelists',artwork+'/ilive.png','Current News Streams','')
               addDir('Radio','Radio','ilivelists',artwork+'/ilive.png','Live Radio Streams from iLive','')
               addDir('Religion','Religion','ilivelists',artwork+'/ilive.png','Live Sports Streams from iLive','')'''
               link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/streams/ilivemenu.xml').replace('\n','').replace('\r','')
               match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
               for name,url,thumb,mode,desc in match:
                     print 'Description is  ' + desc
                     addDir(name,url,mode,thumb,desc,thumb)               
               main.AUTO_VIEW('movies')
     except Exception:
        buggalo.onExceptionRaised()

    
        

def ILIVELISTS(menuurl):
     print 'NEW URLIS ' + menuurl
     link=OPEN_URL('http://www.ilive.to/api/live.xml')
     match=re.compile('<channel><name>(.+?)</name><url>(.+?)</url><image>(.+?)</image><category>(.+?)</category><language>(.+?)</language><views>(.+?)</views></channel>').findall(link)
     match.sort()
     for name,url,thumb,cat,lang,views in match:
          if menuurl == cat:
               
               if settings.getSetting('adult') == 'true':
                      addSTFavDir(name +' '+'[COLOR lime]('+ lang +')[/COLOR] '+' Views '+views,url,'iliveplaylink',thumb,'','',isFolder=False, isPlayable=True)
                 
               else:        
                      if 'venus' not in name.lower() and '+16' not in name.lower() and '+18' not in name.lower() and 'hongkong' not in name.lower() and   'playboy' not in name.lower() and   'sex' not in name.lower() and   'girls' not in name.lower() and   'fuck' not in name.lower() and   'hardcore' not in name.lower() and   'softcore' not in name.lower() and   'pussy' not in name.lower() and   'dick' not in name.lower() and   'anal' not in name.lower() and   'cum' not in name.lower() and   'blowjob' not in name.lower() and   'adult' not in name.lower() and   '18+' not in name.lower() and  '16+' not in name.lower():
                              addSTFavDir(name +' '+'[COLOR lime]('+ lang +')[/COLOR]'+' Views '+views,url,'iliveplaylink',thumb,'','',isFolder=False, isPlayable=True)
                         
          

          if menuurl == 'all':
               
               if settings.getSetting('adult') == 'true':
                      addSTFavDir(name +' '+'[COLOR lime]('+ lang +')[/COLOR] '+' Views '+views,url,'iliveplaylink',thumb,'','',isFolder=False, isPlayable=True)
                 
               else:        
                      if 'venus' not in name.lower() and '+16' not in name.lower() and '+18' not in name.lower() and 'hongkong' not in name.lower() and   'playboy' not in name.lower() and   'sex' not in name.lower() and   'girls' not in name.lower() and   'fuck' not in name.lower() and   'hardcore' not in name.lower() and   'softcore' not in name.lower() and   'pussy' not in name.lower() and   'dick' not in name.lower() and   'anal' not in name.lower() and   'cum' not in name.lower() and   'blowjob' not in name.lower() and   'adult' not in name.lower() and   '18+' not in name.lower() and  '16+' not in name.lower():
                              addSTFavDir(name +' '+'[COLOR lime]('+ lang +')[/COLOR] '+' Views '+views,url,'iliveplaylink',thumb,'','',isFolder=False, isPlayable=True)
                              
               
         
         
def doCtoD(c):
    if len(c) > 0:
        d=""; ic=len(c); i=0; 
        while (i<ic):
            try:
                if i%3==0: d+="%";
                else: d+=c[i]
            except: pass; #debob({'d[error]':d})
            i=i+1
        #debob({'d':d})
        d=urllib.unquote_plus(d)
        #debob({'du':d})
        return d
    else: return ''
    
def doXTtoXZ(x,tS,b=1024,p=0,s=0,w=0,r2=''):
        l=len(x); t=tS.split(','); r=[]
        
        for j in range(int(math.ceil(l/b)),0, -1):
            for i in range(min(l,b),0, -1):
                w |= int(t[ord(x[p])-48]) << s
                p += 1
                if (s):
                    r.append(chr(165 ^ w & 255))
                    w >>= 8
                    s -= 2
                else:
                    s = 6
            l -=1
        r = ''.join(r)
        return r
        
    

def ILIVEPLAYLINKOLD(name,menuurl,thumb):
   try:        
                       
                link=OPEN_URL(menuurl)
                print 'MAIN LINK IS ' + menuurl 
                ok=True
                if link:
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.clear()
                                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace("\/",'/')
                                matchserv=re.compile('''.*getJSON\("([^'"]+)".*''').findall(link)
                                for server in matchserv:
                                        print 'Server IS ' +server
                                        headers = {'Referer': 'http://www.ilive.to/'}
                                        url = server
                                        html = net.http_GET(url, headers=headers).content
                                        match=re.compile('{"token":"(.+?)"}').findall(html)
                                        for token in match:
                                                print 'SERVERTOKEN IS  '+ token
                                                token = token

                                match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
                                for vid in match:
                                        pageUrl='http://www.ilive.to/m/channel.php?n='+vid
                                        playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
                                        playpath = playpath[0]
                                        newplaypath =str(playpath)        
                                        rtmp=re.compile('''streamer: "([^"]+?)"''').findall(link)
                                        app=rtmp[0].split('?xs=')
                                        #newrtmp = str(rtmp)
                                        #newrtmp = newrtmp.replace('\/','/').replace('\\','')        
                                        #newapp = str(app)
                                        link=OPEN_URL(pageUrl)
                                        swff=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)
                                        for swf in swff:
                                                swf= swf
                                                #swf= swf[0]
                                                #Manual SWF Added
                                                #swf = 'http://www.ilive.to/player/player.swf'
                                                print 'SWF IS ' + swf
                                        playable =rtmp[0]+' app=edge/?xs='+app[1]+' playpath=' + newplaypath + ' swfUrl=' + swf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
                                        
                                        print 'RTMP IS ' +  playable
                                        ILIVERESOLVE(name,playable,thumb)
                                        
   except Exception:
        buggalo.onExceptionRaised()                                

def ILIVEPLAYLINKMOBILE(name,menuurl,thumb):
   try:        
                mobileurl=menuurl.replace('http://www.ilive.to/view/','http://www.mobileonline.tv/channel.php?n=')        
                link=OPEN_URL(mobileurl)
                ok=True
                if link:
                     
                     match=re.compile('<a href=(.+?) target=".+?">Link 3').findall(link)
                     for playable in match:

     
                          ILIVERESOLVE(name,playable,thumb)
                                        
   except Exception:
        buggalo.onExceptionRaised()


                             
        
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
        """ shows a keyboard and returns a value """
        keyboard = xbmc.Keyboard( default, heading, hidden )
        keyboard.doModal()
        if ( keyboard.isConfirmed() ):
                return unicode( keyboard.getText(), "utf-8" )
        return default


#Start Search Function
def SEARCHILIVE(url):
        searchUrl = url 
        vq = _get_keyboard( heading="Searching for Streams" )
        if ( not vq ): return False, 0
        title = urllib.quote_plus(vq)
        searchUrl += title  
        print "Searching Streams: " + searchUrl 
        SEARCHLINKS(searchUrl)
             
               
def SEARCHLINKS(urllist):                 
   try:        
                link=OPEN_URL(urllist)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?" /></noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>').findall(link)
                if len(match) > 0:
                        for thumb,url,name in match:
                                addSTFavDir(name,url,'iliveplaylink',thumb,'','', isFolder=False, isPlayable=True)
                                  
                else:
                        addDir('[COLOR red]None Found Try again[/COLOR]','http://www.ilive.to/channels/?q=','searchilive','','','')
   except Exception:
        buggalo.onExceptionRaised()        


def PLAYFAVS(name,url,thumb):        
        queue = streamcache.get('queue')
        if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               name = item[0]
               url = item[1]
               thumb = item[2]
               print 'PLAY URL IS ' + url
               main.RESOLVE(name,url,thumb)
               
  



#====================Standard Favorites===================================
def addSTFavDir(name,url,mode,thumb,desc,favtype, isFolder=True, isPlayable=False):
        gomode=mode
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlspecial', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(thumb)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        #addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems,context_replace=False, img= thumb)
        if isPlayable:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok

def addSTRemoveDir(name,url,mode,thumb,gomode):
        gomode=mode
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,'gomode': gomode}
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems,context_replace=False, img= thumb)            
     
def ADDSTTOFAVS(name,url,thumb,gomode):
   try:        
     queue = standardstreamcache.get('queue')
     queue_items = []
     if queue:
          queue_items = eval(queue)
          if queue_items:
               if (name,url,thumb,gomode) in queue_items:
                    addon.show_small_popup(title='[COLOR red]Item Already In Your Favorites[/COLOR]', msg=name + ' Is Already In Your Favorite List', delay=int(5000), image=thumb)
                    return
     queue_items.append((name,url,thumb,gomode))         
     standardstreamcache.set('queue', str(queue_items))
     addon.show_small_popup(title='[COLOR gold]Item Added To Your Favorites [/COLOR]', msg=name + ' Was Added To Your Favorite List', delay=int(5000), image=thumb)
   except Exception:
        buggalo.onExceptionRaised()
        
def VIEWSTFAVS():
   try:        
     addDir('[COLOR blue]Favorites[/COLOR]','none','viewstfavs',artwork +'playfavs.jpg','','')
     queue = standardstreamcache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
               addSTRemoveDir(item[0],item[1],item[3],item[2],'')
   except Exception:
        buggalo.onExceptionRaised()

def REMOVESTFROMFAVS(name,url,thumb,gomode):
     queue = standardstreamcache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          queue_items.remove((name,url,thumb,gomode))
          standardstreamcache.set('queue', str(queue_items))
          xbmc.executebuiltin("XBMC.Container.Refresh")
          
#====================END Standard Favorites===============================          


def RESOLVER(url,name):
   try:        
        dlfoldername = name                            
        urls = url
        hmf = urlresolver.HostedMediaFile(urls)
        if hmf:
                host = hmf.get_host()
                dlurl = urlresolver.resolve(urls)
                ILIVERESOLVE(name,dlurl,'')
                                  
   except Exception:
        buggalo.onExceptionRaised()

#=============Below to be used for future updates==============================================================================================================        
               
'''
def addFavDir(name,url,mode,thumb,desc,favtype):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}
        contextMenuItems.append(('[COLOR red]Add to Live Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addtofavs', 'name': name,'url': url,'thumb': thumb})))
        contextMenuItems.append(('[COLOR red]Remove From Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removefromfavs', 'name': name,'url': url,'thumb': thumb})))
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)

def addRemoveDir(name,url,mode,thumb,desc,favtype):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}

        contextMenuItems.append(('[COLOR red]Remove From Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removefromfavs', 'name': name,'url': url,'thumb': thumb})))
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)            
     
def ADDTOFAVS(name,url,thumb):
   try:        
     queue = streamcache.get('queue')
     queue_items = []
     if queue:
          queue_items = eval(queue)
          if queue_items:
               if (name,url,thumb,ext,console) in queue_items:
                    addon.show_small_popup(title='[COLOR red]Item Already In Your Favorites[/COLOR]', msg=name + ' Is Already In Your Favorite List', delay=int(5000), image=thumb)
                    return
     queue_items.append((name,url,thumb))         
     streamcache.set('queue', str(queue_items))
     addon.show_small_popup(title='[COLOR gold]Item Added To Your Favorites [/COLOR]', msg=name + ' Was Added To Your Favorite List', delay=int(5000), image=thumb)
   except Exception:
        buggalo.onExceptionRaised()
        
def VIEWFAVS():
   try:        
     addDir('[COLOR blue]iLive Favorites[/COLOR]','none','viewfavs',artwork +'playfavs.jpg','','')
     queue = streamcache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
               addRemoveDir(item[0],item[1],'iliveplaylink',item[2],'','')
   except Exception:
        buggalo.onExceptionRaised()

def REMOVEFROMFAVS(name,url,thumb):
     queue = streamcache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          queue_items.remove((name,url,thumb,))
          streamcache.set('queue', str(queue_items))
          xbmc.executebuiltin("XBMC.Container.Refresh")
'''
def ILIVEPLAYLINK(mname='',murl='',thumb='',LinkNo=''):
    menuurl=""+murl; name=mname; 
    
    #deb('menuurl',menuurl); 
    link=OPEN_URL(menuurl) #OPEN_URL(menuurl)
    ## ### ## 
    vID=re.compile('view/(\d+)').findall(menuurl)[0]
    menuurl2='http://www.mobileonline.tv/channel.php?n=%s'%vID
    #TimeOut=str(addst('DefaultTimeOut','15'))
    #SleeperTime=str(addst('DefaultSleepBeforePlay','4000'))
    
    #LinkNo='99'
    '''if not LinkNo=='99':
        link2=OPEN_URL(menuurl2)
        ## ### ## 
        if LinkNo=='': LinkNo=addst('DefaultVideoLink','2')
        if LinkNo=='': LinkNo=2
        if LinkNo=='0HLS':  LinkNo=0
        if LinkNo=='1RTMP': LinkNo=1
        if LinkNo=='2RTSP': LinkNo=2
        else: LinkNo=int(LinkNo)
        ## ### ## 
        #debob({'LinkNo':LinkNo})
        #playable=re.compile('<p style="font-size:30px;"><a href=(\D+://.+?) target="_blank">Link').findall(link2)[int(LinkNo)] #0-2, 0:http, 1:rtmp, 2:rtsp
        playables=re.compile('<p style="font-size:30px;"><a href=(\D+://.+?) target="_blank">Link').findall(link2)
        #debob({'playables':playables}); 
        playable=playables[int(LinkNo)] #0-2, 0:http, 1:rtmp, 2:rtsp
        ## ### ## 
        if not TimeOut=='0': playable+=' app=%s live=1 timeout=%s'%('',TimeOut)
        try: xbmc.sleep(int(SleeperTime))
        except: pass
        PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)
        return'''
         
    if '<script language=javascript>c="' in link:
        
        c=re.compile('<script language=javascript>c="(.+?)"').findall(link)[0]; #debob({'c':c}); 
        cu=urllib.unquote_plus(c); #debob({'cu':cu}); 
        d=doCtoD(c);    
        t=re.compile('t=Array\(([0-9,]+)\)').findall(d)[0]; #debob({'t':t}); 
        x=re.compile('"\)\);\s*x\("(.+?)"').findall(link)[0]; #debob({'x':x}); 
        z=doXTtoXZ(x,t); #debob({'z':z}); 
        
        
        #html=''+z; 
        link=''+z; 
         
    ok=True
    grabNo=0 #-1
    if link:
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace("\/",'/')
            
            server=re.compile('''.*getJSON\("([^'"]+)".*''').findall(link)[0]
            print 'Server IS '+server; headers={'Referer':'http://www.ilive.to/'}; url=server; 
             
            #html=OPEN_URL(url,headers=headers)
            '''html=OPEN_URL(url)
            token=re.compile('{"token":"(.+?)"}').findall(html)[0]'''
            html = net.http_GET(url, headers=headers).content
            match=re.compile('{"token":"(.+?)"}').findall(html)
            for token in match:
                            print 'SERVERTOKEN IS  '+ token
                            token = token
            #debob({'token':token,'lengthofhtml':len(html),'server':server}); 
            
            
            vid=re.compile('http://www.ilive.to/embed/(\d+)&width=\d*&height=\d*&autoplay=true').findall(link)[0]
            
            pageUrl='http://www.ilive.to'
            
            playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
            #debob(playpath)
            
            playpath=playpath[grabNo]
            newplaypath=str(playpath)        
            rtmp=re.compile('streamer: "(.+?)"').findall(link)
            #debob(rtmp)
            
            rtmp=rtmp[grabNo]
            newrtmp=str(rtmp)
            newrtmp=newrtmp.replace('\/','/').replace('\\','')
            app=''+newrtmp
            app=app.split('?xs=')[1]
            app2=re.compile('rtmp://[\.\w:]*/([^\s]+)').findall(newrtmp)[0]
            
            try:        ReplacementA=re.compile('(rtmp://[0-9A-Za-z]+\.ilive\.to:\d+/)').findall(app)[0]
            except: ReplacementA=''
            if len(ReplacementA) > 0: app=app.replace(ReplacementA,''); #deb('removing',ReplacementA); 
            newapp=str(app)
            #link=nURL(pageUrl)
            try: swf=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)[0]
            except: swf=''
            if len(swf)==0: swf='http://www.ilive.to/player/player_ilive_2.swf'
            TimeOut= '15'
            #playable='%s app=edge/?xs=%s playpath=%s swfUrl=%s pageUrl=%s live=%s timeout=%s token=%s app=%s'%(newrtmp,newapp,newplaypath,swf,pageUrl,'true','15',token,app2)
            playable='%s app=edge/?xs=%s playpath=%s swfUrl=%s pageUrl=%s live=%s timeout=%s token=%s'%(newrtmp,newapp,newplaypath,swf,pageUrl,'true',TimeOut,token)
            
            #
            print 'RTMP IS '+playable
            
            
            try: xbmc.sleep(int(SleeperTime))
            except: pass
            
            #PlayItCustom(url=murl,stream_url=playable,img=thumb,title=name)
            ILIVERESOLVE(name,playable,thumb)
            
