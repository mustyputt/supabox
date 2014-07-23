#Epornik module by o9r1sh

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,main,urlresolver,xbmc,os

net = main.net

artwork = main.artwork
base_url = 'http://www.epornik.com'
settings = main.settings

def CATEGORIES():
        main.addDir('Videos',base_url + '/search.php','epornikIndex',artwork + '/main/videos.png')
        main.addDir('Search','none','epornikSearch',artwork + '/main/search.png')

def INDEX(url):
        np_url = ''
        link = net.http_GET(url).content
        match=re.compile('<a href=".+?">.+?</a>\n                        </div>\n                        <div class="img_preview_item"> <a href="(.+?)"><img src="(.+?)" width=".+?" height=".+?" alt="(.+?)" /></a>').findall(link)
        np=re.compile("<a href='(.+?)' id='next'>Next</a>").findall(link)
        if len(np) > 0:
                if settings.getSetting('nextpagetop') == 'true':
                        np_url = base_url + '/' + np[0]
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'epornikIndex', artwork + '/main/next.png')
                

        for url,thumbnail,name in match:
                if name == 'evil 4 2010':
                        continue
                if name == 'evil 3 2007':
                        continue
                if name == 'evil 2 2004':
                        continue
                if name == 'evil 1':
                        continue
                if name == 'lkesi 4':
                        continue
                else:
                        url = base_url + url
                        thumbnail = base_url + thumbnail
                        try:
                                link = net.http_GET(url).content
                                match=re.compile('"file","(.+?)"').findall(link)
                                main.addDir(name,match[0],'resolve',thumbnail)
                        except:
                                continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        np_url = base_url + '/' + np[0]
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'epornikIndex', artwork + '/main/next.png')

                                   
def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '/search.php?q=' + search + '&x=-1085&y=-177'
                
                INDEX(url)


                


