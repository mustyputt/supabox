#ChannelCut Module by o9r1sh September 2013

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os
import urlresolver

net = main.net

artwork = main.artwork
base_url = 'http://www.channelcut.me'

settings = main.settings

def CATEGORIES():
        main.addDir('Latest Episodes',base_url + '/last-150','channelCutRecentEpisodes',artwork + '/main/recentlyadded.png')
        main.addDir('TV Shows A-Z','none','channelCutLetters',artwork + '/main/a-z.png')
        main.addDir('Search','none','channelCutSearch',artwork + '/main/search.png')

def LETTERS():
        main.addDir('#','none','channelCutNum',artwork + '/letters/num.png')
        main.addDir('A','none','channelCutA',artwork + '/letters/a.png')
        main.addDir('B','none','channelCutB',artwork + '/letters/b.png')
        main.addDir('C','none','channelCutC',artwork + '/letters/c.png')
        main.addDir('D','none','channelCutD',artwork + '/letters/d.png')
        main.addDir('E','none','channelCutE',artwork + '/letters/e.png')
        main.addDir('F','none','channelCutF',artwork + '/letters/f.png')
        main.addDir('G','none','channelCutG',artwork + '/letters/g.png')
        main.addDir('H','none','channelCutH',artwork + '/letters/h.png')
        main.addDir('I','none','channelCutI',artwork + '/letters/i.png')
        main.addDir('J','none','channelCutJ',artwork + '/letters/j.png')
        main.addDir('K','none','channelCutK',artwork + '/letters/k.png')
        main.addDir('L','none','channelCutL',artwork + '/letters/l.png')
        main.addDir('M','none','channelCutM',artwork + '/letters/m.png')
        main.addDir('N','none','channelCutN',artwork + '/letters/n.png')
        main.addDir('O','none','channelCutO',artwork + '/letters/o.png')
        main.addDir('P','none','channelCutP',artwork + '/letters/p.png')
        main.addDir('Q','none','channelCutQ',artwork + '/letters/q.png')
        main.addDir('R','none','channelCutR',artwork + '/letters/r.png')
        main.addDir('S','none','channelCutS',artwork + '/letters/s.png')
        main.addDir('T','none','channelCutT',artwork + '/letters/t.png')
        main.addDir('U','none','channelCutU',artwork + '/letters/u.png')
        main.addDir('V','none','channelCutV',artwork + '/letters/v.png')
        main.addDir('W','none','channelCutW',artwork + '/letters/w.png')
        main.addDir('X','none','channelCutX',artwork + '/letters/x.png')
        main.addDir('Y','none','channelCutY',artwork + '/letters/y.png')
        main.addDir('Z','none','channelCutZ',artwork + '/letters/z.png')

def NUM():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]).isdigit():
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def A():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'A':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def B():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'B':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def C():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'C':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def D():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'D':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def E():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'E':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def F():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'F':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def G():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'G':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def H():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'H':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def I():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'I':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def J():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'K':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def K():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'K':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def L():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'L':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def M():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'M':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def N():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'N':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def O():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'O':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def P():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'P':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def Q():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'Q':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')        

def R():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'R':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def S():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'S':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def T():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'T':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def U():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'U':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def V():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'V':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def W():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'W':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def X():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'X':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','')
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def Y():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link,False)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'Y':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def Z():
        url = base_url
        link = net.http_GET(url).content
        match=re.compile('<option class=".+?" value=".+?">(.+?)</option>').findall(link)
        for name in match:
                name = re.sub(' ', '-', name)
                url = base_url +'/category/' + name
                name = re.sub('-', ' ', name)
                if str(name[0]) == 'Z':
                        try:
                                main.addSDir(name,url,'channelCutEpisodes','',False)
                        except:
                               continue
        main.AUTOVIEW('tvshows')

def EPISODES(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a>').findall(link)
        np=re.compile('<span class="prev"><a href="(.+?)" >Previous Posts</a>').findall(link)
        if len(np) > 0:
                if settings.getSetting('nextpagetop') == 'true':
                        next_page = str(np[0])
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'channelCutEpisodes',artwork + 'main/next.png')
        for url, name in match:
                name = re.sub(' Episode ','x',name)
                show,sep,numbers = name.partition('Season')
                name = show + '' + numbers
                name = name.replace("&#8217;","")
                try:
                        main.addEDir(name,url,'channelCutVideoLinks','',show)
                except:
                        continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        next_page = str(np[0])
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'channelCutEpisodes',artwork + 'main/next.png')

        main.AUTOVIEW('episodes')

def RECENTEPISODES(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)">(.+?)</a> </li>').findall(link)
        for url, name in match:
                name = re.sub(' Episode ','x',name)
                show,sep,numbers = name.partition('Season')
                name = show + '' + numbers
                name = name.replace("&#8217;","")
                try:
                        main.addEDir(name,url,'channelCutVideoLinks','',show)
                except:
                        continue
        main.AUTOVIEW('episodes')

def VIDEOLINKS(name,url):
        link = net.http_GET(url).content
        match=re.compile('<a href=".+?" rel="nofollow">(.+)</a>').findall(link)
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
                
                url = base_url + '/?s=' + search + '&searchsubmit=Search'
                
                EPISODES(url)

def MASTERSEARCH(search):
                url = base_url + '/?s=' + search + '&searchsubmit=Search'
                EPISODES(url)

