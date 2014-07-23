#B-Movies module by o9r1sh
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,main,urlresolver,xbmc,os

net = main.net
artwork = main.artwork
settings = main.settings
base_url = 'http://www.bmovies.com'

def categories():
        main.addDir('Horror',base_url + '/horror','bMoviesIndex',artwork + '/genres/horror.png')
        main.addDir('Kung-Fu',base_url + '/kung-fu','bMoviesIndex',artwork + '/genres/kungfu.png')
        main.addDir('Sci-Fi',base_url + '/sci-fi','bMoviesIndex',artwork + '/genres/sci-fi.png')
        main.addDir('Western',base_url + '/western','bMoviesIndex',artwork + '/genres/western.png')
        main.addDir('Indie',base_url + '//content/free-b-indie-movie-streaming','bMoviesIndex',artwork + '/genres/indie.png')
                       
def index(url):
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" alt="" title=""  class="imagecache imagecache-movie_thumb" width=".+?" height=".+?" /></a></span>\n  </div>\n  \n  <div class="views-field-title">\n                <span class="field-content"><a href="(.+?)">(.+?)</a></span>').findall(link)
        pages=re.compile('<li class="pager-next"><a href="(.+?)" title="Go to next page"').findall(link)
        np_url = ''
        if len(pages) > 0:
                np_url = base_url + str(pages[0])
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'bMoviesIndex', artwork + '/main/next.png')

                
        for thumbnail,url,name in match:
                url = base_url + url
                try:
                        main.addMDir(name,url,'bMoviesVideoLinks',thumbnail,'',False)
                except:
                        pass
        if len(pages) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'bMoviesIndex', artwork + '/main/next.png')


                
        main.AUTOVIEW('movies')

def videoLinks(url,name):
        link = net.http_GET(url).content
        match=re.compile("config: {\r\n           \'file\': \'(.+?)'").findall(link)
        for url in match:
                try:
                        main.addHDir(name,url,'resolve',artwork + '/hosts/play.png')
                except:
                        pass
       



                


