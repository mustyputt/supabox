#NewMyVideoLinks Module by o9r1sh September 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

net = main.net
artwork = main.artwork
base_url = 'http://www.myvideolinks.eu'
settings = main.settings

def CATEGORIES():
        main.addDir('Yify Movies',base_url + '/category/movies/yify/','newMyVideoLinksIndex',artwork + '/main/yify.png')
        main.addDir('Recent Movies',base_url + '/category/movies/','newMyVideoLinksIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Search','none','newMyVideoLinksSearch',artwork + '/main/search.png')

def HDMOVIES():
        INDEX(base_url + '/category/movies/yify/')


def TVCATEGORIES():
        main.addDir('Recent Episodes',base_url + '/category/tv-shows/','newMyVideoLinksIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Search','none','newMyVideoLinksSearch',artwork + '/main/search.png')
        
def INDEX(url):
        types = None
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" rel=".+?" title=".+?"> <img src="(.+?)"  title="(.+?)" class="alignleft" alt=".+?" /></a>').findall(link)
        np=re.compile("<span class='pages'>Page (.+?)</span>").findall(link)
        if len(np) > 0:
                next_page = ''
                numbers = np[0]
                head,sep,tail = numbers.partition('of')
                current_page = int(head)
                last_page = int(tail)
                nex = current_page + 1
                if nex < last_page:
                        if current_page == 1:
                                next_page = url + '/page/' + str(nex)
                        else:
                                a,b,c = url.partition('/page/')
                                next_page = url + a + b + str(nex)
                        if settings.getSetting('nextpagetop') == 'true':
                                main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'newMyVideoLinksIndex',artwork + '/main/next.png')

        for url,thumbnail,name in match:
                if '<img src=' in name:
                        continue
                else:
                        show = re.split('[Ss]\d\d[Ee]\d\d',name)
                        
                        if len(show) == 2:
                                types = 'episode'
                        else:
                                types = 'movie'

                        if types == 'episode':
                                try:        
                                        main.addEDir(name,url,'newMyVideoLinksVideoLinks',thumbnail,show[0])
                                except:
                                        continue
                                
                        if types == 'movie':
                                split = re.split('(\d\d\d\d)',name)
                                try:
                                        year =  str(split[1])
                                except:
                                        pass
                                try:        
                                        main.addMDir(name,url,'newMyVideoLinksVideoLinks',thumbnail,year,False)      
                                except:
                                        continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'newMyVideoLinksIndex',artwork + '/main/next.png')


        if types == 'episode':
                main.AUTOVIEW('episodes')
        else:
                main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb,year):
        skip = 4
        inc = 0
        link = net.http_GET(url).content
        match=re.compile('<li><a href="(.+?)">.+?</a></li>').findall(link)
        for url in match:
                if inc > skip:
                        if main.resolvable(url):
                                try:
                                        main.addHDir(name,url,'resolve','')
                                except:
                                        continue
                inc += 1

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '/index.php?s=' + search
                INDEX(url)


def MASTERSEARCH(search):
                url = base_url + '/index.php?s=' + search
                INDEX(url)
