
# AFDAH Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers


try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.moviedb'
#addon = Addon(addon_id, sys.argv)
addon = main.addon

try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer






# Cache  
cache = StorageServer.StorageServer("MovieDB", 0)

mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')


# Global Stuff
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
settings = xbmcaddon.Addon(id=addon_id)
if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/', ''))
else:
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
grab=metahandlers.MetaData()
net = Net()

base_url ='http://afdah.com/'
base_genre ='http://afdah.com/genre/'
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def AFDAHCATS():

            
          main.addMDCDir('All Movies','http://afdah.com/category/watch-movies/','afdahindex',artwork + 'allmovies.jpg','','dir')
          main.addMDCDir('Featured Movies','http://afdah.com/category/featured/','afdahindex',artwork + 'featured.jpg','','dir')
          main.addMDCDir('Cinema Movies *Mostly Cams*','http://afdah.com/category/cinema/','afdahindex',artwork + 'cinema.jpg','','dir')
          main.addMDCDir('HD Movies','http://afdah.com/category/hd/','afdahindex',artwork + 'hdmovies.jpg','','dir')
          main.addMDCDir('Movies by Year','http://afdah.com/years/','afdahindexsec',artwork + 'years.jpg','','dir')
          main.addMDCDir('Movies by Country','http://afdah.com/country/','afdahindexsec',artwork + 'country.jpg','','dir')
          main.addMDCDir('Movies by Language','http://afdah.com/language/','afdahindexsec',artwork + 'language.jpg','','dir')
          main.addMDCDir('Movies by Genre','http://afdah.com/','afdahgenre',artwork + 'genre.jpg','','dir')
          main.addMDCDir('Search Movies','http://afdah.com/?s=','searchmovieafdah',artwork + 'search.jpg','','dir')
          main.AUTO_VIEW('')    


        
def AFDAHINDEX (url):
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" width=".+?" height=".+?" alt="(.+?)" /></a></div><h3 class="entry-title"><a href="(.+?)"').findall(link)
        for sitethumb, name,url in match:
                inc = 0
                movie_name = name[:-6]
                year = name[-6:]
                movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABMETA(movie_name,year)
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)
                           
                favtype = 'movie'
                main.addDir(name,url,'afdahlinkpage',thumb,data,favtype)
        nmatch=re.compile('<link rel=\'next\' href=\'(.+?)\'').findall(link)
        if len(nmatch) > 0: 
          for pageurl in nmatch:
                     
                main.addDir('Next Page',pageurl,'afdahindex',artwork +'nextpage.jpg','','dir')        
        main.AUTO_VIEW('movies')

        
def AFDAHINDEXSEC (url):
        link = net.http_GET(url).content
        match=re.compile('<td><a href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:        
            favtype = 'movie'
            main.addDir(name,base_url + url,'afdahindex','','',dir)
             
        main.AUTO_VIEW('movies')
        



def AFDAHGENRE(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="/genre/(.+?)"><span>(.+?)<').findall(link)
        for url,name in match:        
            favtype = 'movie'
            main.addDir(name,base_genre + url,'afdahindex','','',dir)


def AFDAHLINKPAGE(url,name,thumb,mainimg):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,'mainimg':mainimg}
        inc = 0
        mainimg = mainimg
        link = net.http_GET(url).content
        match=re.compile('<a rel="nofollow" href="(.+?)" target="_blank">').findall(link)
  
        for url in match:
           print 'host url look is' + url    
            
                   
           if inc < 50:
                
                   urls = url
                   hmf = urlresolver.HostedMediaFile(urls)
                   print 'URLS is ' +urls
                   if hmf:
                          #try:
                                  host = hmf.get_host()
                                  hthumb = main.GETHOSTTHUMB(host)
                                  data = main.GRABTVMETA(name,'')
                                  thumb = data['cover_url']
                                  favtype = 'movie'
                                  hostname = main.GETHOSTNAME(host)
                                  try:    
                                        main.addDLDir(name+'[COLOR lime]'+hostname+'[/COLOR]',urls,'vidpage',hthumb,data,dlfoldername,favtype,mainimg)
                                        inc +=1
                                  except:
                                        continue
                                   




#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHMOVIEAFDAH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for AFDAH Movies" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&x=0&y=0&type=title' 
	print "Searching URL: " + searchUrl 
	AFDAHINDEX (searchUrl)

	main.AUTO_VIEW('movies')



