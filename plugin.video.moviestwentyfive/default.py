import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,xbmc,xbmcaddon,os
from addon.common.addon import Addon
from addon.common.net import Net
import silent


#www.movie25.so - by The_Silencer 2013 v0.9


addon_id = 'plugin.video.moviestwentyfive'
local = xbmcaddon.Addon(id=addon_id)
movie25path = local.getAddonInfo('path')
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()
art = movie25path+'/art'
net = Net()


#Kid Mode Menu
def KIDMODE():
        addDir('Parent View','http://www.movie25.so/',46,os.path.join(art,'PARENT_VIEW.png'),None,None)
        addDir('Kid Movies','http://www.movie25.so/',44,os.path.join(art,'KIDS_MOVIES.png'),None,None)
        addDir('Kid TV Shows','http://www.movie25.so/',45,os.path.join(art,'KIDS_TV.png'),None,None)

def PARENTS():
        Password = local.getSetting('parent-password')
        keyb = xbmc.Keyboard('', 'Please Enter the Parent Password')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)  
                if encode != Password:
                        addDir('Sorry wrong password please try again',url,46,'',None,None)
                else:
                        addDir('Movies','http://www.movie25.so/',16,os.path.join(art,os.path.join(art,'MOVIES.png')),None,None)
                        addDir('TV','http://www.movie25.so/',17,os.path.join(art,os.path.join(art,'TV_SHOWS.png')),None,None)
                        addDir('Settings','http://www.movie25.so/',18,os.path.join(art,os.path.join(art,'SETTINGS.png')),None,None)

def KIDMOVIES():
        MYFAVS = silent.getFavoritesKIDMOVIE()
        try:
                for name,url,year in MYFAVS:
                        addFAVDir(name,url,year)
        except:
                pass

def KIDTV():
        MYFAVS = silent.getFavoritesKIDTV()
        try:
                for name,url,types in MYFAVS:
                        addFAVDirTV(name,url,types)
        except:
                pass

#Urlresolver setttings
def ResolverSettings():
        urlresolver.display_settings()


def SETTINGS():
        addDir('Add-on Settings','http://www.movie25.so/',42,os.path.join(art,'ADDON.png'),None,None)
        addDir('Resolver Settings','http://www.movie25.so/',43,os.path.join(art,'RESOLVER.png'),None,None)

#Main menu
def CATEGORIES():
        KidMode = local.getSetting('kid-mode')
        if KidMode == 'true':
                KIDMODE()
        else:
                addDir('Movies','http://www.movie25.so/',16,os.path.join(art,'MOVIES.png'),None,None)
                addDir('TV','http://www.movie25.so/',17,os.path.join(art,'TV_SHOWS.png'),None,None)
                addDir('Settings','http://www.movie25.so/',18,os.path.join(art,'SETTINGS.png'),None,None)

#Menu for Movies
def MOVIES():
        MYFAVS = silent.getFavoritesKIDMOVIE2()
        addDir('Featured','http://www.movie25.so/featured-movies/',1,os.path.join(art,'featured1.png'),None,None)
        addDir('New Releases','http://www.movie25.so/movies/new-releases/',1,os.path.join(art,'NEW_RELEASES.png'),None,None)
        addDir('Latest Added','http://www.movie25.so/movies/latest-added/',1,os.path.join(art,'LATEST_ADDED.png'),None,None)
        addDir('Latest HD','http://www.movie25.so/movies/latest-hd-movies/',1,os.path.join(art,'latesthd.png'),None,None)
        addDir('Most Viewed','http://www.movie25.so/movies/most-viewed/',1,os.path.join(art,'MOST_VIEWED.png'),None,None)
        addDir('Most Voted','http://www.movie25.so/movies/most-viewed/',1,os.path.join(art,'MOST_VOTED.png'),None,None)
        addDir('A-Z','http://www.movie25.so/',5,os.path.join(art,'A_Z.png'),None,None)
        addDir('Genres','http://www.movie25.so/',8,os.path.join(art,'GENRE.png'),None,None)
        addDir('Year','http://www.movie25.so/',13,os.path.join(art,'year1.png'),None,None)
        addDir('Search','http://www.movie25.so/',6,os.path.join(art,'search1.png'),None,None)
        addDir('Favorites','http://www.movie25.so/',7,os.path.join(art,'FAVORITE.png'),None,None)
        if MYFAVS:
                addDir('Kid Movies','http://www.movie25.so/',44,os.path.join(art,'KIDS_MOVIES.png'),None,None)
                

#List of Years
def YEAR():
        addDir('2014','http://www.movie25.so/search.php?year=2014',12,'',None,None)
        addDir('2013','http://www.movie25.so/search.php?year=2013',12,'',None,None)
        addDir('2012','http://www.movie25.so/search.php?year=2012',12,'',None,None)
        addDir('2011','http://www.movie25.so/search.php?year=2011',12,'',None,None)
        addDir('2010','http://www.movie25.so/search.php?year=2010',12,'',None,None)
        addDir('2009','http://www.movie25.so/search.php?year=2009',12,'',None,None)
        addDir('2008','http://www.movie25.so/search.php?year=2008',12,'',None,None)
        addDir('2007','http://www.movie25.so/search.php?year=2007',12,'',None,None)
        addDir('2006','http://www.movie25.so/search.php?year=2006',12,'',None,None)
        addDir('2005','http://www.movie25.so/search.php?year=2005',12,'',None,None)
        addDir('2004','http://www.movie25.so/search.php?year=2004',12,'',None,None)
        addDir('2003','http://www.movie25.so/search.php?year=2003',12,'',None,None)
        addDir('2002','http://www.movie25.so/search.php?year=2002',12,'',None,None)
        addDir('2001','http://www.movie25.so/search.php?year=2001',12,'',None,None)
        addDir('2000','http://www.movie25.so/search.php?year=2000',12,'',None,None)
        addDir('1999','http://www.movie25.so/search.php?year=1999',12,'',None,None)
        addDir('1998','http://www.movie25.so/search.php?year=1998',12,'',None,None)
        addDir('1997','http://www.movie25.so/search.php?year=1997',12,'',None,None)
        addDir('1996','http://www.movie25.so/search.php?year=1996',12,'',None,None)
        addDir('1995','http://www.movie25.so/search.php?year=1995',12,'',None,None)
        addDir('1994','http://www.movie25.so/search.php?year=1994',12,'',None,None)
        addDir('1993','http://www.movie25.so/search.php?year=1993',12,'',None,None)
        addDir('1992','http://www.movie25.so/search.php?year=1992',12,'',None,None)
        addDir('1991','http://www.movie25.so/search.php?year=1991',12,'',None,None)
        addDir('1990','http://www.movie25.so/search.php?year=1990',12,'',None,None)
        addDir('1989','http://www.movie25.so/search.php?year=1989',12,'',None,None)
        addDir('1988','http://www.movie25.so/search.php?year=1988',12,'',None,None)
        addDir('1987','http://www.movie25.so/search.php?year=1987',12,'',None,None)
        addDir('1986','http://www.movie25.so/search.php?year=1986',12,'',None,None)
        addDir('1985','http://www.movie25.so/search.php?year=1985',12,'',None,None)
        addDir('1984','http://www.movie25.so/search.php?year=1984',12,'',None,None)
        addDir('1983','http://www.movie25.so/search.php?year=1983',12,'',None,None)
        addDir('1982','http://www.movie25.so/search.php?year=1982',12,'',None,None)
        addDir('1981','http://www.movie25.so/search.php?year=1981',12,'',None,None)
        addDir('1980','http://www.movie25.so/search.php?year=1980',12,'',None,None)
        addDir('1979','http://www.movie25.so/search.php?year=1979',12,'',None,None)
        addDir('1978','http://www.movie25.so/search.php?year=1978',12,'',None,None)
        addDir('1977','http://www.movie25.so/search.php?year=1977',12,'',None,None)
        addDir('1976','http://www.movie25.so/search.php?year=1976',12,'',None,None)
        addDir('1975','http://www.movie25.so/search.php?year=1975',12,'',None,None)
        addDir('1974','http://www.movie25.so/search.php?year=1974',12,'',None,None)
        addDir('1973','http://www.movie25.so/search.php?year=1973',12,'',None,None)
        addDir('1972','http://www.movie25.so/search.php?year=1972',12,'',None,None)
        addDir('1971','http://www.movie25.so/search.php?year=1971',12,'',None,None)
        addDir('1970','http://www.movie25.so/search.php?year=1970',12,'',None,None)
        
########
#TV Menu
########
def TV():
        MYFAVS = silent.getFavoritesKIDTV2()
        addDirTV('Most Popular','http://watchseries.to/',21,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Newest Episodes','http://watchseries.to/latest',36,os.path.join(art,'NEW_EPISODES.png'),None)
        addDirTV('A-Z','http://watchseries.to/letters/A',33,os.path.join(art,'A_Z.png'),None)
        addDirTV('Genres','http://watchseries.to/genres/drama',35,os.path.join(art,'GENRE.png'),None)
        addDirTV('TV Schedule','http://www.watchseries.to/tvschedule/-1',38,os.path.join(art,'TV_SCHEDULE.png'),None)
        addDirTV('Search','http://watchseries.to/',37,os.path.join(art,'search1.png'),None)
        addDirTV('Favorites','http://watchseries.to/',39,os.path.join(art,'FAVORITE.png'),None)
        if MYFAVS:
                addDir('Kid TV Shows','http://www.movie25.so/',45,os.path.join(art,'KIDS_TV.png'),None,None)
                

#Popular TV menu
def POPULAR():
        addDirTV('Popular this week','http://watchseries.to/new',22,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Series','http://watchseries.to/',26,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Cartoons','http://watchseries.to/',27,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Documentaries','http://watchseries.to/',28,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Shows','http://watchseries.to/',29,os.path.join(art,'MOST_POPULAR.png'),None)
        addDirTV('Popular Sports','http://watchseries.to/',30,os.path.join(art,'MOST_POPULAR.png'),None)

#TV Schedule menu
def SCHEDULE(url):
        match=re.compile('<a href="(.+?)">(.+?)</a>').findall(net.http_GET(url).content)
        for url,name in match:
                ok = '/tvschedule/'
                nono = 'TV Schedule'
                if ok in url:
                        if name not in nono:
                                addDirTV(name,'http://watchseries.to'+url,36,'',None)
                        
#A-Z TV list
def AZTV(url):
        match=re.compile('<a href="(.+?)">(.+?)</a></li>').findall(net.http_GET(url).content)
        for url,name in match:
                icon = os.path.join(art,name+'.png')
                ok = ['09','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
                if name in ok:
                        addDirTV(name,'http://watchseries.to'+url,34,icon,None)

#Genres TV list
def GENRESTV(url):
        match=re.compile('<a href="(.+?)" class="sr-header" title=".+?">(.+?)</a>').findall(net.http_GET(url).content)
        for url,name in match:
                nono = ['Home', 'New Releases', 'Latest Added', 'Featured Movies', 'Latest HD Movies', 'Most Viewed', 'Most Viewed', 'Most Voted', 'Genres', 'Submit Links']
                if name not in nono:
                        addDirTV(name,'http://www.watchseries.to'+url,34,'',None)

#Search for Movies
def SEARCHTV(url):
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search TV Shows')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                print encode
                url = 'http://www.watchseries.to/search/'+encode
                print url
                match=re.compile('<td valign="top" style="padding-left: 10px;">.+?<a href="(.+?)" title="(.+?)">',re.DOTALL).findall(net.http_GET(url).content) 
                for url,name in match:
                        name = silent.CLEAN(name)
                        if EnableMeta == 'true':
                               addDirTV(name,'http://watchseries.to'+url,31,'','tvshow')
                        if EnableMeta == 'false':
                               addDirTV(name,'http://watchseries.to'+url,31,'',None)

def LIST(url):
        EnableMeta = local.getSetting('Enable-Meta')
        match=re.compile('<li><a href="(.+?)" title=".+?">(.+?)<span class="epnum">(.+?)</span></a></li>').findall(net.http_GET(url).content)
        for url,name,year in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,'http://watchseries.to'+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,'http://watchseries.to'+url,31,'',None)

def NEWLINKS(url):
        EnableMeta = local.getSetting('Enable-Meta')
        match=re.compile('<li><a href="(.+?)">(.+?) Seas. (.+?) Ep. (.+?) \(.+?\).+?</li>',re.DOTALL).findall(net.http_GET(url).content)
        for url,name,season,episode in match:
                nono = '</a>'
                name = silent.CLEAN(name)
                if nono not in name:
                        if EnableMeta == 'true':
                                addDirTV('%s - Seas. %s : Ep. %s' %(name,season,episode),'http://watchseries.to'+url+'@'+name+'@'+season+'@'+episode,23,'','new')
                        if EnableMeta == 'false':
                                addDirTV(name,'http://watchseries.to'+url,23,'',None)

def INDEXTV(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<ul class="listings">(.+?)</ul>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<li><a href="(.+?)">(.+?) Seas..+?</a></li>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,'http://watchseries.to'+url,23,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,'http://watchseries.to'+url,23,'',None)

def INDEX2(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular Series\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,'http://watchseries.to'+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,'http://watchseries.to'+url,31,'',None)

def INDEX3(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular Cartoons\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,'http://watchseries.to'+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,'http://watchseries.to'+url,31,'',None)

def INDEX4(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular Documentaries\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,'http://watchseries.to'+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,'http://watchseries.to'+url,31,'',None)

def INDEX5(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular Shows\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,'http://watchseries.to'+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,'http://watchseries.to'+url,31,'',None)

def INDEX6(url):
        EnableMeta = local.getSetting('Enable-Meta')
        data=re.compile('<img src=".+?"/>&nbsp;Most Popular  Sports\n\t\t\t\t</div>(.+?)</div>',re.DOTALL).findall(net.http_GET(url).content)
        pattern = '<a href="(.+?)" title="watch online (.+?)">.+?</a>'
        match = re.findall(pattern,str(data))
        for url,name in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDirTV(name,'http://watchseries.to'+url,31,'','tvshow')
                if EnableMeta == 'false':
                        addDirTV(name,'http://watchseries.to'+url,31,'',None)

#Find Seasons for shows
def SEASONS(name,url):
        title = name
        match=re.compile('<h2 class="lists"><a href="(.+?)">(.+?)</h2>').findall(net.http_GET(url).content)
        for url,name in match:
                addDirTV(name,'http://watchseries.to'+url+'@'+title,32,'','seasons')

#Find Episodes for shows
def EPISODES(name,url):
        title = url.split('@')[1]
        url = url.split('@')[0]
        season = name
        match=re.compile('<li><a href="(.+?)"><span class="">(.+?)&nbsp;&nbsp;&nbsp;(.+?)</span><span class="epnum">(.+?)</span></a></li>').findall(net.http_GET(url).content)
        for url,episode,name,date in match:
                name = silent.CLEAN(name)
                addDirTV('%s    :    %s   :   %s' %(episode,date,name),'http://watchseries.to'+url+'@'+title+'@'+season+'@'+episode,23,'','new')

#First page with Hosters
def VIDEOLINKSTV(url):
        episode = url.split('@')[3]
        season = url.split('@')[2]
        title = url.split('@')[1]
        url = url.split('@')[0]
        match=re.compile('<a target="_blank" href="(.+?)" class="buttonlink" title="(.+?)" style="cursor:pointer;"').findall(net.http_GET(url).content)
        match2=re.compile('<p><strong>Sorry, there are no links available for this (.+?).</strong></p>').findall(net.http_GET(url).content)
        for url,name in match:
                addDirTV(name,'http://watchseries.to'+url+'@'+title+'@'+season+'@'+episode,24,'',None)
        for name in match2:
                addDirTV('[B][COLOR yellow]Sorry, no links available yet[/COLOR][/B]','http://watchseries.to'+url,24,'',None)

#Get the Final Hoster link
def VIDEOLINKS2TV(name,url):
        episode = url.split('@')[3]
        season = url.split('@')[2]
        title = url.split('@')[1]
        url = url.split('@')[0]
        match=re.compile('<a href="(.+?)" class="myButton">Click Here to Play</a>').findall(net.http_GET(url).content)
        for url in match:
                STREAMTV(name,url+'@'+title+'@'+season+'@'+episode)

#Pass url to urlresolver
def STREAMTV(name,url):
        EnableMeta = local.getSetting('Enable-Meta')
        if EnableMeta == 'true':
                infoLabels = silent.GRABMETATV(name,url,'new')
                try: img = infoLabels['cover_url']
                except: img= iconimage
        episode = url.split('@')[3]
        season = url.split('@')[2]
        title = url.split('@')[1]
        url = url.split('@')[0]
        try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
                print streamlink
                addLinkTV(name,streamlink+'@'+title+'@'+season+'@'+episode,img)
        except:
                silent.Notify('small','Sorry Link Removed:', 'Please try another one.',9000)

def addLinkTV(name,url,iconimage):
        episode = url.split('@')[3]
        season = url.split('@')[2]
        title = url.split('@')[1]
        url = url.split('@')[0]
        season = season.replace('Season ', '')
        episode = episode.replace('Episode ', '')
        ok=True
        liz=xbmcgui.ListItem('%s (%sx%s)' %(title,season,episode), iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": '%s (%sx%s)' %(title,season,episode) } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok

def addDirTV(name,url,mode,iconimage,types):
        EnableFanArt = local.getSetting('Enable-Fanart')
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = silent.GRABMETATV(name,url,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img= iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        contextMenuItems = []
        if mode == 31:
                contextMenuItems = []
                contextMenuItems.append(('TV Show Information', 'XBMC.Action(Info)'))
                contextMenuItems.append(('Add to Favorites', 'XBMC.RunPlugin(%s?mode=40&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
                contextMenuItems.append(('Add to Kids TV', 'XBMC.RunPlugin(%s?mode=49&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
                
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addFAVDirTV(name,url,types):
        EnableFanArt = local.getSetting('Enable-Fanart')
        mode = 31
        iconimage = ''
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = silent.GRABMETATV(name,url,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        ###Add to Library Context Menu
        contextMenuItems = []
        contextMenuItems.append(('TV Show Information', 'XBMC.Action(Info)'))
        contextMenuItems.append(('Remove from Favorites', 'XBMC.RunPlugin(%s?mode=41&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
        contextMenuItems.append(('Remove from Kids TV', 'XBMC.RunPlugin(%s?mode=50&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
        
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ##############################
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

########
########
########

#Return Favorites List *temp need to fix in silent*
def GETMYFAVS():
        MYFAVS = silent.getFavorites()
        try:
                for name,url,year in MYFAVS:
                        addFAVDir(name,url,year)
        except:
                pass

def GETMYFAVSTV():
        MYFAVS = silent.getFavoritesTV()
        try:
                for name,url,types in MYFAVS:
                        addFAVDirTV(name,url,types)
        except:
                pass

#Search for movies by year selected
def YEARFIND(url):
        EnableMeta = local.getSetting('Enable-Meta')
        pages=re.compile('found&nbsp;&nbsp;&nbsp;&nbsp;(.+?)/(.+?)&nbsp;Page').findall(net.http_GET(url).content)
        match=re.compile('<h1><a href="(.+?)" target="_blank">\n\t\t\t\t\t  (.+?) \(([\d]{4})\)\t\t\t\t\t  </a></h1>').findall(net.http_GET(url).content)
        nextpage=re.compile('<font color=\'#FF3300\'>.+?</font>&nbsp;<a href=\'(.+?)\' >.+?</a>').findall(net.http_GET(url).content)
        for current,last in pages:
                addDir('[B][COLOR yellow]Page  %s  of  %s[/COLOR][/B]'%(current,last),'http://www.movie25.so'+url,2,'',None,None)
        for url,name,year in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDir(name,'http://www.movie25.so'+url,2,'','Movie',year)
                if EnableMeta == 'false':
                        addDir(name,'http://www.movie25.so'+url,2,'',None,None)
        if nextpage:
                print nextpage
                url = str(nextpage)
                print url
                url = url.replace('[u\'','')
                url = url.replace(']','')
                url = url.replace('\'','')
                url = '/'+url
                print url
                if EnableMeta == 'true':
                        addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]','http://www.movie25.so'+url,12,'',None,None)
                if EnableMeta == 'false':
                        addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]','http://www.movie25.so'+url,12,'',None,None)
                        
#A-Z list
def AZ(url):
        match2=re.compile('<a href="(.+?)">(.+?)</a>').findall(net.http_GET(url).content)
        match=re.compile('<a href="(.+?)"\ >(.+?)</a>').findall(net.http_GET(url).content)
        for url,name in match2:
                ok = ['0-9']
                if name in ok:
                        addDir(name,'http://www.movie25.so'+url,1,'',None,None)
        for url,name in match:
                ok = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
                A = ['A']
                if name in ok:
                        icon = os.path.join(art,name+'.png')
                        if name in A:
                                url = '/movies/a/'
                        addDir(name,'http://www.movie25.so'+url,1,icon,None,None)

#Genres list
def GENRES(url):
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(net.http_GET(url).content)
        for url,name in match:
                nono = ['Home', 'New Releases', 'Latest Added', 'Featured Movies', 'Latest HD Movies', 'Most Viewed', 'Most Viewed', 'Most Voted', 'Genres', 'Submit Links']
                if name not in nono:
                        addDir(name,'http://www.movie25.so'+url,1,'',None,None)

#Search for Movies
def SEARCH(url):
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search Movie25')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                encode = encode.replace('%20', '+')
                print encode
                url = 'http://www.movie25.so/search.php?key='+encode+'&submit='
                print url
                match=re.compile('<h1><a href="(.+?)" target="_blank">\n\t\t\t\t\t  (.+?) \(([\d]{4})\)\t\t\t\t\t  </a></h1>').findall(net.http_GET(url).content)
                for url,name,year in match:
                        name = silent.CLEAN(name)
                        if EnableMeta == 'true':
                               addDir(name,'http://www.movie25.so'+url,2,'','Movie',year)
                        if EnableMeta == 'false':
                               addDir(name,'http://www.movie25.so'+url,2,'',None,None)

def INDEX(url):
        EnableMeta = local.getSetting('Enable-Meta')
        pages=re.compile('found&nbsp;&nbsp;&nbsp;&nbsp;(.+?)/(.+?)&nbsp;Page').findall(net.http_GET(url).content)
        match=re.compile('<div class="movie_pic"><a href="(.+?)"  target="_self">\n\t\t\t\t  \t\t\t\t  <img src=".+?" width="101" height="150" alt="(.+?)\(([\d]{4})\)"',re.DOTALL).findall(net.http_GET(url).content)
        nextpage=re.compile('<font color=\'#FF3300\'>.+?</font>&nbsp;<a href=\'(.+?)\' >.+?</a>').findall(net.http_GET(url).content)
        for current,last in pages:
                addDir('[B][COLOR yellow]Page  %s  of  %s[/COLOR][/B]'%(current,last),'http://www.movie25.so'+url,2,'',None,None)
        for url,name,year in match:
                name = silent.CLEAN(name)
                if EnableMeta == 'true':
                        addDir(name,'http://www.movie25.so'+url,2,'','Movie',year)
                if EnableMeta == 'false':
                        addDir(name,'http://www.movie25.so'+url,2,'',None,None)

        if nextpage:
                print nextpage
                url = str(nextpage)
                print url
                url = url.replace('[u\'','')
                url = url.replace(']','')
                url = url.replace('\'','')
                print url
                if EnableMeta == 'true':
                        addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]','http://www.movie25.so'+url,1,'',None,None)
                if EnableMeta == 'false':
                        addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]','http://www.movie25.so'+url,1,'',None,None)

#First page with Hosters
def VIDEOLINKS(name,url,year):
        EnableMeta = local.getSetting('Enable-Meta')
        iconimage = ''
        name2 = name
        if EnableMeta == 'true':
                infoLabels = silent.GRABMETA(name2,year)
        try: img = infoLabels['cover_url']
        except: img = iconimage
        match2=re.compile('<h1 >Links - Quality\n(.+?)</h1>').findall(net.http_GET(url).content)
        match=re.compile('<li class="link_name">\n              (.+?)            </li>\n                        <li class="playing_button"><span><a href="(.+?)"').findall(net.http_GET(url).content)
        if match2:
                quality = str(match2).replace('[','').replace(']','').replace("'",'').replace(' ','').replace('u','')
        else:
                quality = 'Not Specified'
        List=[]; ListU=[]; c=0
        for name,url in match:
                url = 'http://www.movie25.so'+url+'@'+name2
                c=c+1; List.append(str(c)+'.)  '+name); ListU.append(url)
        dialog=xbmcgui.Dialog()
        rNo=dialog.select('Select A Host........Quality = %s'%quality, List)
        if rNo>=0:
                rName=List[rNo]
                rURL=ListU[rNo]
                VIDEOLINKS2(rName,rURL,year)
        else:
                pass
                
#Get the Final Hoster link
def VIDEOLINKS2(name,url,year):
        EnableMeta = local.getSetting('Enable-Meta')
        name2 = url.split('@')[1]
        url = url.split('@')[0]
        iconimage = ''
        if EnableMeta == 'true':
                infoLabels = silent.GRABMETA(name2,year)
        try: img = infoLabels['cover_url']
        except: img = iconimage
        match=re.compile('type="button" onclick="location.href=\'(.+?)\'"  value="Click Here to Play"').findall(net.http_GET(url).content)
        for url in match:
                nono = ['http://www.movie25.so/watch/']
                if url not in nono:
                        STREAM(name,url+'@'+name2,img)

#Pass url to urlresolver
def STREAM(name,url,img):
        download_enabled = local.getSetting('movies25-download')
        name2 = url.split('@')[1]
        url2 = url.split('@')[0]
        print url2
        try:
                req = urllib2.Request(url2)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
                addLink(name2,streamlink,img)
        except:
                silent.Notify('small','Sorry Link Removed:', 'Please try another one.',9000)
                

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

def addLink(name,url,iconimage):
        download_enabled = local.getSetting('movies25-download')
        print url
        ok=True
        try: addon.resolve_url(streamlink)
        except: pass
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('Video', infoLabels={ "Title": name } )
        ###Download Context Menu
        contextMenuItems = []
        if download_enabled == 'true':
                contextMenuItems = []
                contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=9&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
                liz.addContextMenuItems(contextMenuItems, replaceItems=True)
                ########################
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok

def addDir(name,url,mode,iconimage,types,year):
        EnableFanArt = local.getSetting('Enable-Fanart')
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = silent.GRABMETA(name,year)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        ###Add to Library and Favorites Context Menu
        contextMenuItems = []
        if mode == 2:
                contextMenuItems = []
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
                
                contextMenuItems.append(('Add to Library', 'XBMC.RunPlugin(%s?mode=10&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
        
                contextMenuItems.append(('Add to Favorites', 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))

                contextMenuItems.append(('Add to Kid Movies', 'XBMC.RunPlugin(%s?mode=47&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ##############################
        ##############################
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        if mode == 20000:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addFAVDir(name,url,year):
        EnableFanArt = local.getSetting('Enable-Fanart')
        mode = 2
        types = 'Movie'
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = silent.GRABMETA(name,year)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        ###Add to Library Context Menu
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        contextMenuItems.append(('Remove from Favorites', 'XBMC.RunPlugin(%s?mode=15&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))
        
        contextMenuItems.append(('Remove from Kids Movies', 'XBMC.RunPlugin(%s?mode=48&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ##############################
        if mode == 20000:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

    
params=get_params()
url=None
name=None
mode=None
year=None
types=None

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
try:
        year=urllib.unquote_plus(params["year"])
except:
        pass
try:
        types=urllib.unquote_plus(params["types"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        
elif mode==1:
        print ""+url
        INDEX(url)

elif mode==2:
        print ""+url
        VIDEOLINKS(name,url,year)

elif mode==3:
        print ""+url
        VIDEOLINKS2(name,url,year)

elif mode==4:
        print ""+url
        STREAM(name,url)

elif mode==5:
        print ""+url
        AZ(url)

elif mode==6:
        print ""+url
        SEARCH(url)

elif mode==7:
        print ""+url
        GETMYFAVS()

elif mode==8:
        print ""+url
        GENRES(url)

elif mode==9:
        print ""+url
        silent.DOWNLOAD(name,url)

elif mode==10:
        print ""+url
        silent.AddToLibrary(name,url)

elif mode==11:
        print ""+url
        silent.LIBRARYPLAY(name,url)

elif mode==12:
        print ""+url
        YEARFIND(url)

elif mode==13:
        print ""+url
        YEAR()

elif mode==14:
        print ""+url
        silent.addFavorite(name,url,year)

elif mode==15:
        print ""+url
        silent.removeFavorite(name,url,year)

elif mode==16:
        print ""+url
        MOVIES()

elif mode==17:
        print ""+url
        TV()

elif mode==18:
        print ""+url
        SETTINGS()

elif mode==21:
        POPULAR()

elif mode==22:
        print ""+url
        INDEXTV(url)

elif mode==23:
        print ""+url
        VIDEOLINKSTV(url)

elif mode==24:
        print ""+url
        VIDEOLINKS2TV(name,url)

elif mode==25:
        print ""+url
        STREAMTV(name,url)

elif mode==26:
        print ""+url
        INDEX2(url)

elif mode==27:
        print ""+url
        INDEX3(url)

elif mode==28:
        print ""+url
        INDEX4(url)

elif mode==29:
        print ""+url
        INDEX5(url)

elif mode==30:
        print ""+url
        INDEX6(url)

elif mode==31:
        print ""+url
        SEASONS(name,url)

elif mode==32:
        print ""+url
        EPISODES(name,url)

elif mode==33:
        print ""+url
        AZTV(url)

elif mode==34:
        print ""+url
        LIST(url)

elif mode==35:
        print ""+url
        GENRESTV(url)

elif mode==36:
        print ""+url
        NEWLINKS(url)

elif mode==37:
        print ""+url
        SEARCHTV(url)

elif mode==38:
        print ""+url
        SCHEDULE(url)

elif mode==39:
        print ""+url
        GETMYFAVSTV()

elif mode==40:
        print ""+url
        silent.addFavoriteTV(name,url,types)

elif mode==41:
        print ""+url
        silent.removeFavoriteTV(name,url,types)

elif mode==42:	addon.addon.openSettings()

elif mode==43:
        ResolverSettings()

elif mode==44:
        KIDMOVIES()

elif mode==45:
        KIDTV()

elif mode==46:
        PARENTS()

elif mode==47:
        print ""+url
        silent.addFavoriteKIDMOVIE(name,url,year)

elif mode==48:
        print ""+url
        silent.removeFavoriteKIDMOVIE(name,url,year)

elif mode==49:
        print ""+url
        silent.addFavoriteKIDTV(name,url,types)

elif mode==50:
        print ""+url
        silent.removeFavoriteKIDTV(name,url,types)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
