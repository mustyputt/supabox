#TV Release Module by o9r1sh September 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

net = main.net
artwork = main.artwork
base_url = 'http://tv-release.org'
settings = main.settings

def TV_CATEGORIES():
        main.addDir('XVID Episodes',base_url + '/index.php?page=1&cat=TV-XviD','tvreleaseIndex',artwork + '/main/xvidtv.png')
        main.addDir('MP4 Episodes',base_url + '/index.php?page=1&cat=TV-Mp4','tvreleaseIndex',artwork + '/main/mp4tv.png')
        main.addDir('480P Episodes',base_url + '/index.php?page=1&cat=TV-480p','tvreleaseIndex',artwork + '/main/sdtv.png')
        main.addDir('720P Episodes',base_url + '/index.php?page=1&cat=TV-720p','tvreleaseIndex',artwork + '/main/hdtv.png')
        main.addDir('Foreign Episodes',base_url + '/index.php?page=1&cat=TV-Foreign','tvreleaseIndex',artwork + '/main/foreign.png')
        main.addDir('Search',base_url + 'none','tvreleaseSearch',artwork + '/main/search.png')

def HDMOVIES():
        INDEX(base_url + '/index.php?page=1&cat=Movies-720p')

        
def MOVIE_CATEGORIES():
        main.addDir('XVID Movies',base_url + '/index.php?page=1&cat=Movies-XviD','tvreleaseIndex',artwork + '/main/xvidmovies.png')
        main.addDir('480P Movies',base_url + '/index.php?page=1&cat=Movies-480p','tvreleaseIndex',artwork + '/main/sdmovies.png')
        main.addDir('720P Movies',base_url + '/index.php?page=1&cat=Movies-720p','tvreleaseIndex',artwork + '/main/hdmovies.png')
        main.addDir('DVD-R Movies',base_url + '/index.php?page=1&cat=Movies-DVDR','tvreleaseIndex',artwork + '/main/dvdrmovies.png')
        main.addDir('Foreign Movies',base_url + '/index.php?page=1&cat=Movies-Foreign','tvreleaseIndex',artwork + '/main/foreign.png')
        
def INDEX(url):
        np_url = ''
        types = None
        last_page = None
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile("<td width=\'60%\' style=\'text-align:left; font-size:12px;font-weight:bold;\'><a href=\'(.+?)'>(.+?)</a></td").findall(link)
        lp=re.compile("<span class='zmg_pn_standar'><a href=.+?>(.+?)</a>").findall(link)

        if len(lp) > 0:
                last_page = int(lp[11])
                
        current_url = response.geturl()
        head,sep,tail = current_url.partition('page=')
        a,b,c = tail.partition('&cat=')
        cur_page = int(a)
        next_page = cur_page + 1
        np_url = head +  sep + str(next_page) + b + c

        if cur_page < last_page:
                if settings.getSetting('nextpagetop') == 'true':       
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'tvreleaseIndex',artwork + '/main/next.png')

        for url,name in match:
                try:
                        if 'Filech' in name:
                                continue
                        else:
                                url = base_url + '/' + url
                                show = re.split('[Ss]\d\d[Ee]\d\d',name)
                
                                if len(show) == 2:
                                        types = 'episode'
                                else:
                                        types = 'movie'

                                if types == 'episode':
                                        try:        
                                                main.addEDir(name,url,'tvreleaseVideoLinks','',show[0])
                                        except:
                                                continue
                        
                                if types == 'movie':
                                        try:        
                                                main.addMDir(name,url,'tvreleaseVideoLinks','','',False)      
                                        except:
                                                continue
                except:
                        continue
        if types == 'episode':
                main.AUTOVIEW('episodes')
        else:
                main.AUTOVIEW('movies')
        if cur_page < last_page:
                if settings.getSetting('nextpagebottom') == 'true':       
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'tvreleaseIndex',artwork + '/main/next.png')


def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        match=re.compile("<a target='_blank' href='(.+?)'>").findall(link)
        for url in match:
                if main.resolvable(url):
                        main.addHDir(name,url,'resolve','')

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','%20')
                url = base_url + '/?s=' + search + '&cat='
                
                INDEX(url)

def MASTERSEARCH(search):
        url = base_url + '/?s=' + search + '&cat='    
        INDEX(url)

