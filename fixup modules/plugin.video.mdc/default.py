import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
from BeautifulSoup import BeautifulSoup
try:
    import json
except:
    import simplejson as json
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
    
cache = StorageServer.StorageServer("mydamnchannel", 24)
addon = xbmcaddon.Addon(id='plugin.video.mdc')
home = addon.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
base = 'http://www.mydamnchannel.com'


def makeRequest(url,data=None,headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
                           'Referer' : 'http://www.mydamnchannel.com/channels'}
            req = urllib2.Request(url,data,headers)
            response = urllib2.urlopen(req)
            link = response.read()
            response.close()
            return link
        except urllib2.URLError, e:
            print 'We failed to open "%s".' % url
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
                xbmc.executebuiltin("XBMC.Notification(No Agenda,HTTP Error: "+str(e.code)+",5000,"+icon+")")
                
                
def cache_cats():
        return(makeRequest('http://www.mydamnchannel.com/channels'))
                

def Categories():
        thumbs = {
            'Adam Carolla' : 'http://content.MyDamnChannel.com/datastore/channels/RDACSchannelbanner021912.jpg',
            'Andy Milonakis' : 'http://content.MyDamnChannel.com/datastore/channels/RDandychannelbanner035331.jpg',
            'Answerly' : 'http://content.MyDamnChannel.com/datastore/channels/Answerlychannelbanner092458.jpg',
            'Back On Topps' : 'http://content.MyDamnChannel.com/datastore/channels/Toppschannelbanner094617.jpg',
            'Bruce McCall' : 'http://content.MyDamnChannel.com/datastore/channels/mccall997x316024131.jpg',
            'Carnival of Stuff' : 'http://content.MyDamnChannel.com/datastore/channels/CoS997x80025916.jpg',
            'Celebrity Autobiography' : 'http://content.MyDamnChannel.com/datastore/channels/CelebAutochannelbanner093842.jpg',
            'Co-op Of The Damned' : 'http://content.MyDamnChannel.com/datastore/channels/CotDBanner996x85032317.jpg',
            'Coffey Chat' : 'http://content.MyDamnChannel.com/datastore/channels/SCbanner996x85023453.jpg',
            "Cookin' With Coolio" : 'http://content.MyDamnChannel.com/datastore/channels/Cooliochannelbanner093911.jpg',
            'Culture Catch' : 'http://content.MyDamnChannel.com/datastore/channels/CC997x80020950.jpg',
            'Daddy Knows Best' : 'http://content.MyDamnChannel.com/datastore/channels/DKB996x80114653.jpg',
            'Daily Grace' : 'http://content.MyDamnChannel.com/datastore/channels/RDGracechannelbanner091255.jpg',
            'Dame Delilah' : 'http://content.MyDamnChannel.com/datastore/channels/DD997x80021306.jpg',
            'Daily Grace Archives' : 'http://content.mydamnchannel.com/datastore/channels/RDGracechannelbanner091255.jpg',
            'Dicki' : 'http://content.MyDamnChannel.com/datastore/channels/Dickichannelbanner093937.jpg',
            'Don Was' : 'http://content.MyDamnChannel.com/datastore/channels/DonWaschannelbanner094002.jpg',
            'Gigi' : 'http://content.MyDamnChannel.com/datastore/channels/gigichannelbanner094030.jpg',
            'Gilbert Gets It' : 'http://content.MyDamnChannel.com/datastore/channels/gilbert997x80092934.jpg',
            'Go Sukashi!' : 'http://content.MyDamnChannel.com/datastore/channels/Sukashichannelbanner094508.jpg',
            'Grace N Michelle' : 'http://content.MyDamnChannel.com/datastore/channels/GnM997x80022004.jpg',
            'Harry Shearer' : 'http://content.MyDamnChannel.com/datastore/channels/Shearerchannelbanner094339.jpg',
            'Horrible People' : 'http://content.MyDamnChannel.com/datastore/channels/HPchannelbanner094130.jpg',
            'Jimmy Kimmel' : 'http://content.MyDamnChannel.com/datastore/channels/RDKimmelchannelbanner024401.jpg',
            'Jon Friedman' : 'http://content.MyDamnChannel.com/datastore/channels/RDJonFriedmanchannelbanner121339.jpg',
            'Linked Out' : 'http://content.MyDamnChannel.com/datastore/channels/LinkedOut996x85111059.jpg',
            'Mark Malkoff' : 'http://content.MyDamnChannel.com/datastore/channels/RDMalkoffchannelbanner024457.jpg',
            'McMayhem' : 'http://content.MyDamnChannel.com/datastore/channels/RDMcMayhemchannelbanner082645.jpg',
            'Murderfist' : 'http://content.MyDamnChannel.com/datastore/channels/MFchannelbanner094255.jpg',
            'My Damn Channel Live' : 'http://content.MyDamnChannel.com/datastore/channels/RDMDClivechannel032712012359.jpg',
            'Pilot Season' : 'http://content.MyDamnChannel.com/datastore/channels/Pilotchannelbanner094315.jpg',
            'Product Displacement' : 'http://content.MyDamnChannel.com/datastore/channels/ProductDisplacementBanner996x85105729.jpg',
            'Promos' : 'http://content.MyDamnChannel.com/datastore/channels/MDClivechannelbanner113410.jpg',
            'Spinal Tap' : 'http://content.MyDamnChannel.com/datastore/channels/SpinalTapchannelbanner094426.jpg',
            'Status Kill' : 'http://content.MyDamnChannel.com/datastore/channels/StatusKillchannelbanner094447.jpg',
            'Stella' : 'http://content.MyDamnChannel.com/datastore/channels/RDStellachannelbanner025639.jpg',
            'SUBWAY Fresh Artists' : 'http://content.MyDamnChannel.com/datastore/channels/RDSUBBchannelbanner091006.jpg',
            'Super Amazing Project' : 'http://content.MyDamnChannel.com/datastore/channels/SuperAmazingchannelbanner075354.jpg',
            'SUPEREGO' : 'http://content.MyDamnChannel.com/datastore/channels/RDsuperegochannelbanner044303.jpg',
            'The Temp Life' : 'http://content.MyDamnChannel.com/datastore/channels/RDTempLifechannelbanner025825.jpg',
            'The Tweekly News' : 'http://content.MyDamnChannel.com/datastore/channels/tweekly997x316tweetbackground012244.jpg',
            'The Worst Generation' : 'http://content.MyDamnChannel.com/datastore/channels/RDTWGchannelbanner030002.jpg',
            'Versailles' : 'http://content.MyDamnChannel.com/datastore/channels/RDVersailleschannelbanner030031.jpg',
            'Wainy Days' : 'http://content.MyDamnChannel.com/datastore/channels/RDWDchannelbanner093257.jpg',
            'Webventures...' : 'http://content.MyDamnChannel.com/datastore/channels/RDWebVchannelbanner091712.jpg',
            'Workless' : 'http://content.MyDamnChannel.com/datastore/channels/WorklessBanner996x85105829.jpg',
            'WTF with Marc Maron' : 'http://content.MyDamnChannel.com/datastore/channels/RDWTFchannelbanner030317.jpg',
            'You Rock At Photoshop' : 'http://content.MyDamnChannel.com/datastore/channels/RDYRAPchannelbanner081636.jpg',
            'You Suck at Photoshop' : 'http://content.MyDamnChannel.com/datastore/channels/RDYSAPchannelbanner030448.jpg'
            }
        soup = BeautifulSoup(cache.cacheFunction(cache_cats), convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = soup('ul', attrs={'id' : "channel-list"})[0]('a')
        for i in items:
            url = 'http://www.mydamnchannel.com'+i['href']
            name = i.contents[1]
            try:
                thumb = thumbs[name]
            except:
                print name
                thumb = i.img['src']
            addDir(name, url, 1, thumb)
            

def get_total_episodes(channel_id, referer):
        post_url = 'http://www.mydamnchannel.com/webservices/mydamnchannel.asmx/GetTotalNumEpisodes'
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
                   'Referer' : referer,
                   'Content-Type' : 'application/json; charset=UTF-8'}
        data = "{'channelID': %s}" %channel_id
        j_data = json.loads(makeRequest(post_url, data, headers))
        return j_data['d']

            
def getVideos(url):
        data = makeRequest(url)
        channel_id = url.split('_')[-1].split('.')[0]
        total = get_total_episodes(channel_id, url)
        if total/9.0 > total/9:
            total_pages = (total/9)+1
        else: total_pages = total/9
        current_page = re.compile('current_page: (.+?)\r\n                }').findall(data)[0]
        soup = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
        items = soup('div', attrs={'id' : 'previous_episodes'})[0]('li')
        for i in items:
            url_ = 'http://www.mydamnchannel.com'+i.a['href']
            name = i.h2.string
            if name is None:
                try:
                    name = i.h2.contents[0] + i.h2.contents[2]
                except:
                    name = i.h2.contents[0]
            desc = i.p.string.strip()
            thumb = i.img['src']
            addLink(name.encode('ascii', 'ignore'), url_, 2, thumb)
        if total_pages > 1:
            pagnation(current_page, current_page, total_pages, url)  
        

def get_episodes_by_page(referer, start_page, page, total_pages):
        post_url = 'http://www.mydamnchannel.com/webservices/mydamnchannel.asmx/GetEpisodesByPage'
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
                   'Referer' : referer,
                   'Content-Type' : 'application/json; charset=UTF-8'}
        channel_id = referer.split('_')[-1].split('.')[0]
        data = "{'channelID': "+channel_id+", 'page': "+str(int(page)-1)+", 'pageSize': '9'}"
        j_data = json.loads(makeRequest(post_url, data, headers))
        items = j_data['d']
        for i in items:
            episode_id = i['episodeID']
            soup = BeautifulSoup(i['markup'], convertEntities=BeautifulSoup.HTML_ENTITIES)
            href = soup.a['href']
            thumb = soup.img['src']
            title = soup.h2.string
            if title is None:
                try:
                    title = soup.h2.contents[0] + soup_.h2.contents[2]
                except:
                    title = soup.h2.contents[0]
            desc = soup.p.string
            addLink(title.encode('ascii', 'ignore'), base+href, 2, thumb)
        pagnation(start_page, page, total_pages, referer)  
            
            
def pagnation(start_page, current_page, total_pages, url):
        print "pagnation current: " + current_page
        print "pagnation total: " + str(total_pages)
        mode = 3
        if int(current_page) != int(total_pages):
            next_page = str(int(current_page)+1)
            if start_page == next_page:
                mode = 2
            else: mode = 3
            addDir('Next Page('+next_page+' of '+str(total_pages)+')',
            url, mode, icon, start_page, next_page, total_pages)
        if int(current_page) > 1:
            previous_page = str(int(current_page)-1)
            if start_page == previous_page:
                mode = 2
            else: mode = 3
            addDir('Previous Page('+previous_page+' of '+str(total_pages)+')',
            url, mode, icon, start_page, previous_page, total_pages)
        if int(total_pages) > 3:
            if (int(current_page) > (int(start_page)+3)) or (int(current_page) < (int(start_page)-3)):
                addDir('Main Menu', '', 4, icon)


def setVideoUrl(url):
        soup = BeautifulSoup(makeRequest(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        try:
            path = soup.source['src']
        except:
            print '--- No source element ---'
            if 'youtube' in soup.iframe['src']:
                print ' --- youtube link ---'
                youtube_id = soup.iframe['src'].split('?')[0].split('/')[-1]
                path = 'plugin://plugin.video.youtube/?action=play_video&videoid='+youtube_id
            else: print ' ------ not youtube --------'
        item = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            
                
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


def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,start_page='',page='',total_pages=''):
        u=(sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&page="+str(page)
        +"&start_page="+str(start_page)+"&total_pages="+str(total_pages)+"&name="+urllib.quote_plus(name))
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


params=get_params()
url=None
name=None
mode=None
page=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    page=int(params["page"])
except:
    pass
try:
    start_page=int(params["start_page"])
except:
    pass
try:
    total_pages=int(params["total_pages"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
    Categories()
        
if mode==1:
    getVideos(url)
        
if mode==2:
    setVideoUrl(url)
        
if mode==3:
    get_episodes_by_page(url, start_page, str(page), str(total_pages))
        
if mode==4:
    xbmc.executebuiltin("XBMC.Container.Update(%s, replace)" %sys.argv[0])
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))