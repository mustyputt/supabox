#'' module by o9r1sh
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,main,urlresolver,xbmc,os

net = main.net
artwork = main.artwork
settings = main.settings
base_url = 'http://www.shortoftheweek.com'

def categories():
        main.addDir('Categories',base_url + '/films','sotwSections',artwork + '/main/categories.png')
        main.addDir('Search','none','sotwSearch',artwork + '/main/search.png')
        

def sections(url):
        link = net.http_GET(url).content
        match=re.compile('<li id="cat.+?"><a href="(.+?)">(.+?)</a><span>').findall(link)
        for url,name in match:
                main.addDir(name,url,'sotwIndex','')

def index(url):
        npUrl = ''
        link = net.http_GET(url).content
        np=re.compile('class="wp-pagenavi">\n<span class="current">1</span><a href=".+?" class="page" title=".+?">.+?</a><a href="(.+?)" >next .+?</a></div>').findall(link)
        if len(np) > 0:
                npUrl = str(np[0])
        if settings.getSetting('nextpagetop') == 'true':
                main.addDir('[COLOR blue]Next Page[/COLOR]',npUrl,'sotwIndex',artwork + '/main/next.png')

                
        match=re.compile('<a href="(.+?)" title="(.+?)">\n\t\t\t\t\t<img width=".+?" height=".+?" src="(.+?)"').findall(link)
        match2=re.compile('<a href="(.+?)" title="(.+?)">\n\t\t\t\t\t<img src="(.+?)"').findall(link)

        for url,name,thumbnail in match:
                try:
                        main.addDir(name,url,'sotwVideoLinks',thumbnail)
                except:
                        pass

        for url,name,thumbnail in match2:
                try:
                        main.addDir(name,url,'sotwVideoLinks',thumbnail)
                except:
                        pass
        if settings.getSetting('nextpagebottom') == 'true':
                if len(np) > 0:
                        main.addDir('[COLOR blue]Next Page[/COLOR]',npUrl,'sotwIndex',artwork + '/main/next.png')

                
def videoLinks(url,name):
        link = net.http_GET(url).content
        match=re.compile('<a class="fancybox-video" href="(.+?)" title=".+?">').findall(link)

        inc = 0
        
        for url in match:
                if inc == 1:
                
                        if  'vimeo' in url:
                                head,sep,tail = url.partition('?')
                                head = head.replace('player.', '')
                                head = head.replace('/video', '')
                                head = head.replace('https://', '')
                        
                        elif  'youtube' in url:
                                head,sep,tail = url.partition('?')
                                
                        try:
                                main.addHDir(name,head,'resolve','')
                        except:
                                continue
                inc += 1
       
         
def search():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '/?s=' + search + '&search='
                print url
                
                index(url)


                


