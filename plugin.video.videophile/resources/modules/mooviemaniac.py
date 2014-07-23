#MoovieManiac Module by o9r1sh September 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

net = main.net
artwork = main.artwork
base_url = 'http://www.mooviemaniac.net'
settings = main.settings

def CATEGORIES():
        url = base_url + '/movies.htm'
        INDEX(url)
        
def INDEX(url):
        np_url= ''
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" target=".+?" onclick=".+?">\n  <img class=".+?" src="(.+?)" alt=".+?" title="(.+?)" onmousemove=".+?" style=".+?"/>').findall(link)
        if url == base_url + '/movies.htm':
                np_url = base_url + '/movies2.htm'
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'moovieManiacIndex',artwork + '/main/next.png')
        elif url == base_url + '/movies2.htm':
                np_url = base_url + '/movies3.htm'
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'moovieManiacIndex',artwork + '/main/next.png')
        elif url == base_url + '/movies3.htm':
                np_url = base_url + '/movies4.htm'
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'moovieManiacIndex',artwork + '/main/next.png')
                
        for url,thumbnail,name in match:
                if len(match) > 0:
                        thumbnail = base_url +'/' +  thumbnail
                        head, sep, tail = name.partition(')')
                        name = head[:-5]
                        year = head[-5:] + sep
                try:       
                        main.addMDir(name,url,'resolve',thumbnail,year,False)
                except:
                        continue
        if settings.getSetting('nextpagebottom') == 'true':
                if np_url == '':
                        pass
                else:
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'moovieManiacIndex',artwork + '/main/next.png')
                


        main.AUTOVIEW('movies')


