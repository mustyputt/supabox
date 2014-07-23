import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,xbmcvfs
from metahandler import metahandlers
from addon.common.addon import Addon
from addon.common.net import Net
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer
     

#Silent - The_Silencer 2013 v0.1
#Common routines used accross my add-ons


addon_id = 'plugin.video.moviestwentyfive'
local = xbmcaddon.Addon(id=addon_id)
movie25path = local.getAddonInfo('path')
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()
art = movie25path+'/art'
net = Net()
cache = StorageServer.StorageServer(addon_id)
grab = metahandlers.MetaData(preparezip = False)


############
#Metahandler
############
def GRABMETA(name,year):
        EnableMeta = local.getSetting('Enable-Meta')
        if EnableMeta == 'true':
                meta = grab.get_meta('movie',name,None,None,year,overlay=6)
                infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
        return infoLabels

def GRABMETATV(name,url,types):
          EnableMeta = local.getSetting('Enable-Meta')
          type = types
          if EnableMeta == 'true':
                if 'Movie' in type:
                        meta = grab.get_meta('movie',name,'',None,None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                                'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                                'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'],
                                'overlay' : meta['overlay']}
                elif 'tvshow' in type:
                        meta = grab.get_meta('tvshow',name,'','',None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                                'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                                'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                                'backdrop_url': meta['backdrop_url'],'status': meta['status']}
                elif 'season' in type:
                        title = url.split('@')[1]
                        url = url.split('@')[0]
                        meta = grab.get_meta('tvshow',title,'','',None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                                'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                                'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                                'backdrop_url': meta['backdrop_url'],'status': meta['status']}
                elif 'episode' in type:
                        season = url.split('@')[2]
                        title = url.split('@')[1]
                        url = url.split('@')[0]
                        tv = grab.get_meta('tvshow',title,'','',None,overlay=6)
                        imdb_id = tv['imdb_id']
                        season = season.replace('Season ', '')
                        episode = name.replace('Episode ', '')
                        print title
                        print imdb_id
                        print season
                        print episode
                        meta = grab.get_episode_meta(title,imdb_id,season,episode)
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                                'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                                'director': meta['director'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id']}
                elif 'new' in type:
                        episode = url.split('@')[3]
                        season = url.split('@')[2]
                        title = url.split('@')[1]
                        url = url.split('@')[0]
                        tv = grab.get_meta('tvshow',title,'','',None,overlay=6)
                        imdb_id = tv['imdb_id']
                        season = season.replace('Season ', '')
                        episode = episode.replace('Episode ', '')
                        print title
                        print imdb_id
                        print season
                        print episode
                        meta = grab.get_episode_meta(title,imdb_id,season,episode)
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                                'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                                'director': meta['director'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id']}

          return infoLabels
############
#Metahandler
############


#########
#Download
#########
def DOWNLOAD(name,url):
        download_status = local.getSetting('download-status')
        dir = local.getSetting('download-folder')
        if '.mp4' in url:
                ext = '.mp4'
        elif '.flv' in url:
                ext = '.flv'
        elif '.avi' in url:
                ext = '.avi'
        elif '.mkv' in url:
                ext = '.mkv'
        file_name = name+ext
        u = urllib2.urlopen(url)
        f = open(dir+file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        size = file_size
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        Notify('small','Downloading:', '%s Bytes: %s' % (file_name, file_size) ,5000)
        file_size_dl = 0
        block_sz = 20480
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            if download_status == 'false':
                    Notify('small','Downloading: '+name, '%s   of   %s' % (status, size),'')
        f.close()
        Notify('small','Download: '+name, 'Completed' ,10000)
#########
#########
        

##############
#Notifications
##############
def Notify(typeq,title,message,times, line2='', line3=''):
     if typeq == 'small':
            smallicon= addon.get_icon()
            xbmc.executebuiltin("XBMC.Notification("+title+","+message+","''","+smallicon+")")
     elif typeq == 'big':
            dialog = xbmcgui.Dialog()
            dialog.ok(' '+title+' ', ' '+message+' ', line2, line3)
     else:
            dialog = xbmcgui.Dialog()
            dialog.ok(' '+title+' ', ' '+message+' ')
##############
##############
            

##################
#Cleaner for names
##################
def CLEAN(name):
        name = name.replace('&amp;','&')
        name = name.replace('&#x27;',"'")
        urllib.quote(u'\xe9'.encode('UTF-8'))
        name = name.replace(u'\xe9','e')
        urllib.quote(u'\xfa'.encode('UTF-8'))
        name = name.replace(u'\xfa','u')
        urllib.quote(u'\xed'.encode('UTF-8'))
        name = name.replace(u'\xed','i')
        urllib.quote(u'\xe4'.encode('UTF-8'))
        name = name.replace(u'\xe4','a')
        urllib.quote(u'\xf4'.encode('UTF-8'))
        name = name.replace(u'\xf4','o')
        urllib.quote(u'\u2013'.encode('UTF-8'))
        name = name.replace(u'\u2013','-')
        urllib.quote(u'\xe0'.encode('UTF-8'))
        name = name.replace(u'\xe0','a')
        try: name=messupText(name,True,True)
        except: pass
        try:name = name.decode('UTF-8').encode('UTF-8','ignore')
        except: pass
        return name

def ParseDescription(plot):
	if ("&nbsp;" in plot):  plot=plot.replace('&nbsp;' ," ")
	if ('&#' in plot) and (';' in plot):
		if ("&#8211;" in plot): plot=plot.replace("&#8211;","-")
		if ("&#8216;" in plot): plot=plot.replace("&#8216;","'")
		if ("&#8217;" in plot): plot=plot.replace("&#8217;","'")
		if ("&#8220;" in plot): plot=plot.replace('&#8220;','"')
		if ("&#8221;" in plot): plot=plot.replace('&#8221;','"')
		if ("&#215;"  in plot): plot=plot.replace('&#215;' ,'x')
		if ("&#x27;"  in plot): plot=plot.replace('&#x27;' ,"'")
		if ("&#xF4;"  in plot): plot=plot.replace('&#xF4;' ,"o")
		if ("&#xb7;"  in plot): plot=plot.replace('&#xb7;' ,"-")
		if ("&#xFB;"  in plot): plot=plot.replace('&#xFB;' ,"u")
		if ("&#xE0;"  in plot): plot=plot.replace('&#xE0;' ,"a")
		if ("&#0421;" in plot): plot=plot.replace('&#0421;',"")
		if ("&#xE9;" in plot):  plot=plot.replace('&#xE9;' ,"e")
		if ("&#xE2;" in plot):  plot=plot.replace('&#xE2;' ,"a")
		if ("&#038;" in plot):  plot=plot.replace('&#038;' ,"&")
		if ('&#' in plot) and (';' in plot):
			try:		matches=re.compile('&#(.+?);').findall(plot)
			except:	matches=''
			if (matches is not ''):
				for match in matches:
					if (match is not '') and (match is not ' ') and ("&#"+match+";" in plot):  
						try: plot=plot.replace("&#"+match+";" ,"")
						except: pass
	for i in xrange(127,256):
		try: plot=plot.replace(chr(i),"")
		except: pass
	return plot
def unescape_(s):
	p = htmllib.HTMLParser(None)
	p.save_bgn()
	p.feed(s)
	return p.save_end()
def messupText(t,_html=False,_ende=False,_a=False,Slashes=False):
	if (_html==True): 
		try: t=HTMLParser.HTMLParser().unescape(t)
		except: t=t
		try: t=ParseDescription(t)
		except: t=t
	if (_ende==True): 
		try: t=t.encode('ascii', 'ignore'); t=t.decode('iso-8859-1')
		except: t=t
	if (_a==True): 
		try: t=_addon.decode(t); t=_addon.unescape(t)
		except: t=t
	if (Slashes==True): 
		try: t=t.replace( '_',' ')
		except: t=t
	return t

##################
##################
     

##########
#Favorites
##########
def addFavorite(name,url,year):
     saved_favs = cache.get('favourites')
     favs = []
     if saved_favs:
          favs = eval(saved_favs)
          if favs:
               if (name,url,year) in favs:
                    Notify('small',name,'Already in Favorites',9000)
                    return
     favs.append((name,url,year))         
     cache.set('favourites', str(favs))
     Notify('small',name,'Succesfully Added To Favorites',9000)

def removeFavorite(name,url,year):
    saved_favs = cache.get('favourites')
    if saved_favs:
        favs = eval(saved_favs)
        favs.remove((name,url,year))   
        cache.set('favourites', str(favs))
        xbmc.executebuiltin("XBMC.Container.Refresh")
        Notify('small',name,'Succesfully Removed From Favorites',9000)

def getFavorites():
     saved_favs = cache.get('favourites')
     if saved_favs:
          favs = sorted(eval(saved_favs))
          if favs:
               for fav in favs:
                    return favs
          else:
                    Notify('small','Sorry','You have no Favorites Added',9000)


def addFavoriteTV(name,url,types):
     saved_favs = cache.get('favouritesTV')
     favs = []
     if saved_favs:
          favs = eval(saved_favs)
          if favs:
               if (name,url,types) in favs:
                    Notify('small',name,'Already in Favorites',9000)
                    return
     favs.append((name,url,types))         
     cache.set('favouritesTV', str(favs))
     Notify('small',name,'Succesfully Added To Favorites',9000)

def removeFavoriteTV(name,url,types):
    saved_favs = cache.get('favouritesTV')
    if saved_favs:
        favs = eval(saved_favs)
        favs.remove((name,url,types))   
        cache.set('favouritesTV', str(favs))
        xbmc.executebuiltin("XBMC.Container.Refresh")
        Notify('small',name,'Succesfully Removed From Favorites',9000)

def getFavoritesTV():
     saved_favs = cache.get('favouritesTV')
     if saved_favs:
          favs = sorted(eval(saved_favs))
          if favs:
               for fav in favs:
                    return favs
          else:
                    Notify('small','Sorry','You have no Favorites Added',9000)

#Kid Mode
def addFavoriteKIDMOVIE(name,url,year):
     saved_favs = cache.get('favouritesKIDMOVIE')
     favs = []
     if saved_favs:
          favs = eval(saved_favs)
          if favs:
               if (name,url,year) in favs:
                    Notify('small',name,'Already in Kid Movies',9000)
                    return
     favs.append((name,url,year))         
     cache.set('favouritesKIDMOVIE', str(favs))
     Notify('small',name,'Succesfully Added To Kid Movies',9000)

def removeFavoriteKIDMOVIE(name,url,year):
    saved_favs = cache.get('favouritesKIDMOVIE')
    if saved_favs:
        favs = eval(saved_favs)
        favs.remove((name,url,year))   
        cache.set('favouritesKIDMOVIE', str(favs))
        xbmc.executebuiltin("XBMC.Container.Refresh")
        Notify('small',name,'Succesfully Removed From Kid Movies',9000)

def getFavoritesKIDMOVIE():
     saved_favs = cache.get('favouritesKIDMOVIE')
     if saved_favs:
          favs = sorted(eval(saved_favs))
          if favs:
               for fav in favs:
                    return favs
          else:
                    Notify('small','Sorry','You have no Kid Movies Added',9000)

def getFavoritesKIDMOVIE2():
     saved_favs = cache.get('favouritesKIDMOVIE')
     if saved_favs:
          favs = sorted(eval(saved_favs))
          if favs:
               for fav in favs:
                    return favs


def addFavoriteKIDTV(name,url,types):
     saved_favs = cache.get('favouritesKIDTV')
     favs = []
     if saved_favs:
          favs = eval(saved_favs)
          if favs:
               if (name,url,types) in favs:
                    Notify('small',name,'Already in Kid TV',9000)
                    return
     favs.append((name,url,types))         
     cache.set('favouritesKIDTV', str(favs))
     Notify('small',name,'Succesfully Added To Kid TV',9000)

def removeFavoriteKIDTV(name,url,types):
    saved_favs = cache.get('favouritesKIDTV')
    if saved_favs:
        favs = eval(saved_favs)
        favs.remove((name,url,types))   
        cache.set('favouritesKIDTV', str(favs))
        xbmc.executebuiltin("XBMC.Container.Refresh")
        Notify('small',name,'Succesfully Removed From Kid TV',9000)

def getFavoritesKIDTV():
     saved_favs = cache.get('favouritesKIDTV')
     if saved_favs:
          favs = sorted(eval(saved_favs))
          if favs:
               for fav in favs:
                    return favs
          else:
                    Notify('small','Sorry','You have no Kid TV Added',9000)

def getFavoritesKIDTV2():
     saved_favs = cache.get('favouritesKIDTV')
     if saved_favs:
          favs = sorted(eval(saved_favs))
          if favs:
               for fav in favs:
                    return favs

##########
##########

          

###############################################################
#Library Integration First attempt not very pretty needs work
###############################################################
#create STRM file and add to movie library
def AddToLibrary(name,url):
        save_path = local.getSetting('movies25-folder')
        save_path = xbmc.translatePath(save_path)
        strm_string = addon.build_plugin_url(
            {'mode': '11', 'url': url, 'name': name})
        filename = '%s.strm' % name
        final_path = os.path.join(save_path, name, filename)
        final_path = xbmc.makeLegalFilename(final_path)
        if not xbmcvfs.exists(os.path.dirname(final_path)):
            try:
                xbmcvfs.mkdirs(os.path.dirname(final_path))
            except Exception, e:
                addon.log('Failed to create directory %s' % final_path)
        try:
            file_desc = xbmcvfs.File(final_path, 'w')
            file_desc.write(strm_string)
            file_desc.close()
            Notify('small',name, 'Added to Library' ,8000)
        except Exception, e:
                Notify('small',name, 'ERROR adding to Library' ,8000)
                addon.log('Failed to create .strm file: %s\n%s' % (final_path, e))

#Play from the Library STRM file *no directories
def LIBRARYPLAY(name,url):
        EnableMeta = local.getSetting('Enable-Meta')
        iconimage = ''
        name2 = name
        if EnableMeta == 'true':
                infoLabels = GRABMETA(name2,'')
        try: img = infoLabels['cover_url']
        except: img = iconimage
        match=re.compile('<li class="link_name">\n              (.+?)            </li>\n                        <li class="playing_button"><span><a href="(.+?)"').findall(net.http_GET(url).content)
        List=[]; ListU=[]; c=0
        for name,url in match:
                url = 'http://www.movie25.so'+url+'@'+name2
                c=c+1; List.append(str(c)+'.)  '+name); ListU.append(url)
        dialog=xbmcgui.Dialog()
        rNo=dialog.select('Select A Host', List)
        rName=List[rNo]
        rURL=ListU[rNo]
        print 'Play '+rURL
        LIBRARYPLAY2(rName,rURL)

def LIBRARYPLAY2(name,url):
        EnableMeta = local.getSetting('Enable-Meta')
        name2 = url.split('@')[1]
        url = url.split('@')[0]
        iconimage = ''
        if EnableMeta == 'true':
                infoLabels = GRABMETA(name2,'')
        try: img = infoLabels['cover_url']
        except: img = iconimage
        match=re.compile('type="button" onclick="location.href=\'(.+?)\'"  value="Click Here to Play"').findall(net.http_GET(url).content)
        for url in match:
                nono = ['http://www.movie25.so/watch/']
                if url not in nono:
                        print 'Play2 '+url
        LIBRARYSTREAM(name,url+'@'+name2,img)

def LIBRARYSTREAM(name,url,img):
        iconimage = img
        name = url.split('@')[1]
        url = url.split('@')[0]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
        try:
               addon.resolve_url(streamlink)
        except:
               Notify('small','Sorry Link Removed:', 'Please try another one.',9000)
        #except : pass
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo('video',infoLabels={ "Title": name })

        xbmc.sleep(2000)
        
        xbmc.Player ().play(streamlink, liz, False)
###############################################################
###############################################################
