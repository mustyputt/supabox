#'' module by o9r1sh
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,main,urlresolver,xbmc,os

net = main.net
artwork = main.artwork
settings = main.settings
base_url = ''

def categories():
        main.addDir('A-Z','none','mode',artwork + '/main/a-z.png')
        main.addDir('Latest Episodes',base_url + 'url','mode',artwork + '/main/recentlyadded.png')
        main.addDir('Search','none','mode',artwork + '/main/search.png')

def letters():
        main.addDir("#",base_url + 'url' ,'mode', artwork + '/letters/num.png')
        main.addDir("A",base_url + 'url','mode',artwork + '/letters/a.png')
        main.addDir("B",base_url + 'url','mode',artwork + '/letters/b.png')
        main.addDir("C",base_url + 'url','mode',artwork + '/letters/c.png')
        main.addDir("D",base_url + 'url','mode',artwork + '/letters/d.png')
        main.addDir("E",base_url + 'url','mode',artwork + '/letters/e.png')
        main.addDir("F",base_url + 'url','mode',artwork + '/letters/f.png')
        main.addDir("G",base_url + 'url','mode',artwork + '/letters/g.png')
        main.addDir("H",base_url + 'url','mode',artwork + '/letters/h.png')
        main.addDir("I",base_url + 'url','mode',artwork + '/letters/i.png')
        main.addDir("J",base_url + 'url','mode',artwork + '/letters/j.png')
        main.addDir("K",base_url + 'url','mode',artwork + '/letters/k.png')
        main.addDir("L",base_url + 'url','mode',artwork + '/letters/l.png')
        main.addDir("M",base_url + 'url','mode',artwork + '/letters/m.png')
        main.addDir("N",base_url + 'url','mode',artwork + '/letters/n.png')
        main.addDir("O",base_url + 'url','mode',artwork + '/letters/o.png')
        main.addDir("P",base_url + 'url','mode',artwork + '/letters/p.png')
        main.addDir("Q",base_url + 'url','mode',artwork + '/letters/q.png')
        main.addDir("R",base_url + 'url','mode',artwork + '/letters/r.png')
        main.addDir("S",base_url + 'url','mode',artwork + '/letters/s.png')
        main.addDir("T",base_url + 'url','mode',artwork + '/letters/t.png')
        main.addDir("U",base_url + 'url','mode',artwork + '/letters/u.png')
        main.addDir("V",base_url + 'url','mode',artwork + '/letters/v.png')
        main.addDir("W",base_url + 'url','mode',artwork + '/letters/w.png')
        main.addDir("X",base_url + 'url','mode',artwork + '/letters/x.png')
        main.addDir("Y",base_url + 'url','mode',artwork + '/letters/y.png')
        main.addDir("Z",base_url + 'url','mode',artwork + '/letters/z.png')
                       
def index(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title="(.+?)"><img src="(.+?)" width="130" border=".+?" height=".+?" /></a>').findall(link)

        for url,name,thumbnail in match:
                url = base_url + url
                main.addSDir(name,url,'mode','',False)
                                 
        main.AUTOVIEW('tvshows')


def indexEps(url,name):
        link = net.http_GET(url).content
        match=re.compile('<li>(.+?)<a href="(.+?)">').findall(link)
                        
        for name,url in match:
                url = base_url + url
                try:
                        main.addEDir(name,url,'mode','','')
                except:
                        continue

        main.AUTOVIEW('episodes')

def videoLinks(url,name):
        link = net.http_GET(url).content
        match=re.compile('<a target="_blank" id="hovered" href="(.+?)">.+?</a>').findall(link)
        for url in match:
                if main.resolvable(url):
                        try:
                                main.addHDir(name,url,'resolve','')
                        except:
                                continue
       
         
def search():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '/?s=' + search + '&search='
                print url
                
                INDEX(url)


                


