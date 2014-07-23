#GoGO Anime module by o9r1sh
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,main,urlresolver,xbmc,os

net = main.net

artwork = main.artwork
base_url = 'http://www.gogoanime.com'
settings = main.settings

def CATEGORIES():
        main.addDir('A-Z','none','gogoAnimeLetters',artwork + '/main/a-z.png')
        main.addDir('New Series',base_url + '/category/new-release','gogoAnimeRecentIndex',artwork + '/main/recentlyadded.png')
        #main.addDir('Search','none','gogoAnimeSearch',artwork + '/main/search.png')


def LETTERS():
        main.addDir('#',base_url + '/free-anime-list','gogoAnimeNum',artwork + '/letters/num.png')
        main.addDir('A',base_url + '/free-anime-list','gogoAnimeA',artwork + '/letters/a.png')
        main.addDir('B',base_url + '/free-anime-list','gogoAnimeB',artwork + '/letters/b.png')
        main.addDir('C',base_url + '/free-anime-list','gogoAnimeC',artwork + '/letters/c.png')
        main.addDir('D',base_url + '/free-anime-list','gogoAnimeD',artwork + '/letters/d.png')
        main.addDir('E',base_url + '/free-anime-list','gogoAnimeE',artwork + '/letters/e.png')
        main.addDir('F',base_url + '/free-anime-list','gogoAnimeF',artwork + '/letters/f.png')
        main.addDir('G',base_url + '/free-anime-list','gogoAnimeG',artwork + '/letters/g.png')
        main.addDir('H',base_url + '/free-anime-list','gogoAnimeH',artwork + '/letters/h.png')
        main.addDir('I',base_url + '/free-anime-list','gogoAnimeI',artwork + '/letters/i.png')
        main.addDir('J',base_url + '/free-anime-list','gogoAnimeJ',artwork + '/letters/j.png')
        main.addDir('K',base_url + '/free-anime-list','gogoAnimeK',artwork + '/letters/k.png')
        main.addDir('L',base_url + '/free-anime-list','gogoAnimeL',artwork + '/letters/l.png')
        main.addDir('M',base_url + '/free-anime-list','gogoAnimeM',artwork + '/letters/m.png')
        main.addDir('N',base_url + '/free-anime-list','gogoAnimeN',artwork + '/letters/n.png')
        main.addDir('O',base_url + '/free-anime-list','gogoAnimeO',artwork + '/letters/o.png')
        main.addDir('P',base_url + '/free-anime-list','gogoAnimeP',artwork + '/letters/p.png')
        main.addDir('Q',base_url + '/free-anime-list','gogoAnimeQ',artwork + '/letters/q.png')
        main.addDir('R',base_url + '/free-anime-list','gogoAnimeR',artwork + '/letters/r.png')
        main.addDir('S',base_url + '/free-anime-list','gogoAnimeS',artwork + '/letters/s.png')
        main.addDir('T',base_url + '/free-anime-list','gogoAnimeT',artwork + '/letters/t.png')
        main.addDir('U',base_url + '/free-anime-list','gogoAnimeU',artwork + '/letters/u.png')
        main.addDir('V',base_url + '/free-anime-list','gogoAnimeV',artwork + '/letters/v.png')
        main.addDir('W',base_url + '/free-anime-list','gogoAnimeW',artwork + '/letters/w.png')
        main.addDir('X',base_url + '/free-anime-list','gogoAnimeX',artwork + '/letters/x.png')
        main.addDir('Y',base_url + '/free-anime-list','gogoAnimeY',artwork + '/letters/y.png')
        main.addDir('Z',base_url + '/free-anime-list','gogoAnimeZ',artwork + '/letters/z.png')

def NUM(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                chars = set('0123456789$.')
                if any((c in chars) for c in name[0]):
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def A(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'A':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def B(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'B':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def C(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'C':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def D(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'D':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def E(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'E':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def F(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'F':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def G(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'G':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def H(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'H':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def I(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'I':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def J(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'J':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def K(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'K':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def L(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'L':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def M(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'M':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def N(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'N':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def O(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'O':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def P(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'P':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def Q(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'Q':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def R(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'R':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def S(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'S':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def T(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'T':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def U(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'U':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def V(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'V':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def W(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'W':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def X(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'X':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def Y(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'Y':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def Z(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="http://www.gogoanime.com/category/(.+?)" title=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = base_url + '/category/' +  url
                if name[0] == 'Z':
                        try:
                                main.addAnimeDir(name, url,'gogoAnimeEpisodes','',False)
                        except:
                                continue
        main.AUTOVIEW('tvshows')

def RECENTINDEX(url):
        next_page = ''
        link = net.http_GET(url).content
        np=re.compile('<span class="current">.+?</span><a href="(.+?)" class=".+?" title=".+?">.+?</a>').findall(link)
        match=re.compile('<a href="(.+?)" title="(.+?)" ><img src="(.+?)" width=".+?" height=".+?" /></a>').findall(link)
        if len(np) > 0:
                next_page = np[0]
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'gogoAnimeRecentIndex',artwork + '/main/next.png')
        for url, name, thumbnail in match:
                if "<span>" not in name:
                        url = base_url + '/category/' +  url
                        try:
                                main.addAnimeDir(name,url,'gogoAnimeEpisodes',thumbnail,False)
                        except:
                                continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'gogoAnimeRecentIndex',artwork + '/main/next.png')

        main.AUTOVIEW('tvshows')

def INDEXEPS(url,name):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" rel="(.+?)" title=".+?">(.+?)</a>').findall(link)
                        
        for url,thumbnail,name in match:
                try:
                        main.addEDir(name,url,'gogoAnimeVideoLinks','','')
                except:
                        continue

        main.AUTOVIEW('episodes')

def VIDEOLINKS(url,name,thumb):
        link = net.http_GET(url).content
        match=re.compile('<iframe src="(.+?)"').findall(link)
        for url in match:
                if main.resolvable(url):
                        try:
                                main.addHDir(name,url,'resolve','')
                        except:
                                continue
         
def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '/?s=' + search 
                print url
                
                INDEX(url)


                


