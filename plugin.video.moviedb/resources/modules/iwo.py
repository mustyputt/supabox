#IWatchOnline Module by : Bazetamer   Thanks to O9 for the basic code setup
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
import downloader
import extract
import time,re
import datetime
import shutil
from metahandler import metahandlers
from resources.modules import main
from resources.modules import live
from resources.utils import buggalo


from addon.common.addon import Addon
from addon.common.net import Net
net = Net(http_debug=True)
        
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')

base_url = 'http://www.iwatchonline.to'






#PATHS
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg', ''))
else:
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart/fanart.jpg', ''))

    


#Main Links 

def CATZEEMOVIES (url):
        main.addDir('Random Movies ','http://www.zmovie.tw/','zeemovies','','','dir')
        main.addDir('Genres','http://www.zmovie.tw/search/genre','zeegenres','','','dir')
        main.addDir('Featured Movies','http://www.zmovie.tw/movies/featured','zeemovies','','','dir')
        main.addDir('New Movies','http://www.zmovie.tw/movies/new','zeemovies','','','dir')
        main.addDir('Top Movies All-Time','http://www.zmovie.tw/movies/top','zeemovies','','','dir')

        
        main.AUTO_VIEW('')

def CATIWO (url):
        live.addDir('Featured Movies','http://www.iwatchonline.to/movies?sort=featured','iwomovies','','','')
        live.addDir('Popular','http://www.iwatchonline.to/movies?sort=popular','iwomovies','','','')
        live.addDir('Genre','none','iwogenres','','','')
        live.addDir('A-Z','none','iwoalph','','','')
        live.addDir('HD Movies','none','iwohd','','','')
        
        
        main.AUTO_VIEW('')

def CATTVSHOWS (url):
        main.addDir('Genre','http://www.iwatchonline.to/movies','iwogenres','','','dir')
        
        main.AUTO_VIEW('')

def ZEEGENRES(url):
        link = net.http_GET(url).content
        match=re.compile('float:left"> <a href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:
            name = name.replace("&#039;s","'s")
            favtype = 'movie'
            main.addDir(name,url,'zeemovies','','',favtype)
            main.AUTO_VIEW('movies')

def IWOHD():
        main.addDir('Recently Added',base_url +'//movies?sort=latest&quality=hd','iwomovies','','','')
        main.addDir('Popular',base_url + '//movies?sort=popular&quality=hd','iwomovies','','','')
        main.addDir('A-Z','none','iwohdalph','','','')            

def IWOGENRES(url):
        main.addDir('Action','http://www.iwatchonline.to/movies?gener=action','iwomovies','','','dir')
        main.addDir('Adventure','http://www.iwatchonline.to/movies?gener=adventure','iwomovies','','','dir')
        main.addDir('Animation','http://www.iwatchonline.to/movies?gener=animation','iwomovies','','','dir')
        main.addDir('Biography','http://www.iwatchonline.to/movies?gener=biography','iwomovies','','','dir')
        main.addDir('Comedy','http://www.iwatchonline.to/movies?gener=comedy','iwomovies','','','dir')
        main.addDir('Crime','http://www.iwatchonline.to/movies?gener=crime','iwomovies','','','dir')
        main.addDir('Documentary','http://www.iwatchonline.to/movies?gener=documentery','iwomovies','','','dir')
        main.addDir('Drama','http://www.iwatchonline.to/movies?gener=drama','iwomovies','','','dir')
        main.addDir('Family','http://www.iwatchonline.to/movies?gener=family','iwomovies','','','dir')
        main.addDir('Fantasy','http://www.iwatchonline.to/movies?gener=fantasy','iwomovies','','','dir')
        main.addDir('Film-Noir','http://www.iwatchonline.to/movies?gener=film-noir','iwomovies','','','dir')
        main.addDir('History','http://www.iwatchonline.to/movies?gener=history','iwomovies','','','dir')
        main.addDir('Horror','http://www.iwatchonline.to/movies?gener=horror','iwomovies','','','dir')
        main.addDir('Music','http://www.iwatchonline.to/movies?gener=music','iwomovies','','','dir')
        main.addDir('Musical','http://www.iwatchonline.to/movies?gener=musical','iwomovies','','','dir')
        main.addDir('Mystery','http://www.iwatchonline.to/movies?gener=mystery','iwomovies','','','dir')
        main.addDir('News','http://www.iwatchonline.to/movies?gener=news','iwomovies','','','dir')
        main.addDir('Romance','http://www.iwatchonline.to/movies?gener=romance','iwomovies','','','dir')
        main.addDir('Sci-Fi','http://www.iwatchonline.to/movies?gener=sci-fi','iwomovies','','','dir')
        main.addDir('Short','http://www.iwatchonline.to/movies?gener=short','iwomovies','','','dir')
        main.addDir('Sport','http://www.iwatchonline.to/movies?gener=sport','iwomovies','','','dir')
        main.addDir('Thriller','http://www.iwatchonline.to/movies?gener=thriller','iwomovies','','','dir')
        main.addDir('War','http://www.iwatchonline.to/movies?gener=war','iwomovies','','','dir')
        main.addDir('Western','http://www.iwatchonline.to/movies?gener=western','iwomovies','','','dir')
        main.AUTO_VIEW('')

        
def IWOALPH():
        main.addDir('#',base_url + '/movies?startwith=09','iwomovies','','','dir')
        main.addDir('A',base_url + '/movies?startwith=a','iwomovies','','','dir')
        main.addDir('B',base_url + '/movies?startwith=b','iwomovies','','','dir')
        main.addDir('C',base_url + '/movies?startwith=c','iwomovies','','','dir')
        main.addDir('D',base_url + '/movies?startwith=d','iwomovies','','','dir')
        main.addDir('E',base_url + '/movies?startwith=e','iwomovies','','','dir')
        main.addDir('F',base_url + '/movies?startwith=f','iwomovies','','','dir')
        main.addDir('G',base_url + '/movies?startwith=g','iwomovies','','','dir')
        main.addDir('H',base_url + '/movies?startwith=h','iwomovies','','','dir')
        main.addDir('I',base_url + '/movies?startwith=i','iwomovies','','','dir')
        main.addDir('J',base_url + '/movies?startwith=j','iwomovies','','','dir')
        main.addDir('K',base_url + '/movies?startwith=k','iwomovies','','','dir')
        main.addDir('L',base_url + '/movies?startwith=l','iwomovies','','','dir')
        main.addDir('M',base_url + '/movies?startwith=m','iwomovies','','','dir')
        main.addDir('N',base_url + '/movies?startwith=n','iwomovies','','','dir')
        main.addDir('O',base_url + '/movies?startwith=o','iwomovies','','','dir')
        main.addDir('P',base_url + '/movies?startwith=p','iwomovies','','','dir')
        main.addDir('Q',base_url + '/movies?startwith=q','iwomovies','','','dir')
        main.addDir('R',base_url + '/movies?startwith=r','iwomovies','','','dir')
        main.addDir('S',base_url + '/movies?startwith=s','iwomovies','','','dir')
        main.addDir('T',base_url + '/movies?startwith=t','iwomovies','','','dir')
        main.addDir('U',base_url + '/movies?startwith=u','iwomovies','','','dir')
        main.addDir('V',base_url + '/movies?startwith=v','iwomovies','','','dir')
        main.addDir('W',base_url + '/movies?startwith=w','iwomovies','','','dir')
        main.addDir('X',base_url + '/movies?startwith=x','iwomovies','','','dir')
        main.addDir('Y',base_url + '/movies?startwith=y','iwomovies','','','dir')
        main.addDir('Z',base_url + '/movies?startwith=z','iwomovies','','','dir')    
def IWOHDALPH():
        main.addDir('#',base_url + '/movies?quality=hd&startwith=09','iwomovies','','','dir')
        main.addDir('A',base_url + '/movies?quality=hd&startwith=a','iwomovies','','','dir')
        main.addDir('B',base_url + '/movies?quality=hd&startwith=b','iwomovies','','','dir')
        main.addDir('C',base_url + '/movies?quality=hd&startwith=c','iwomovies','','','dir')
        main.addDir('D',base_url + '/movies?quality=hd&startwith=d','iwomovies','','','dir')
        main.addDir('E',base_url + '/movies?quality=hd&startwith=e','iwomovies','','','dir')
        main.addDir('F',base_url + '/movies?quality=hd&startwith=f','iwomovies','','','dir')
        main.addDir('G',base_url + '/movies?quality=hd&startwith=g','iwomovies','','','dir')
        main.addDir('H',base_url + '/movies?quality=hd&startwith=h','iwomovies','','','dir')
        main.addDir('I',base_url + '/movies?quality=hd&startwith=i','iwomovies','','','dir')
        main.addDir('J',base_url + '/movies?quality=hd&startwith=j','iwomovies','','','dir')
        main.addDir('K',base_url + '/movies?quality=hd&startwith=k','iwomovies','','','dir')
        main.addDir('L',base_url + '/movies?quality=hd&startwith=l','iwomovies','','','dir')
        main.addDir('M',base_url + '/movies?quality=hd&startwith=m','iwomovies','','','dir')
        main.addDir('N',base_url + '/movies?quality=hd&startwith=n','iwomovies','','','dir')
        main.addDir('O',base_url + '/movies?quality=hd&startwith=o','iwomovies','','','dir')
        main.addDir('P',base_url + '/movies?quality=hd&startwith=p','iwomovies','','','dir')
        main.addDir('Q',base_url + '/movies?quality=hd&startwith=q','iwomovies','','','dir')
        main.addDir('R',base_url + '/movies?quality=hd&startwith=r','iwomovies','','','dir')
        main.addDir('S',base_url + '/movies?quality=hd&startwith=s','iwomovies','','','dir')
        main.addDir('T',base_url + '/movies?quality=hd&startwith=t','iwomovies','','','dir')
        main.addDir('U',base_url + '/movies?quality=hd&startwith=u','iwomovies','','','dir')
        main.addDir('V',base_url + '/movies?quality=hd&startwith=v','iwomovies','','','dir')
        main.addDir('W',base_url + '/movies?quality=hd&startwith=w','iwomovies','','','dir')
        main.addDir('X',base_url + '/movies?quality=hd&startwith=x','iwomovies','','','dir')
        main.addDir('Y',base_url + '/movies?quality=hd&startwith=y','iwomovies','','','dir')
        main.addDir('Z',base_url + '/movies?quality=hd&startwith=z','iwomovies','','','dir')

def ZEEMOVIES(url):
        link = net.http_GET(url).content
        
        match=re.compile('relative;"><a href="(.+?)" title="(.+?)">').findall(link)
        
        inc = 0
        if len(match) > 0:
         for url,name in match:      


             inc += 1
             if inc > 8:
                movie_name = name[:-6]
                year = name[-6:]
                movie_name = movie_name.decode('UTF-8','ignore')
                                
                data = main.GRABMETA(movie_name,year)
                thumb = data['cover_url']
                

                favtype = 'movie'
                main.addDir(name,url,'zeevidpage',thumb,data,favtype)

                main.AUTO_VIEW('movies')

def IWOMOVIES(url):
        link = net.http_GET(url).content
        
        match=re.compile('<a href="(.+?)" class=".+?" rel=".+?">\r\n\t\t\t\t\t\t\t<img class=".+?" src="(.+?)" alt="">\r\n\t\t\t\t\t\t\t <div class=".+?">.+?</div>\t  \r\n\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t<div class=".+?">(.+?)\t\t\t\t\t\t<div').findall(link)
        inc = 0
        if len(match) > 0:
         for url,thumbnail,name in match:       

             inc += 1
             if inc > 6:
                movie_name = name[:-4]
                year = name[-4:]
                movie_name = movie_name.decode('UTF-8','ignore')               
                data = main.GRABMETA(movie_name,year)
                favtype = 'movie'
                main.addDir(name,url,'iwovidpage',thumbnail,data,favtype)
                match=re.compile('<li class="next pagea"><a href="(.+?)">Next &rarr;</a>').findall(link)
         for url in match:       
          if len(match) > 0:
                  url = url.replace('&amp;','&')
                  main.addDir('Next Page',url,'iwomovies','','','dir')

                  main.AUTO_VIEW('movies')



def LATESTO(url):
        link = net.http_GET(url).content
        match=re.compile('<a data-id="tooltip" href="(.+?)">\n<i class="icon-c-play fixed"></i>\n<img width="260" height="380" class="poster" src="(.+?)" alt="(.+?)"/>\n</a>\n<div class="caption">\n<a data-id="tooltip".+?">\n<h4>.+?</h4>\n</a>\n<table class="table table-custom">\n<tr>\n<th>Genre </th>\n<td>.+?</td>\n</tr>\n<tr>\n<th>Year </th>\n<td>(.+?)</td>').findall(link)
        inc = 0
        if len(match) > 0:
         for url,thumb,name,year in match:       
             name = name+'('+year+')'

             inc += 1
             if inc > 8:
                movie_name = name[:-6]
                year = name[-6:]
                movie_name = movie_name.decode('UTF-8','ignore') 
                data = main.GRABMETA(movie_name,year)
                favtype = 'movie'
                main.addDir(name,url,'linkpage',thumb,data,favtype)

                main.AUTO_VIEW('movies')

                   
def LINKPAGE(url,name):
        link = net.http_GET(url).content
        match=re.compile('target="_blank"   href="(.+?)"> <b> Watch Full </b></a> </td>').findall(link)
        for url in match:
                main.addDir(name,url,'vidpage',thumb,data,favtype)
                    
                favtype = 'movie'
                main.AUTO_VIEW('movies')
                
def ZEEVIDPAGE(url,name):
        dlfoldername = name
        titlename = name
        link = net.http_GET(url).content
        match=re.compile('target="_blank"   href="(.+?)"> <b> Watch Full </b></a> </td>').findall(link)
        for urls in match:
                
                hmf = urlresolver.HostedMediaFile(urls)
                   ##########################################
                print 'URLS is ' +urls
                
                print 'Pre HMF url is  ' +urls
                if hmf:
                          #try:
                                    host = hmf.get_host()
                                    hthumb = main.GETHOSTTHUMB(host)  
                                    favtype = 'movie'
                                    hostname = main.GETHOSTNAME(host)
                                    main.addDLDir(titlename+'[COLOR lime]'+hostname+'[/COLOR]',urls,'vidpage',hthumb,'',dlfoldername,favtype,'')
                                    favtype = 'movie'
                                    main.AUTO_VIEW('')





def IWOVIDPAGE(url,name):
        dlfoldername = name
        titlename = name
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" target="_blank" rel="nofollow">').findall(link)
        for url in match:
            link = net.http_GET(url).content
            match=re.compile('<iframe name="frame" class="frame" src="(.+?)"').findall(link)
            for urls in match:
                hmf = urlresolver.HostedMediaFile(urls)
                   ##########################################
                print 'URLS is ' +urls
                
                print 'Pre HMF url is  ' +urls
                if hmf:
                          #try:
                                    host = hmf.get_host()
                                    hthumb = main.GETHOSTTHUMB(host)
                                    favtype = 'movie'
                                    hostname = main.GETHOSTNAME(host)
                                    #main.addDLDir(titlename,urls,'vidpage',hthumb,'',dlfoldername,favtype,thumb)
                                    main.addDir(titlename+'[COLOR lime]'+hostname+'[/COLOR]',urls,'vidpage',hthumb,'','')
                                    main.AUTO_VIEW('')                
                 


def ZEERESPASS(url,name):
        #if 'vidshark' in url:
             #vidshark.VIDINDEX(url)

        main.RESOLVE(name,url,'')

def IWOFORVID(url,name):
        link = net.http_GET(url).content
        match=re.compile('<iframe name="frame" class="frame" src="(.+?)"').findall(link)
        for url in match:

         main.RESOLVE(name,url,'')


	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching......" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	INDEX(searchUrl)

	main.AUTO_VIEW('movies') 
        

        




              










