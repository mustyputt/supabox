#WeWatchMoviesFree Module by o9r1sh October 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

net = main.net
artwork = main.artwork
base_url = 'http://www.wewatchmoviesfree.net/'
settings = main.settings

def CATEGORIES():
        main.addDir('Recently Added',base_url,'wwmfIndex',artwork + '/main/recentlyadded.png')
        main.addDir('A-Z','none','wwmfLetters',artwork + '/main/a-z.png')
        main.addDir('Genres','none','wwmfGenres',artwork + '/main/genres.png')
        main.addDir('Search','none','wwmfSearch',artwork + '/main/search.png')

def LETTERS():
        main.addDir('A',base_url + '/category/a','wwmfIndex',artwork + '/letters/a.png')
        main.addDir('B',base_url + '/category/b','wwmfIndex',artwork + '/letters/b.png')
        main.addDir('C',base_url + '/category/c','wwmfIndex',artwork + '/letters/c.png')
        main.addDir('D',base_url + '/category/d','wwmfIndex',artwork + '/letters/d.png')
        main.addDir('E',base_url + '/category/e','wwmfIndex',artwork + '/letters/e.png')
        main.addDir('F',base_url + '/category/f','wwmfIndex',artwork + '/letters/f.png')
        main.addDir('G',base_url + '/category/g','wwmfIndex',artwork + '/letters/g.png')
        main.addDir('H',base_url + '/category/h','wwmfIndex',artwork + '/letters/h.png')
        main.addDir('I',base_url + '/category/i','wwmfIndex',artwork + '/letters/i.png')
        main.addDir('J',base_url + '/category/j','wwmfIndex',artwork + '/letters/j.png')
        main.addDir('K',base_url + '/category/k','wwmfIndex',artwork + '/letters/k.png')
        main.addDir('L',base_url + '/category/l','wwmfIndex',artwork + '/letters/l.png')
        main.addDir('M',base_url + '/category/m','wwmfIndex',artwork + '/letters/m.png')
        main.addDir('N',base_url + '/category/n','wwmfIndex',artwork + '/letters/n.png')
        main.addDir('O',base_url + '/category/o','wwmfIndex',artwork + '/letters/o.png')
        main.addDir('P',base_url + '/category/p','wwmfIndex',artwork + '/letters/p.png')
        main.addDir('Q',base_url + '/category/q','wwmfIndex',artwork + '/letters/q.png')
        main.addDir('R',base_url + '/category/r','wwmfIndex',artwork + '/letters/r.png')
        main.addDir('S',base_url + '/category/s','wwmfIndex',artwork + '/letters/s.png')
        main.addDir('T',base_url + '/category/t','wwmfIndex',artwork + '/letters/t.png')
        main.addDir('U',base_url + '/category/u','wwmfIndex',artwork + '/letters/u.png')
        main.addDir('V',base_url + '/category/v','wwmfIndex',artwork + '/letters/v.png')
        main.addDir('W',base_url + '/category/w','wwmfIndex',artwork + '/letters/w.png')
        main.addDir('X',base_url + '/category/x','wwmfIndex',artwork + '/letters/x.png')
        main.addDir('Y',base_url + '/category/y','wwmfIndex',artwork + '/letters/y.png')
        main.addDir('Z',base_url + '/category/z','wwmfIndex',artwork + '/letters/z.png')

def GENRES():
        main.addDir('Action',base_url + '/category/action','wwmfIndex',artwork + '/genres/action.png')
        main.addDir('Adventure',base_url + '/category/adventure','wwmfIndex',artwork + '/genres/adventure.png')
        main.addDir('Animation',base_url + '/category/animation','wwmfIndex',artwork + '/genres/animation.png')
        main.addDir('Biography',base_url + '/category/biography','wwmfIndex',artwork + '/genres/biography.png')
        main.addDir('Bollywood',base_url + '/category/bollywood','wwmfIndex',artwork + '/genres/bollywood.png')
        main.addDir('Comedy',base_url + '/category/comedy','wwmfIndex',artwork + '/genres/comedy.png')
        main.addDir('Crime',base_url + '/category/crime','wwmfIndex',artwork + '/genres/crime.png')
        main.addDir('Documentary',base_url + '/category/documentary','wwmfIndex',artwork + '/genres/docs.png')
        main.addDir('Drama',base_url + '/category/drama','wwmfIndex',artwork + '/genres/drama.png')
        main.addDir('Family',base_url + '/category/family','wwmfIndex',artwork + '/genres/family.png')
        main.addDir('Fantasy',base_url + '/category/fantasy','wwmfIndex',artwork + '/genres/fantasy.png')
        main.addDir('Film-Noir',base_url + '/category/general','wwmfIndex',artwork + '/genres/film-noir.png')
        main.addDir('History',base_url + '/category/history','wwmfIndex',artwork + '/genres/history.png')
        main.addDir('Horror',base_url + '/category/horror','wwmfIndex',artwork + '/genres/horror.png')
        main.addDir('Musical',base_url + '/category/musical','wwmfIndex',artwork + '/genres/musical.png')
        main.addDir('Mystery',base_url + '/category/mystery','wwmfIndex',artwork + '/genres/mystery.png')
        main.addDir('Reality TV',base_url + '/category/reality-tv','wwmfIndex',artwork + '/genres/reality.png')
        main.addDir('Romance',base_url + '/category/romance','wwmfIndex',artwork + '/genres/romance.png')
        main.addDir('Sci-Fi',base_url + '/category/sci-fi','wwmfIndex',artwork + '/genres/sci-fi.png')
        main.addDir('Short',base_url + '/category/short','wwmfIndex',artwork + '/genres/short.png')
        main.addDir('Sports',base_url + '/category/sport','wwmfIndex',artwork + '/genres/sport.png')
        main.addDir('Thriller',base_url + '/category/thriller','wwmfIndex',artwork + '/genres/thriller.png')
        main.addDir('War',base_url + '/category/war','wwmfIndex',artwork + '/genres/war.png')
        main.addDir('Western',base_url + '/category/western','wwmfIndex',artwork + '/genres/western.png')

def INDEX(url):
        link = net.http_GET(url).content
        match=re.compile('<a\nhref="(.+?)" rel=".+?" > <img\nclass=".+?" src="(.+?)" width=".+?" height=".+?" title="Watch (.+?) Online Free" >').findall(link)
        np=re.compile("rel='next' href='(.+?)' /><link").findall(link)
        if len(np) > 0:
                next_page = np[0]
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'wwmfIndex',artwork + '/main/next.png')
        
        for url,thumbnail,name in match:
                try:
                        main.addMDir(name,url,'wwmfVideoLinks',thumbnail,'',False)
                        print year
                except:
                        continue

        if len(np) > 0:
                next_page = np[0]
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'wwmfIndex',artwork + '/main/next.png')

        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        match=re.compile('<a\nhref="(.+?)" class="ext-link"').findall(link)
        for url in match:
                head,sep,tail = url.partition('=')
                if main.resolvable(tail):
                        try:
                                main.addHDir(name,tail,'resolve','')
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
                
                INDEX(url)

def MASTERSEARCH(search):
        url = base_url + '/?s=' + search 
        INDEX(url)

