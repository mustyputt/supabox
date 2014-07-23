'''
    Copyright (C) Mikey1234

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,time
import json
import datetime
import time

from t0mm0.common.net import Net

net=Net()

PLUGIN='plugin.audio.xbmchubmusic'
ADDON = xbmcaddon.Addon(id=PLUGIN)
icon = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.xbmchubmusic', 'icon.png'))
icon2='http://xbmc-hub-repo.googlecode.com/svn/addons/plugin.audio.xbmchubmusic/icon.png'
allmusic='http://www.allmusic.com'
base='http://dl.dropbox.com/u/129714017/hubmaintenance/'
packages = 'special://home/addons/packages'
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.xbmchubmusic', 'fanart.jpg'))
if ADDON.getSetting('fanart')=='true':
    fanart2 = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.xbmchubmusic', 'fanart.jpg'))
else:
    fanart2 = 'None'
musicdownloads=ADDON.getSetting('download_path')
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))
favorites = os.path.join(datapath, 'favorites')
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
    
VERSION = "3.0.2"
PATH = "XBMC_MUSIC"            

datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_jar = os.path.join(datapath, 'musicru.lwp')

    
def CATEGORIES():
        addDir('Artist Search','url',1,icon,'','','')
        addDir('Album Search','url',2,icon,'','','')
        addDir('Song Search','url',3,icon,'','','')
        if os.path.exists(favorites)==True:
            addDir('Favorites','url',7,icon,'','','')
        addDir('UK Charts','http://www.officialcharts.com/albums-chart/',17,icon,'','','')
        addDir('BillBoard Album Charts','http://www1.billboard.com/#/charts',8,icon,'','','')
        addDir('What Mood Are You In','http://www.allmusic.com/moods',11,icon,'','','')
        addDir('Genres','http://www.allmusic.com/genres',13,icon,'','','')
        addDir('Themes','http://www.allmusic.com/themes',14,icon,'','','')
        addDir('Need Help??','url',2000,base+'images/help.jpg',base+'images/fanart/expert.jpg','','')
        setView('movies', 'default') 
        
def UK_CHARTS(name,url):
        addDir('UK Top 40 Singles','http://www.bigtop40.com/chart/',15,'http://xbmc-hub-repo.googlecode.com/svn/addons/plugin.audio.xbmchubmusic/icon.png','','','')
        addDir("Number Ones",'url',19,'http://xbmc-hub-repo.googlecode.com/svn/addons/plugin.audio.xbmchubmusic/icon.png','','','')
        link=OPEN_URL(url)
        link=link.split('singles-chart/">Singles Chart Top 100')[1]
        link=link.split('@OfficialCharts')[0]
        match = re.compile('href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:
            iconimage=icon
            addDir(name,url,16,iconimage,'','','')    
        setView('movies', 'default') 
        
def BILLBOARD_MAIN_LIST(url):
        addDir('BillBoard 200','http://www1.billboard.com/charts/billboard-200',9,icon,'','','')
        addDir('Country Albums','http://www1.billboard.com/charts/country-albums',9,icon,'','','')
        addDir('HeatSeeker Albums','http://www1.billboard.com/charts/heatseekers-albums',9,icon,'','','')
        addDir('Independent Albums','http://www1.billboard.com/charts/independent-albums',9,icon,'','','')
        addDir('Catalogue Albums','http://www1.billboard.com/charts/catalog-albums',9,icon,'','','')
        addDir('Folk Albums','http://www1.billboard.com/charts/folk-albums',9,icon,'','','')
        addDir('Digital Albums','http://www1.billboard.com/charts/digital-albums',9,icon,'','','')
        setView('movies', 'default') 
        
def BILLBOARD_ALBUM_LISTS(name,url):
        link=OPEN_URL(url)
        match = re.compile('"title" : "(.+?)"\r\n.+?"artist" : "(.+?)"\r\n.+?image" : "(.+?)"\r\n.+?"entityId" : ".+?"\r\n.+?"entityUrl" : "(.+?)"').findall(link)
        for name, artist, iconimage, url in match:
            artist=artist.replace('&','And')
            url='http://www1.billboard.com'+url+'#'+url
            if re.search('.gif',iconimage):
                iconimage=icon
            addDir(name,url,10,iconimage,'',artist,name)    
        setView('movies', 'album') 
        
def BILLBOARD_SONG_LISTS(url,iconimage,artist,album):
        link=OPEN_URL(url)
        match = re.compile('<span class="song-title">(.+?)</span>').findall(link)
        foricon = re.compile('<link rel="image_src" href="(.+?)" />').findall(link)
        iconimage=foricon[0]
        for name in match:
            addDir(name,url,6,iconimage,'',artist,album)    
        setView('movies', 'default') 
        
def DownloaderClass(url,dest,name,dp,start,range): 
    dp.update(int(start), "Downloading & Copying File",'',name)   
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,dp,start,range,url))
 
def _pbhook(numblocks, blocksize, filesize, dp, start, range, url=None):
    try:
        percent = min(start+((numblocks*blocksize*range)/filesize), start+range)
        print 'Downloaded '+str(percent)+'%'
        dp.update(int(percent))
    except:
        percent = 100
        dp.update(int(percent))
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED" # need to get this part working        
        raise Exception("Canceled")
        
def select_year():
    dialog = xbmcgui.Dialog()
    start = 1960
    end   = datetime.datetime.today().year
    year  = []
    for yr in range(start, end+1):
        year.append(str(yr))
    return year[xbmcgui.Dialog().select('Please Select A Year !', year)]
    
    	
def which_year(name):
    year=select_year()
    url='http://www.officialcharts.com/all-the-number-ones-singles-list/_/'+str(year)+'/'
    link=OPEN_URL(url).replace('\n','')
    match = re.compile('<td class="artist">(.+?)</td>.+?td class="title">(.+?)</td>').findall(link)
    iconimage=icon2
    for artist,name in match:      
        artist=str(artist).replace('&amp;','&').replace('&#039;','')
        name=str(name).replace('&amp;','&').replace('&#039;','')
        addDir(name,'Number Ones',6,iconimage,'',artist,str(year))    
    setView('movies', 'default') 
        
def which_year_playlist(name,clear):
    dialog = xbmcgui.Dialog()
    dp = xbmcgui.DialogProgress()
    dp.create("XunityTalk Music",'Creating Your Playlist')
    dp.update(0)
    year=select_year()
    pl = get_XBMCPlaylist(clear)
    url='http://www.officialcharts.com/all-the-number-ones-singles-list/_/'+str(year)+'/'
    link=OPEN_URL(url).replace('\n','')
    try:
        if dialog.yesno("XunityTalk Music",'Do You Want To Use Musicmp3.ru ?','','Go For It'):
            graburl=True
        else:
            graburl=False
        match = re.compile('<td class="artist">(.+?)</td>.+?td class="title">(.+?)</td>').findall(link)
        iconimage=icon2
        playlist=[]
        nItem=len(match)
        for artist,name in match:   
            artist=urllib.unquote(artist).replace('&amp;','&').replace('&#039;','').replace('/','')
            name=urllib.unquote(name).replace('&amp;','&').replace('&#039;','').replace('/','')
            liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            liz.setInfo('music', {'Title':name, 'Artist':artist, 'Album':"Number Ones "+str(year)})
	    liz.setProperty("IsPlayable","true")               
            liz.setProperty('mimetype', 'audio/mpeg')                
            if graburl == True:
                playlist.append((get_musicru(artist+'%20'+name),liz))
            else:
                playlist.append((for_download_or_playlist(name,artist),liz))

            progress = len(playlist) / float(nItem) * 100               
            dp.update(int(progress), 'Adding to Your Playlist',name)
            if dp.iscanceled():
                return

        print 'THIS IS PLAYLIST====   '+str(playlist)
    
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob.replace(' ','%20'),liz)
            except:
                pass
        if clear or (not xbmc.Player().isPlayingAudio()):
            xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("XunityTalk Music", "Sorry Cant Find Songs From Album", "Why Not Try A Different Album")
        
def which_year_download(name):
    iconimage=icon2
    if musicdownloads == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XunityTalk Music", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set")
        ADDON.openSettings()
    year=select_year()
    url='http://www.officialcharts.com/all-the-number-ones-singles-list/_/'+str(year)+'/'
    link=OPEN_URL(url).replace('\n','')
    match = re.compile('<td class="artist">(.+?)</td>.+?td class="title">(.+?)</td>').findall(link)
    path = xbmc.translatePath(os.path.join(musicdownloads+'Number Ones',str(year)))
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    dp = xbmcgui.DialogProgress()
    dp.create("XunityTalk Music")

    nItems = len(match) + 1 #+1 for cover
    range  = float(100) / nItems
    start  = 0

    DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
    start += range

    for artist, name in match:
        artist=urllib.unquote(artist).replace('&amp;','&').replace('&#039;','').replace('/','')
        name=urllib.unquote(name).replace('&amp;','&').replace('&#039;','').replace('/','')
        url=for_download_or_playlist(name,artist)
        mp3=os.path.join(path, str(name)+'.mp3')
        try:
            DownloaderClass(url,mp3,name, dp, start, range)
        except Exception as e:
            if str(e) == "Canceled":
                dp.close()
                return
            pass
        start += range
        
        
def top40(name,url):
        link=OPEN_URL(url)
        match = re.compile('<img src="(.+?)".+?\n.+?<span class="track_title".+?>(.+?)</span>.+?\n.+?class="artist">.+?>(.+?)</a></span>').findall(link)
        for iconimage, name, artist in match:
            artist=str(artist).replace('&amp;','&')
            name=str(name).replace('&amp;','&')
            iconimage=str(iconimage).replace('170x170-75.jpg','600x600-75.jpg')
            addDir(name,url,6,iconimage,'',artist,'UK TOP 40')    
        setView('movies', 'default') 
        
def ukalbumchart(name,url):
        link=OPEN_URL(url).replace('\n','')
        link=link.split('The Official Charts logo')[1]
        match = re.compile('<img src="(.+?)".+?<h3>(.+?)</h3>.+?<h4>(.+?)</h4>.+?<a target="_blank" href="http://clk.tradedoubler.com.+?&url=(.+?)"').findall(link)
        uniques=[]
        for iconimage, name, artist,url in match:
            if name not in uniques:
                uniques.append(name) 
                artist=urllib.unquote(artist).replace('&amp;','&').replace('&#039;','')
                name=urllib.unquote(name).replace('&amp;','&').replace('&#039;','')
                iconimage=str(iconimage).replace('60x60-50.jpg','600x600-75.jpg').replace('_50.jpg','_350.jpg')  
                url=urllib.unquote(url)
                addDir(name,url,18,iconimage,'',artist,name)    
        setView('movies', 'album') 
        
        
def UK_CHARTS_SONG_LIST(url,iconimage,artist,album): 
        link=OPEN_URL(url)
        link=link.split('"tracklist-footer"')[0]
        match = re.compile('preview-title="(.+?)"').findall(link)
        for name in match:
            name=str(name).replace('&amp;','&')    
            addDir(name,url,6,iconimage,'',artist,album)    
        setView('movies', 'default') 
        
        

                

def artist_search_auto(artist):
    do_artist_search(artist.replace(' ', '+'))

def artist_search(url):
    do_artist_search(SEARCH())
                
def do_artist_search(search_entered):
    name=str(search_entered).replace('+','')
    fanart=get_fanart(name)    
    link = OPEN_URL('http://www.allmusic.com/search/artists/'+search_entered)
    
    match=re.compile('<div class="photo">\n.+?a href="(.+?)" data-tooltip=".+?">\n.+?img src="(.+?).jpg.+?" height=".+?" alt="(.+?)">').findall(link)
    for url,iconimage,artist in match:
        url=allmusic+url+'/discography'
        iconimage=iconimage.replace('JPG_170','JPG_400')+'.jpg'
        addDir(artist,url,4,iconimage,fanart,artist,'')
        setView('movies', 'default') 
        
        
def artist_album_index(name,url,iconimage,fanart,artist):
    link = OPEN_URL(url)
    match=re.compile('<td class="cover">\n.+?a href="(.+?)"\n.+?title="(.+?)"\n.+?data-tooltip=".+?">\n.+?div class=".+?" style=".+?" ><img class=".+?" src=".+?" data-original="(.+?).jpg.+?"').findall(link)
    uniques=[]
    for url,name,iconimage in match:
        if name not in uniques:
            uniques.append(name)
            url=allmusic+'/album'+url
            iconimage=iconimage.replace('JPG_250','JPG_400').replace('JPG_75','JPG_400')+'.jpg'
            name=str(name).replace("'",'').replace(',','') .replace(":",'').replace('&amp;','And').replace('.','')
            addDir(name,url,5,iconimage,fanart,artist,name)
            setView('movies', 'album') 
            
def album_index(name,url,iconimage,fanart,artist,album):
    link = OPEN_URL(url)
    artist=re.compile('data-artist="(.+?)"').findall(link)
    match=re.compile('<a href="http://www.allmusic.com/song/.+?">(.+?)</a>').findall(link)
    for name in match:
        addDir(name,url,6,iconimage,fanart,artist[0],album)
        setView('movies', 'default') 
        
        
def moods(url,iconimage):
    link=OPEN_URL(url)
    link=link.split('<div class="mood-container">')[1]
    match=re.compile('<a href="http://www.allmusic.com/mood(.+?)">(.+?)</a>').findall(link)
    for url ,name in match:
        url='http://www.allmusic.com/mood'+url
        addDir(name,url,12,iconimage,'','','')
        setView('movies', 'default') 
        
        
def themes(url,iconimage):
    link=OPEN_URL(url)
    match=re.compile('<a href="http://www.allmusic.com/theme(.+?)">(.+?)</a>').findall(link)
    for url ,name in match:
        url='http://www.allmusic.com/theme'+url
        addDir(name,url,12,iconimage,'','','')
        setView('movies', 'default') 
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            
def moods_extended_list(url,iconimage):
    link = OPEN_URL(url)
    link = str(link).replace('\n','')
    match=re.compile('<a href="/album/(.+?)-mw(.+?)".+?img src="(.+?).jpg.+?"').findall(link)
    for name,url,iconimage in match:
        url=allmusic+'/album/'+name+'-mw'+url
        name=urllib.unquote(name).upper().replace('-',' ')
        iconimage=iconimage.replace('JPG_170','JPG_400').replace('JPG_250','JPG_400').replace('JPG_75','JPG_400')+'.jpg'
        addDir(name,url,5,iconimage,'','',name)
        setView('movies', 'album')
        
def genre(url,iconimage):
    link=OPEN_URL(url)
    match=re.compile('<a href="/genre(.+?)">\n.+?span>(.+?)</span>').findall(link)
    for url, name in match:
        url=allmusic+'/genre'+url
        addDir(name,url,12,iconimage,'','','')
        setView('movies', 'default') 
       
        
def album_search(url):
    search_entered =SEARCH()
    name=str(search_entered).replace('+','')
    link = OPEN_URL('http://www.allmusic.com/search/albums/'+search_entered).replace('\n','')
    match=re.compile('<div class="cover">.+?href="(.+?)" title="(.+?)".+?<img src="(.+?).jpg.+?".+?<div class="artist">.+?a href=".+?">(.+?)</a>').findall(link)
    for url,name,iconimage,artist in match:
        url=allmusic+'/album'+url
        iconimage=iconimage.replace('JPG_170','JPG_250')+'.jpg'
        addDir(name,url,5,iconimage,'',artist,artist)
        setView('movies', 'album') 

def song_search_auto(name):
    do_song_search(name.replace(' ', '+'),iconimage)

def song_search(url,iconimage):
    do_song_search(SEARCH(),iconimage)
                                
def do_song_search(search_entered,iconimage):
    name_Download=str(search_entered).replace('+',' ')
    r= 'http://musicmp3.ru/search.html?text=%s&all=songs' % (str(search_entered).replace(' ','%20'))
    get_cookie()
    try:
	    linked=APPLE_URL(r)
	    matched=re.compile('class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" />.+?<a class="song__link" href=".+?">(.+?)</a>.+?lass="song__artist song__artist.+?="song__link" href=".+?">(.+?)</a>.+?"song__album song__album.+?song__link" href=".+?">(.+?)</a>',re.DOTALL).findall(linked)
	    for id,name,artist,where in matched:
	      
	        url='http://listen.musicmp3.ru/2f99f4bf4ce7b171/'+id
	        name=name.replace('&amp;','')
	        name='[COLOR cyan]MUSICMP3.RU[/COLOR]-%s (%s-%s)'%(name,artist,where) 
	        addLink(name,url,icon2,'','','','false')
    except:pass
    try:
	    url='http://mp3skull.uno/mp3/'+str(search_entered).replace('+','_')
	    link = OPEN_URL(url).replace('\n','')
	    match=re.compile('<div class=song-col-info>.+?data-src="(.+?)".+?title=".+?">(.+?)</a>.+?<span class=size>(.+?)</span>').findall(link)
	    print 'MP3 Skull========================================='+str(match)
            for url,name,bitrate in match:
                name=name.strip()
	        name='[COLOR green]MP3 SKULL[/COLOR]-%s-%s'%(bitrate,name) 
	        addLink(name,url,icon2,search_entered.replace('+',' '),'','','true')
    except:pass
    try:
	    url='http://mp3chief.co/search?q='+str(search_entered)+'&duration=1&size=1&bitrate=4'
	    link = OPEN_URL(url)
	    match=re.compile('MB<br>									(.+?) kbps<br>.+?<h3>(.+?)</h3>.+?class="download"><a href="(.+?)"',re.DOTALL).findall(link)
	    print 'MP3 CHIEF========================================='+str(match)
	    for bitrate,name,url in match:
	        name='[COLOR yellow]MP3 CHIEF[/COLOR]-%sKbps-%s'%(bitrate,name) 
	        addLink(name,url,icon2,name_Download,'','','true')   
    except:pass
         
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def ENTER_ALBUM_OR_ARTIST(name):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter '+str(name)+' Name')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText()
            if search_entered == None:
                return False          
        return search_entered    
    
def SEARCH():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Music...XunityTalk')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
            if search_entered == None:
                return False          
        return search_entered    
    
        
def for_download_or_playlist(name,artist):
    try:
        hello = None
        name=str(name).replace(' ','+').replace("'",'+').replace(',','').replace('(','').replace(')','').replace('?','')
        artist=str(artist).replace(' ','+').replace("'",'+').replace(',','').replace('(','').replace(')','').replace('?','')
               
               
               
        url='http://mp3skull.uno/mp3/'+str(artist).replace('+','_')+'_'+str(name).replace('+','_')
        link = OPEN_URL(url).replace('\n','')
        match=re.compile('<div class=song-col-info>.+?data-src="(.+?)"').findall(link)
        try:
            url=match[0]
            hello='MP3SKULL 1 ========================================='+str(url)
        except:
            url=''
            
        if url=='':
            url='http://mp3chief.co/search?q='+str(name)+'&duration=1&size=1&bitrate=4'
            link = OPEN_URL(url)
            match=re.compile('<h3>.+?</h3>.+?class="download"><a href="(.+?)"',re.DOTALL).findall(link)
            try:
                url=match[0]
                hello=  'MP3 CHIEF========================================='+str(url)
            except:
                url==''
            
                
        if not hello:
            print "NOT FOUND========================================="
            return None
        print hello   
        return url
    except:
        pass
        
        
def album_links(name,artist):
    r='[COLOR white]Looking For[/COLOR] - [COLOR green]%s[/COLOR]'%name
    return_name=[]
    return_url=[]
    return_name.append('[COLOR orange]Cancel[/COLOR]')  
    return_url.append('Cancel')  
    name_url=str(name).replace(' ','+').replace("'",'+').replace(',','').replace('(','').replace(')','').replace('?','')
    artist_url=str(artist).replace(' ','+').replace("'",'+').replace(',','').replace('(','').replace(')','').replace('?','')
    url='http://mp3skull.uno/mp3/'+str(name_url).replace('+','_')
    link = OPEN_URL(url).replace('\n','')
    match=re.compile('<div class=song-col-info>.+?data-src="(.+?)".+?title=".+?">(.+?)</a>.+?<span class=size>(.+?)</span>').findall(link)
    print 'MP3 Skull========================================='+str(match)
    for url,name,bitrate in match:
        name=name.strip()
        name='[COLOR green]MP3 SKULL[/COLOR]-%s-%s'%(bitrate,name) 
        return_name.append(name)  
        return_url.append(url)   
    url='http://mp3chief.co/search?q='+str(name_url)+'&duration=1&size=1&bitrate=4'
    link = OPEN_URL(url)
    match=re.compile('MB<br>									(.+?) kbps<br>.+?<h3>(.+?)</h3>.+?class="download"><a href="(.+?)"',re.DOTALL).findall(link)
    print 'MP3 CHIEF========================================='+str(match)
    for bitrate,name,url in match:
        name='[COLOR yellow]MP3 CHIEF[/COLOR]-%sKbps-%s'%(bitrate,name) 
        return_name.append(name)  
        return_url.append(url) 
    r= 'http://musicmp3.ru/search.html?text=%s_%s&all=songs' % (artist_url.replace('+','%20'),name_url.replace('+','%20'))
    get_cookie()
    linked=APPLE_URL(r.replace('_','%20'))
    matched=re.compile('class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" />.+?<a class="song__link" href=".+?">(.+?)</a>.+?lass="song__artist song__artist.+?="song__link" href=".+?">(.+?)</a>.+?"song__album song__album.+?song__link" href=".+?">(.+?)</a>',re.DOTALL).findall(linked)
    for id,name,artist,where in matched:
        url='http://listen.musicmp3.ru/2f99f4bf4ce7b171/'+id
        name=name.replace('&amp;','')
        name='[COLOR cyan]MUSICMP3.RU[/COLOR]-%s (%s-%s)'%(name,artist,where) 
        return_name.append(name)  
        return_url.append(url) 
        
    dialog=xbmcgui.Dialog()
    
    return return_url[xbmcgui.Dialog().select(r, return_name)]
    
def song_links(name,url,iconimage,fanart,artist,album):
    if ADDON.getSetting('oneclick')=='true':
        if url=='Number Ones':
            _artist = 'Number Ones'
        else:
            _artist = artist
            
    name_Download=str(name)
    name_url=str(name).replace(' ','+').replace("'",'+').replace(',','').replace('(','').replace(')','').replace('?','')
    artist_url=str(artist).replace(' ','+').replace("'",'+').replace(',','').replace('(','').replace(')','').replace('?','')
    r= 'http://musicmp3.ru/search.html?text=%s_%s&all=songs' % (artist_url.replace('+','%20'),name_url.replace('+','%20'))
    get_cookie()
    linked=APPLE_URL(r.replace('_','%20'))
    matched=re.compile('class="player__play_btn js_play_btn" href="#" rel="(.+?)" title="Play track" />.+?<a class="song__link" href=".+?">(.+?)</a>.+?lass="song__artist song__artist.+?="song__link" href=".+?">(.+?)</a>.+?"song__album song__album.+?song__link" href=".+?">(.+?)</a>',re.DOTALL).findall(linked)
    for id,name,artist,where in matched:
      
        url='http://listen.musicmp3.ru/2f99f4bf4ce7b171/'+id
        name=name.replace('&amp;','')
        name='[COLOR cyan]MUSICMP3.RU[/COLOR]-%s (%s-%s)'%(name,artist,where) 
        addLink(name,url,icon2,name_url.replace('+',' '),'','','true')
    print 'MUSICMP3========================================='+str(matched)
    url='http://mp3skull.uno/mp3/'+str(artist_url).replace('+','_')+'_'+str(name_url).replace('+','_')
    link = OPEN_URL(url)
    match=re.compile('<div class=song-col-info>.+?data-src="(.+?)".+?title=".+?">(.+?)</a>.+?<span class=size>(.+?)</span>',re.DOTALL).findall(link)
    print 'MP3 Skull========================================='+str(match)
    for url,name,bitrate in match:
        name=name.strip()
        name='[COLOR green]MP3 SKULL[/COLOR]-%s-%s'%(bitrate,name) 
        addLink(name,url,icon2,name_url.replace('+',' '),'','','true')   
    url='http://mp3chief.co/search?q='+str(artist_url)+'+'+str(name_url)+'&duration=1&size=1&bitrate=4'
    link = OPEN_URL(url)
    match=re.compile('MB<br>									(.+?) kbps<br>.+?<h3>(.+?)</h3>.+?class="download"><a href="(.+?)"',re.DOTALL).findall(link)
    print 'MP3 CHIEF========================================='+str(match)
    for bitrate,name,url in match:
        name='[COLOR yellow]MP3 CHIEF[/COLOR]-%sKbps-%s'%(bitrate,name) 
        addLink(name,url,icon2,name_Download,'','','true')   
           
         
        
def download_album_song(name,url,iconimage,artist,album):
    iconimage=str(iconimage)
    if musicdownloads == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XunityTalk Music", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set")
        ADDON.openSettings()
    if re.search('allmusic',url,re.IGNORECASE):
        link = OPEN_URL(url)
        match_artist=re.compile('data-artist="(.+?)"').findall(link)
        artist=match_artist[0]
        match=re.compile('<a href="http://www.allmusic.com/song/.+?">(.+?)</a>').findall(link)
        album=str(album).replace("'",'').replace(",",'').replace(":",'').replace(">",'').replace("<",'').replace("|",'').replace("\\",'').replace("/",'')
        artist=str(artist).replace("'",'').replace(",",'').replace(":",'').replace(">",'').replace("<",'').replace("|",'').replace("\\",'').replace("/",'')
    else:
        link=OPEN_URL(url)
        match=re.compile('<span class="song-title">(.+?)</span>').findall(link)
        foricon = re.compile('<link rel="image_src" href="(.+?)" />').findall(link)
        iconimage=foricon[0]
    path = xbmc.translatePath(os.path.join(musicdownloads+artist,album))
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    files = []
    
    for name in match:
        name=str(name).replace("'",'').replace(".",'').replace(",",'')
        url=album_links(name,artist)
        if 'Cancel' in url:
            print 'Cancel Choose Download'
        else:
            mp3=os.path.join(path, str(name)+'.mp3')
            try:
                #DownloaderClass(url,mp3,name, dp, start, range)            
                files.append((url, mp3))
            except Exception as e:
                if str(e) == "Canceled":
                    dp.close()
                    return
            #start += range

    if len(files) == 0:
        return

    dp = xbmcgui.DialogProgress()
    dp.create("XunityTalk Music")

    nItems = len(match) + 1 #+1 for cover
    range  = float(100) / nItems
    start  = 0

    DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
    start += range

    for item in files:
        try:
            DownloaderClass(item[0],item[1],name, dp, start, range)
        except Exception as e:
	    if str(e) == "Canceled":
	        dp.close()
	        return
        start += range

    
def download_album(name,url,iconimage,artist,album):
    iconimage=str(iconimage)
    if musicdownloads == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XunityTalk Music", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set")
        ADDON.openSettings()
    if re.search('allmusic',url,re.IGNORECASE):
        link = OPEN_URL(url)
        match_artist=re.compile('data-artist="(.+?)"').findall(link)
        artist=match_artist[0]
        match_album=re.compile('data-title="(.+?)"').findall(link)
        album=match_album[0]
        match=re.compile('<a href="http://www.allmusic.com/song/.+?">(.+?)</a>').findall(link)
        album=str(album).replace("'",'').replace(",",'').replace(":",'').replace(">",'').replace("<",'').replace("|",'').replace("\\",'').replace("/",'')
        artist=str(artist).replace("'",'').replace(",",'').replace(":",'').replace(">",'').replace("<",'').replace("|",'').replace("\\",'').replace("/",'')
    else:
        link=OPEN_URL(url)
        match=re.compile('<span class="song-title">(.+?)</span>').findall(link)
        foricon = re.compile('<link rel="image_src" href="(.+?)" />').findall(link)
        iconimage=foricon[0]
    path = xbmc.translatePath(os.path.join(musicdownloads+artist,album))
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    nItems = len(match) + 1 #+1 for cover
    range  = float(100) / nItems
    start  = 0
    dp = xbmcgui.DialogProgress()
    dp.create("XunityTalk Music")
    
    for name in match:
        name=str(name).replace("'",'').replace(".",'').replace(",",'')
        url=for_download_or_playlist(name,artist)
        DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
        start += range
        mp3=os.path.join(path, str(name)+'.mp3')
        
        
        try:
            DownloaderClass(url,mp3,name, dp, start, range)            
        except Exception as e:
            if str(e) == "Canceled":
                dp.close()
                return
            pass
        start += range
            
def download_uk_album(name,url,iconimage,artist,album):
    iconimage=str(iconimage)
    if musicdownloads == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("XunityTalk Music", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set")
        ADDON.openSettings()
    link=OPEN_URL(url)
    if re.search('apple.com',url,re.IGNORECASE):
        link=link.split('table class="tracklist-footer"')[0]
        match=re.compile('preview-title="(.+?)"').findall(link)
    else:
        match=re.compile('&#39;(.+?)&#39;').findall(link)
    path = xbmc.translatePath(os.path.join(musicdownloads+artist,album))
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    dp = xbmcgui.DialogProgress()
    dp.create("XunityTalk Music")

    nItems = len(match) + 1 #+1 for cover
    range  = float(100) / nItems
    start  = 0

    DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
    start += range
    album=str(album).replace("'",'').replace(",",'').replace(":",'').replace(">",'').replace("<",'').replace("|",'').replace("\\",'').replace("/",'')
    artist=str(artist).replace("'",'').replace(",",'').replace(":",'').replace(">",'').replace("<",'').replace("|",'').replace("\\",'').replace("/",'')
    for name in match:
        name=str(name).replace("'",'').replace(".",'').replace(",",'').replace('&amp;','').replace("'",'').replace(",",'').replace(":",'').replace(">",'').replace("<",'').replace("|",'').replace("\\",'').replace("/",'')
        url=for_download_or_playlist(name,artist)
        mp3=os.path.join(path, str(name)+'.mp3')
        try:
            DownloaderClass(url,mp3,name, dp, start, range)
        except Exception as e:
            if str(e) == "Canceled":
                dp.close()
                return
            pass
        start += range
            
def get_XBMCPlaylist(clear):
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    #if not xbmc.Player().isPlayingAudio():
    if clear:
        pl.clear()
    return pl

    dialog = xbmcgui.Dialog()
    if dialog.yesno("XunityTalk Music", 'Queue album or play now?', '', '', 'Play Now','Queue') == 0:
        pl.clear()
    return pl

def APPLE_URL(url):
    header_dict = {}#audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5
    header_dict['Accept'] = 'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'
    header_dict['User-Agent'] = '	AppleWebKit/<WebKit Rev>'
    header_dict['Host'] = 'musicmp3.ru'
    header_dict['Referer'] = 'http://musicmp3.ru/'
    header_dict['Connection'] = 'keep-alive'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    return link
    
        
def get_cookie():
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    header_dict['Connection'] = 'keep-alive'
    net.set_cookies(cookie_jar)
    link = net.http_GET('http://musicmp3.ru/', headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)    
    
    
                 
def get_playlist(name,url,iconimage,artist,album,clear):
    iconimage=str(iconimage)
    dp = xbmcgui.DialogProgress()
    dp.create("XunityTalk Music",'Creating Your Playlist')
    dp.update(0)
    pl = get_XBMCPlaylist(clear)
    link=OPEN_URL(url)
    try:
	    if re.search('allmusic',url,re.IGNORECASE):
		    match_artist=re.compile('data-artist="(.+?)"').findall(link)
		    artist=match_artist[0]
		    match=re.compile('<a href="http://www.allmusic.com/song/.+?">(.+?)</a>').findall(link)
	    playlist=[]

            nItem = len(match)           
	    for name in match:                
	        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	        #liz.setInfo( type="Audio", infoLabels={ "Title": name} )
                liz.setInfo('music', {'Title':name, 'Artist':artist, 'Album':album})
	        liz.setProperty("IsPlayable","true")               
	        liz.setProperty('mimetype', 'audio/mpeg')                
	        playlist.append((for_download_or_playlist(name,artist),liz))

                progress = len(playlist) / float(nItem) * 100               
	        dp.update(int(progress), 'Adding to Your Playlist',name)
                if dp.iscanceled():
                    return

	    print 'THIS IS PLAYLIST====   '+str(playlist)
            
	    for blob ,liz in playlist:
	        try:
                    if blob:
	                pl.add(blob.replace(' ','%20'),liz)
	        except:
	            pass
            if clear or (not xbmc.Player().isPlayingAudio()):
	        xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("XunityTalk Music", "Sorry Cant Find Songs From Album", "Why Not Try A Different Album")
    
    
def get_musicru(name):
    r= 'http://musicmp3.ru/search.html?text=%s&all=songs' % (name.replace(' ','%20'))
    get_cookie()
        
    linked=APPLE_URL(r)
    matched=re.compile('class="player__play_btn js_play_btn" href="#" rel="(.+?)"',re.DOTALL).findall(linked)
    try: 
        return 'http://listen.musicmp3.ru/2f99f4bf4ce7b171/'+matched[0]
    except: 
        return None
	        
def get_uk_playlist(name,url,iconimage,artist,album,clear):
    iconimage=str(iconimage)
    dp = xbmcgui.DialogProgress()
    dialog = xbmcgui.Dialog()
    dp.create("XunityTalk Music",'Creating Your Playlist')
    dp.update(0)
    pl = get_XBMCPlaylist(clear)
    link=OPEN_URL(url)
    try:
	    if re.search('apple.com',url,re.IGNORECASE):
	        link=link.split('table class="tracklist-footer"')[0]
	        match=re.compile('preview-title="(.+?)"').findall(link)
	    else:
	        match=re.compile('&#39;(.+?)&#39;').findall(link)
	    if dialog.yesno("XunityTalk Music",'Do You Want To Use Musicmp3.ru ?','','Go For It'):
	        graburl=True
	    else:
	        graburl=False
	        
	    playlist=[]

            nItem = len(match)           
	    for name in match:    
	        name=name.replace('&amp;','')
	        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	        #liz.setInfo( type="Audio", infoLabels={ "Title": name} )
                liz.setInfo('music', {'Title':name, 'Artist':artist, 'Album':album})
	        liz.setProperty("IsPlayable","true")               
	        liz.setProperty('mimetype', 'audio/mpeg') 
	        if graburl == True:
	            playlist.append((get_musicru(name),liz))
	        else:
	            playlist.append((for_download_or_playlist(name,artist),liz))

                progress = len(playlist) / float(nItem) * 100               
	        dp.update(int(progress), 'Adding to Your Playlist',name)
                if dp.iscanceled():
                    return

	    print 'THIS IS PLAYLIST====   '+str(playlist)
            
	    for blob ,liz in playlist:
	        try:
                    if blob:
	                pl.add(blob.replace(' ','%20'),liz)
	        except:
	            pass
            if clear or (not xbmc.Player().isPlayingAudio()):
	        xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("XunityTalk Music", "Sorry Cant Find Songs From Album", "Why Not Try A Different Album")

    
    
        
def download_single_song(name,url,iconimage,fanart,artist,album):
    name=str(fanart).title()
    if artist=="None":
        artist=ENTER_ALBUM_OR_ARTIST("Artists")
    if album=="None":
        album=ENTER_ALBUM_OR_ARTIST("Album")
    if artist=="":
        artist=ENTER_ALBUM_OR_ARTIST("Artists")
    if album=="":
        album=ENTER_ALBUM_OR_ARTIST("Album")
    path = xbmc.translatePath(os.path.join(musicdownloads+artist.title(),album.title()))
    if os.path.exists(path) == False:
        os.makedirs(path)
    jpg=os.path.join(path, 'folder.jpg')

    dp = xbmcgui.DialogProgress()
    dp.create("XunityTalk Music")
    if os.path.exists(jpg) == False:
        nItems = 1 + 1 #+1 for cover
    else:
        nItems = 1
    range  = int(100) / nItems
    start  = 0
    if os.path.exists(jpg) == False:
        try:
            DownloaderClass(iconimage,jpg,'Album Cover', dp, start, range)
            start += range
        except:
            pass
    name=str(name).replace("'",'').replace(".",'').replace(",",'')
    mp3=os.path.join(path, str(name)+'.mp3')
    try:
        DownloaderClass(url,mp3,name, dp, start, range)            
    except Exception as e:
        if str(e) == "Canceled":
            dp.close()
            return
        pass
    start += range
    
    
def getFavorites():
        with open(favorites) as f:
            a = f.read()
        try:
            for i in json.loads(a):
                name = i[0]
                url = i[1]
                iconimage = i[2]
                artist = i[3]
                album = i[4]
                if re.search('allmusic',url,re.IGNORECASE):
                    addDir(name,url,5,iconimage,'',artist,album)
                else:
                        addDir(name,url,10,iconimage,'',artist,album) 
                setView('movies', 'album')
        except:
            pass
            


            
def addFavorite(name,url,iconimage,artist,album):
        favList = []
        if os.path.exists(favorites)==False:
            print 'Making Favorites File'
            favList.append((name,url,iconimage,artist,album))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            print 'Appending Favorites'
            with open(favorites) as f:
                a = f.read()
            try:
                data = json.loads(a)
                data.append((name,url,iconimage,artist,album))
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
            except:
                favList.append((name,url,iconimage,artist,album))
                a = open(favorites, "w")
                a.write(json.dumps(favList))
                a.close()

def rmFavorite(name):
        print 'Remove Favorite'
        with open(favorites) as f:
            a = f.read()
        data = json.loads(a)
        for index in range(len(data)):
            try:
                if data[index][0]==name:
                    del data[index]
                    b = open(favorites, "w")
                    b.write(json.dumps(data))
                    b.close()
            except:
                pass
                    
    
            
            




             
            

def get_fanart(name):
    try:
	    name=str(name).replace(", ","+").replace("(The)","").replace(" ","+")
	    url = 'http://www.htbackdrops.com/v2/thumbnails.php?search=%s&submit=search&album=search&title=checked&caption=checked&keywords=checked&type=AND' %(name)
	    link = OPEN_URL(url)
	    icon = re.compile('<img src="(.+?)" class="image" width=".+?" height=".+?" border="0" alt=".+?" title="Filename=.+?\r\nFilesize=.+?KiB\r\nDimensions=1.+?x.+?0').findall(link)
	    normal = icon[0]
	    fanart = 'http://www.htbackdrops.com/v2/%s' % str(normal).replace('thumb_','')
    except:
	    fanart=fanart2
    return fanart
	
	
            
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
def addDir(name,url,mode,iconimage,fanart,artist,album):
        if fanart=='':
            fanart=fanart2
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&artist="+urllib.quote_plus(artist)+"&album="+urllib.quote_plus(album)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        liz.setProperty("Fanart_Image", fanart)
        menu = []
        play      = 0
        queue     = 0
        download  = 0
        Fave      = False
        try:
            Fave = (len(FAV) > -1)
        except:
            pass
        if (mode == 5) or (mode == 12) or (mode == 10):
            play     = 200
            queue    = 202
            download = 201
            download_choose = 215
        if (mode == 18) or  (mode == 15):
            url=urllib.quote(url)
            play     = 206
            queue    = 207
            download = 208
            download_choose = 215
        if (mode == 19):
            play     = 210
            queue    = 211
            download = 212
            download_choose = 215
        if play > 0:
            menu.append(('Play Album','XBMC.RunPlugin(%s?mode=%d&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], play,     url, name, iconimage, artist, album)))
            menu.append(('Queue Album','XBMC.RunPlugin(%s?mode=%d&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], queue,    url, name, iconimage, artist, album)))
            menu.append(('Download Album','XBMC.RunPlugin(%s?mode=%d&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], download, url, name, iconimage, artist, album)))
            menu.append(('[COLOR yellow]Download Album But Choose[/COLOR]','XBMC.RunPlugin(%s?mode=%d&url=%s&name=%s&iconimage=%s&artist=%s&album=%s)'% (sys.argv[0], download_choose, url, name, iconimage, artist, album)))
            if Fave and (name in FAV):
                menu.append(('Remove Album Favorites','XBMC.Container.Update(%s?name=%s&mode=205&iconimage=None&artist=None&url=None&album=None)'% (sys.argv[0],name)))
            else:
                menu.append(('Add to Album Favorites','XBMC.Container.Update(%s?&mode=204&url=%s&album=%s&iconimage=%s&artist=%s&name=%s)'% (sys.argv[0], url, name, iconimage, artist,album)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        if (mode == 2000):
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)
        
        
def addLink(name,url,iconimage,fanart,artist,album,download): 
        ok=True       
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('music', {'Title':name, 'Artist':artist, 'Album':album})
        liz.setProperty("IsPlayable","true")
        liz.setProperty('mimetype', 'audio/mpeg')
        menu = []
        if download =="true":
            url_for_download=urllib.quote_plus(url)
            menu.append(('Download Song', 'XBMC.RunPlugin(%s?&iconimage=%s&mode=209&url=%s&artist=%s&album=%s&name=%s&fanart=%s)'% (sys.argv[0], iconimage,url_for_download,artist,album,name,fanart)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
        
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
artist=None
album=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        artist=urllib.unquote_plus(params["artist"])
except:
        pass
try:        
        album=urllib.unquote_plus(params["album"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
        
        
        

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
print "Artist: "+str(artist)
print "Album: "+str(album)
print "Fanart: "+str(fanart)

if mode==213 or mode==214:
        url = 'dummy'

#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        artist_search(url)
        
elif mode==2:
        print ""+url
        album_search(url)
        
elif mode==3:
        print ""+url
        song_search(url,iconimage)
        
elif mode==4:
        print ""+url
        artist_album_index(name,url,iconimage,fanart,artist)
        
elif mode==5:
        print ""+url
        album_index(name,url,iconimage,fanart,artist,album)
        
elif mode==6:
        print ""+url
        song_links(name,url,iconimage,fanart,artist,album)
        
elif mode==7:
    print ""
    getFavorites()
        
elif mode==8:
        print ""+url
        BILLBOARD_MAIN_LIST(url)
        
elif mode==9:
        print ""+url
        BILLBOARD_ALBUM_LISTS(name,url) 
        
elif mode==10:
        print ""+url
        BILLBOARD_SONG_LISTS(url,iconimage,artist,album) 
        
elif mode==11:
        print ""+url
        moods(url,iconimage) 
        
elif mode==12:
        print ""+url
        moods_extended_list(url,iconimage) 
        
elif mode==13:
        print ""+url
        genre(url,iconimage) 
        
elif mode==14:
        print ""+url
        themes(url,iconimage) 
        
elif mode==15:
        print ""+url
        top40(name,url)
        
elif mode==16:
        print ""+url
        ukalbumchart(name,url) 
        
elif mode==17:
        print ""+url
        UK_CHARTS(name,url) 
        
elif mode==18:
        print ""+url
        UK_CHARTS_SONG_LIST(url,iconimage,artist,album) 
elif mode==19:
        print ""+url
        which_year(name) 
        
elif mode==200:
        print ""+url
        get_playlist(name,url,iconimage,artist,album,True)

elif mode==202:
        print ""+url
        get_playlist(name,url,iconimage,artist,album,False)
        
elif mode==201:
        print ""+url
        download_album(name,url,iconimage,artist,album)
               
elif mode==204:
    print ""
    addFavorite(name,url,iconimage,artist,album)

elif mode==205:
    print ""
    rmFavorite(name)
    
    
elif mode==206:
        print ""+url
        get_uk_playlist(name,url,iconimage,artist,album,True)
elif mode==207:
        print ""+url
        get_uk_playlist(name,url,iconimage,artist,album,False)
        
elif mode==208:
        print ""+url
        download_uk_album(name,url,iconimage,artist,album)
    
elif mode==209:
        print ""+url
        download_single_song(name,url,iconimage,fanart,artist,album)
        
elif mode==210:
        print ""+url
        which_year_playlist(name,True)
    
elif mode==211:
        print ""+url
        which_year_playlist(name,False)
        
elif mode==212:
        print ""+url
        which_year_download(name)

elif mode==213:
        print ""+url
        song_search_auto(name)

elif mode==214:
        print ""+url
        artist_search_auto(artist)
        
elif mode==215:
        print ""+url
        download_album_song(name,url,iconimage,artist,album)
        
elif mode==2000:
        pop()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
