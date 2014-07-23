# -*- coding: cp1252 -*-
import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,xbmcaddon,sys,os,cookielib,htmlentitydefs,urlresolver,requests
import simplejson as json

from BeautifulSoup import BeautifulSoup, SoupStrainer
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from metahandler import metahandlers



##
# Bunkford - 2013.
#
# TODO:
#    multithreaded downloader class running in background.
#    get helpText from file.

helpText = """
Downloading:

     For downloading to work correctly you need to specify download paths in the plugin settings.
"""
def xbmcpath(path,filename):
     translatedpath = os.path.join(xbmc.translatePath( path ), ''+filename+'')
     return translatedpath

#CONSTANTS
_PLUG = Addon('plugin.video.putlockertv', sys.argv)

USER_AGENT = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"

#pulockertv constants
putlocker_URL = 'http://www.putlockertvshows.me'
urllist = putlocker_URL+ '/tv-shows.list.html'
urlimages = putlocker_URL+ '/p/'
urlwatch = putlocker_URL+ '/watch/'
allurl = putlocker_URL + '/tv-shows-list.html'

adatapath = 'special://profile/addon_data/plugin.video.putlockertv'
metapath = adatapath+'/mirror_page_meta_cache'
downinfopath = adatapath+'/downloadinfologs'
transdowninfopath = xbmcpath(downinfopath,'')
transmetapath = xbmcpath(metapath,'')
translateddatapath = xbmcpath(adatapath,'')
path = adatapath
datapath = _PLUG.get_profile()
artdir = "special://home/addons/plugin.video.putlockertv/resources/media/"
downloadScript = "special://home/addons/plugin.video.putlockertv/resources/lib/download.py"
textBoxesScript = "special://home/addons/plugin.video.putlockertv/resources/lib/textBoxes.py"

#cookie constants
cookie_path = os.path.join(datapath)
cookiejar = os.path.join(cookie_path,'losmovies.lwp')
net = Net()


# FUNCTIONS USED   

def f7(seq):
    #sorts list
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def trim():
    #gets list of good links to trim non working
    goodlinks = []
    req = urllib2.Request(allurl)
    req.add_header('User-Agent', USER_AGENT)
    response = urllib2.urlopen(req)
    for link in BeautifulSoup(response.read(), parseOnlyThese=SoupStrainer('a', attrs={'class':'lc'})):
        goodlinks.append(link['href'])
    return goodlinks

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
     
def unescape(text):
##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def cleanUnicode(string):
    try:
        string = string.replace("'","").replace(unicode(u'\u201c'), '"').replace(unicode(u'\u201d'), '"').replace(unicode(u'\u2019'),'').replace(unicode(u'\u2026'),'...').replace(unicode(u'\u2018'),'').replace(unicode(u'\u2013'),'-')
        return string
    except:
        return string


#START MAIN SCRIPT
def STARTPOINT():
        addDir('TV (http://putlockertvshows.me)',putlocker_URL,900,artdir+'putlockertv-logo.png')                 


#PUTLOCKERTVSHOWS.ME
def PUTLOCKERMAIN(url):
    goodones = trim()
    print goodones
    req = urllib2.Request(urlimages)
    req.add_header('User-Agent',USER_AGENT)
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response.read())
    for a in soup.findAll('a', href=True):
        if u'/watch/'+a['href'][:-4] in goodones:
            image =  urlimages+ a['href']
            name = a['href'].title().replace('-',' ')[:-4]
            link = urlwatch + a['href'][:-4]+'/'
            if len(name) > 0:
                addDir(name,link,902,image)

def PUTLOCKERSEASONS(url,name,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="/watch/.+?/s(.+?)e.+?.html" class="la">WATCH</a>').findall(link)
        match.sort() # sort list so it shows season one first
        match = f7(match)
        for season in match:
            meta = None
            #getMeta(name=None,season=None,episode=None,year=None,imdbid=None,tvdbid=None):
            try:
                 meta = getMeta(name=name,season='0',episode='0') 
            except:
                 pass
            addDir(name+' - Season '+season,url+'/',903,iconimage,meta=meta,season=season) #adds dir listing of episodes  

def PUTLOCKERTVEPISODES(url,name,season,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        season = str(season)
        print 'SeaSon:'+season
        match=re.compile('<a href="/watch/(.+?)/s'+season+'e(.+?).html" class="la">WATCH</a>').findall(link)
        match.sort() # sort list so it shows first episode first
     
        for name,episode in match:
                url = putlocker_URL+'/watch/'+name+'/s'+season+'e'+episode+'.html'         
                name = re.sub('-', ' ', name)

                meta = None
                #getMeta(name=None,season=None,episode=None,year=None,imdbid=None,tvdbid=None):
                try:
                     meta = getMeta(name=name,season='0',episode='0') 
                except:
                     pass
                addDir(name.title()+' - Season '+season+' - Episode '+episode,url,904,iconimage,meta=meta) #adds dir listing of episodes 

def getData(url,headers={}):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    return data

def ResolveMailRuLink(url):
    m = (url)
    if m:
        items = []
        headers = { "User-Agent":UA, "Referer":referer, "Cookie":cookie }
        # header "Cookie" with parameters need to be set for your download/playback
        quality = "???"
        data = getData(m, headers)
        item = json.loads(data)
        for qual in item[u'videos']:
            if qual == 'sd':
                quality = "480p"
            elif qual == "hd":
                quality = "720p"
            else:
                quality = "???"
            link = item[u'videos'][qual]
            items.append({'quality':quality, 'url':link}) #+'|Cookie='+cookie+'|Referer='+referer})
            
        # best quality
        resolved = sorted(items,key=lambda i:i['quality'])
        #resolved.reverse()
        return resolved[-1][u'url']        
     
def PUTLOCKERPLAY(url,name,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<iframe src="(.+?)" width="600" height="360" frameborder="0" scrolling="no"></iframe>').findall(link)
        media_url = urlresolver.resolve(match[0])
        meta = None
        #getMeta(name=None,season=None,episode=None,year=None,imdbid=None,tvdbid=None):
        try:
             meta = getMeta(name=name,season='0',episode='0') 
        except:
             pass
        for url in match:
                #if url containt '/ifr/' then re-do video link with second url before resolving video link
                if re.search('ifr', url):
                        print 'iframe detected - more required: ' + url
                        url = url.replace('ifr/','ifr/vid/') # need to add vid to help with add clicking thingy
                        print 'iframe detected - more completed: ' + url
                        url = putlocker_URL + url
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', USER_AGENT)
                        response = urllib2.urlopen(req)
                        link=response.read()
                        match=re.compile('<iframe src="(.+?)" width="600" height="360" frameborder="0" scrolling="no"></iframe>').findall(link)
                        media_url = urlresolver.resolve(match[0]) 
                        for url in match:
                                if 'mail.ru' in url:
                                     # From: http://api.video.mail.ru/videos/embed/mail/john.tim/st/8042.html
                                     match=re.compile('mail.ru/videos/embed/mail/(.+?).html').findall(url)
                                     # To: http://api.video.mail.ru/videos/mail/john.tim/st/8042.json
                                     url = 'http://api.video.mail.ru/videos/mail/' + match + '.json'
                                     url = ResolveMailRuLink(url=url)
                                else:
                                     url = urlresolver.HostedMediaFile(url=url).resolve()
                                     
                                print 'final play url: ' + url
                else:
                        url = urlresolver.HostedMediaFile(url=url).resolve()
                        print 'final play url: ' + url
    
                #xbmc.executebuiltin('XBMC.PlayMedia(%s)' % url) 
                #addLink(name,url,'')
                addLink(name,url,iconimage,'tv',meta=meta) #adds link of episode
                

         
             
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

 
def addLink(name,url,iconimage,mediaType=None,infoLabels=False,trailer=None,meta=None):
        ok=True

        downloadPath = _PLUG.get_setting(mediaType+'downpath')
                
        #handle adding context menus
        contextMenuItems = []
        contextMenuItems.append(('Show Information', 'XBMC.Action(Info)',))
        contextMenuItems.append(('Download Video', "RunScript("+downloadScript+","+url.encode('utf-8','ignore')+","+downloadPath+","+name+","+mediaType+")",))
        if trailer is not None:
             contextMenuItems.append(('Watch Trailer', 'xbmc.PlayMedia('+trailer+')',))

        if meta is None:     
             liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
             liz.setProperty('fanart_image', 'special://home/addons/plugin.video.putlockertv/fanart.jpg')
        else:
             liz = xbmcgui.ListItem(name, iconImage=str(meta['cover_url']), thumbnailImage=str(meta['cover_url']))


             liz.setInfo('video', infoLabels=meta)
             liz.setProperty('fanart_image', meta['backdrop_url'])
             
             infoLabels = {}
             infoLabels['title'] = name
             infoLabels['plot'] = cleanUnicode(meta['plot']) # to-check if we need cleanUnicode
             infoLabels['duration'] = str(meta['duration'])
             infoLabels['premiered'] = str(meta['premiered'])
             infoLabels['mpaa'] = str(meta['mpaa'])
             infoLabels['code'] = str(meta['imdb_id'])
             infoLabels['rating'] = float(meta['rating'])
             #infoLabels['overlay'] = meta['watched'] # watched 7, unwatched 6

             if meta.has_key('season_num'):
                 infoLabels['Episode'] = int(meta['episode_num'])
                 infoLabels['Season'] =int(meta['season_num'])
                 print 'No refresh for episodes yet'
             
        liz.setInfo( type="Video", infoLabels=infoLabels )

        if contextMenuItems:
             #print str(contextMenuItems)
             liz.addContextMenuItems(contextMenuItems, replaceItems=True)
             
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
     
def getMeta(name=None,season=None,episode=None,year=None,imdbid=None,tvdbid=None):
        print 'getMeta() ran',name,season,episode,year,imdbid,tvdbid
        useMeta = _PLUG.get_setting('use-meta')
        print useMeta
        if useMeta == 'true':
             print 'use-meta = true'
             metaget=metahandlers.MetaData(translateddatapath)
             if episode and season is not None:
                  print 'getMeta() is tvshow'
                  #get_episode_meta(self, tvshowtitle, imdb_id, season, episode, air_date='', episode_title='', overlay=''):
                  #get season and episode
                  meta=metaget.get_meta('tvshow',name)
                  #meta=megaget.get_episode_meta(name,meta['imdbid'],season,episode)
                  
                  #_get_tv_extra(self, meta):
                  #meta=metaget.get_tv_extra(meta)
             else:
                  #get_meta(self, media_type, name, imdb_id='', tmdb_id='', year='', overlay=6):
                  #get regular
                  meta=metaget.get_meta('movie',name,year=year)
        return meta
     
def addDir(name,url,mode,iconimage,meta=None,season=None):

        
        #handle adding context menus
        contextMenuItems = []
        contextMenuItems.append(('Help', "RunScript("+textBoxesScript+",HELP,"+helpText+")",))

        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url.encode('utf-8','ignore'))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8','ignore'))+ "&season="+str(season)+"&iconimage="+str(iconimage)
        ok=True
        
        if meta is None:     
             liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
             liz.setProperty('fanart_image', 'special://home/addons/plugin.video.putlockertv/fanart.jpg')
        else:
             contextMenuItems.append(('Show Information', 'XBMC.Action(Info)',))
             liz = xbmcgui.ListItem(name, iconImage=str(meta['cover_url']), thumbnailImage=str(meta['cover_url']))


             liz.setInfo('video', infoLabels=meta)
             liz.setProperty('fanart_image', meta['backdrop_url'])

                
             infoLabels = {}
             infoLabels['title'] = name
             infoLabels['plot'] = cleanUnicode(meta['plot']) # to-check if we need cleanUnicode
             infoLabels['duration'] = str(meta['duration'])
             infoLabels['premiered'] = str(meta['premiered'])
             infoLabels['mpaa'] = str(meta['mpaa'])
             infoLabels['code'] = str(meta['imdb_id'])
             infoLabels['rating'] = float(meta['rating'])
             #infoLabels['overlay'] = meta['watched'] # watched 7, unwatched 6

             if meta.has_key('season_num'):
                 infoLabels['Episode'] = int(meta['episode_num'])
                 infoLabels['Season'] =int(meta['season_num'])
                 print 'No refresh for episodes yet'
                 
        liz.setInfo( type="Video", infoLabels={ "Title": name } )

        if contextMenuItems:
             #print str(contextMenuItems)
             liz.addContextMenuItems(contextMenuItems, replaceItems=False)
             
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
#for passing parameters between menus              
params=get_params()
iconimage=None
season=None
url=None
name=None
mode=None

try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        season=urllib.unquote_plus(params["season"])
except:
        pass
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Season: "+str(season)
print "Iconimage: "+str(iconimage)

#main exicution of menu navigation
if mode==None or url==None or len(url)<1:
        print ""
        STARTPOINT()
        
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        INDEX2(url,name)

elif mode==3:
        print ""+url
        INDEX3(url,name)

elif mode==10:
        print ""
        CATEGORIES()

elif mode==100:
        print""
        BARWOMAIN()
        
elif mode==11:
        print""
        BARWOGENRE()

elif mode==112:
        print""
        BARWOGENRELIST(url,name)

elif mode==113:
        print""
        BARWOMOVIE(url,name)
       
elif mode==300:
        print""
        BUNNYMAIN()
        
elif mode==311:
        print""
        BUNNYGENRE()

elif mode==312:
        print""
        BUNNYGENRELIST(url,name)

elif mode==313:
        print""
        BUNNYMOVIE(url,name)

elif mode==315:
        print""
        SEARCHSITE(url)

elif mode==4:
        print""
        SEARCHSITETV(url)

elif mode==600:
        print""
        MUCHMAIN()
        
elif mode==900:
        print""
        PUTLOCKERMAIN(url)

elif mode==902:
        print""
        PUTLOCKERSEASONS(url,name,iconimage)

elif mode==903:
        print""
        PUTLOCKERTVEPISODES(url,name,season,iconimage)
        
elif mode==904:
        print""
        PUTLOCKERPLAY(url,name,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
