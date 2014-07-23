#ZMovie Module by o9r1sh October 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

net = main.net
artwork = main.artwork
base_url = 'http://www2.zmovie.tw'
settings = main.settings

def CATEGORIES():
        main.addDir('New Releases',base_url + '/movies/new','zmovieIndex',artwork + '/main/newreleases.png')
        main.addDir('Featured',base_url + '/movies/featured','zmovieIndex',artwork + '/main/featured.png')
        main.addDir('Recently Added',base_url + '/movies/recent','zmovieIndex',artwork + '/main/recentlyadded.png')
        main.addDir('A-Z','none','zmovieLetters',artwork + '/main/a-z.png')
        main.addDir('Genres','none','zmovieGenres',artwork + '/main/genres.png')

def LETTERS():
        main.addDir('#',base_url + '/search/alpha/0-9','zmovieIndex',artwork + '/letters/num.png')
        main.addDir('A',base_url + '/search/alpha/A','zmovieIndex',artwork + '/letters/a.png')
        main.addDir('B',base_url + '/search/alpha/B','zmovieIndex',artwork + '/letters/b.png')
        main.addDir('C',base_url + '/search/alpha/C','zmovieIndex',artwork + '/letters/c.png')
        main.addDir('D',base_url + '/search/alpha/D','zmovieIndex',artwork + '/letters/d.png')
        main.addDir('E',base_url + '/search/alpha/E','zmovieIndex',artwork + '/letters/e.png')
        main.addDir('F',base_url + '/search/alpha/F','zmovieIndex',artwork + '/letters/f.png')
        main.addDir('G',base_url + '/search/alpha/G','zmovieIndex',artwork + '/letters/g.png')
        main.addDir('H',base_url + '/search/alpha/H','zmovieIndex',artwork + '/letters/h.png')
        main.addDir('I',base_url + '/search/alpha/I','zmovieIndex',artwork + '/letters/i.png')
        main.addDir('J',base_url + '/search/alpha/J','zmovieIndex',artwork + '/letters/j.png')
        main.addDir('K',base_url + '/search/alpha/K','zmovieIndex',artwork + '/letters/k.png')
        main.addDir('L',base_url + '/search/alpha/L','zmovieIndex',artwork + '/letters/l.png')
        main.addDir('M',base_url + '/search/alpha/M','zmovieIndex',artwork + '/letters/m.png')
        main.addDir('N',base_url + '/search/alpha/N','zmovieIndex',artwork + '/letters/n.png')
        main.addDir('O',base_url + '/search/alpha/O','zmovieIndex',artwork + '/letters/o.png')
        main.addDir('P',base_url + '/search/alpha/P','zmovieIndex',artwork + '/letters/p.png')
        main.addDir('Q',base_url + '/search/alpha/Q','zmovieIndex',artwork + '/letters/q.png')
        main.addDir('R',base_url + '/search/alpha/R','zmovieIndex',artwork + '/letters/r.png')
        main.addDir('S',base_url + '/search/alpha/S','zmovieIndex',artwork + '/letters/s.png')
        main.addDir('T',base_url + '/search/alpha/T','zmovieIndex',artwork + '/letters/t.png')
        main.addDir('U',base_url + '/search/alpha/U','zmovieIndex',artwork + '/letters/u.png')
        main.addDir('V',base_url + '/search/alpha/V','zmovieIndex',artwork + '/letters/v.png')
        main.addDir('W',base_url + '/search/alpha/W','zmovieIndex',artwork + '/letters/w.png')
        main.addDir('X',base_url + '/search/alpha/X','zmovieIndex',artwork + '/letters/x.png')
        main.addDir('Y',base_url + '/search/alpha/Y','zmovieIndex',artwork + '/letters/y.png')
        main.addDir('Z',base_url + '/search/alpha/Z','zmovieIndex',artwork + '/letters/z.png')

def GENRES():
        main.addDir('Action',base_url + '/search/genre/Action','zmovieIndex',artwork + '/genres/action.png')
        main.addDir('Adventure',base_url + '/search/genre/Adventure','zmovieIndex',artwork + '/genres/adventure.png')
        main.addDir('Animation',base_url + '/search/genre/Animation','zmovieIndex',artwork + '/genres/animation.png')
        main.addDir('Biography',base_url + '/search/genre/Biography','zmovieIndex',artwork + '/genres/biography.png')
        main.addDir('Comedy',base_url + '/search/genre/Comedy','zmovieIndex',artwork + '/genres/comedy.png')
        main.addDir('Crime',base_url + '/search/genre/Crime','zmovieIndex',artwork + '/genres/crime.png')
        main.addDir('Documentary',base_url + '/search/genre/Documentary','zmovieIndex',artwork + '/genres/docs.png')
        main.addDir('Drama',base_url + '/search/genre/Drama','zmovieIndex',artwork + '/genres/drama.png')
        main.addDir('Family',base_url + '/search/genre/Family','zmovieIndex',artwork + '/genres/family.png')
        main.addDir('Fantasy',base_url + '/search/genre/Fantasy','zmovieIndex',artwork + '/genres/fantasy.png')
        main.addDir('Film-Noir',base_url + '/search/genre/Film-Noir','zmovieIndex',artwork + '/genres/film-noir.png')
        main.addDir('History',base_url + '/search/genre/History','zmovieIndex',artwork + '/genres/history.png')
        main.addDir('Hindi',base_url + '/search/genre/Hindi','zmovieIndex',artwork + '/genres/hindi.png')
        main.addDir('Horror',base_url + '/search/genre/Horror','zmovieIndex',artwork + '/genres/horror.png')
        main.addDir('Korean',base_url + '/search/genre/Korean','zmovieIndex',artwork + '/genres/korean.png')
        main.addDir('Music',base_url + '/search/genre/Music','zmovieIndex',artwork + '/genres/music.png')
        main.addDir('Musical',base_url + '/search/genre/Musical','zmovieIndex',artwork + '/genres/musical.png')
        main.addDir('Mystery',base_url + '/search/genre/Mystery','zmovieIndex',artwork + '/genres/mystery.png')
        main.addDir('News',base_url + '/search/genre/News','zmovieIndex',artwork + '/genres/news.png')
        main.addDir('Reality',base_url + '/search/genre/Reality%20TV','zmovieIndex',artwork + '/genres/reality.png')
        main.addDir('Romance',base_url + '/search/genre/Romance','zmovieIndex',artwork + '/genres/romance.png')
        main.addDir('Sci-Fi',base_url + '/search/genre/Sci-Fi','zmovieIndex',artwork + '/genres/sci-fi.png')
        main.addDir('Short',base_url + '/search/genre/Short','zmovieIndex',artwork + '/genres/short.png')
        main.addDir('Sport',base_url + '/search/genre/Sport','zmovieIndex',artwork + '/genres/sport.png')
        main.addDir('Talk Show',base_url + '/search/genre/Talk%20Show','zmovieIndex',artwork + '/genres/talk.png')
        main.addDir('Thriller',base_url + '/search/genre/Thriller','zmovieIndex',artwork + '/genres/thriller.png')
        main.addDir('War',base_url + '/search/genre/War','zmovieIndex',artwork + '/genres/war.png')
        main.addDir('Western',base_url + '/search/genre/Western','zmovieIndex',artwork + '/genres/western.png')

def INDEX(url):
        next_page = ''
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title="(.+?)"> <img src="(.+?)"  alt=".+?" height=".+?" width=".+?"/></a>').findall(link)
        np=re.compile("..</span> <a class=.+? href='(.+?)'> Next+").findall(link)
        if len(np) > 0:
                next_page = np[0]
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'zmovieIndex',artwork + '/main/next.png')
                                              
        for url,name,thumbnail in match:
                head, sep, tail = name.partition(')')
                name = head[:-5]
                year = head[-5:] + sep
                try:
                        main.addMDir(name,url,'zmovieVideoLinks',thumbnail,year,False)
                except:

                        continue
        if len(np) > 0:        
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'zmovieIndex',artwork + '/main/next.png')

        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        match=re.compile('class="atest" target="_blank"   href="(.+?)">').findall(link)
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
                
                url = base_url + 'index.php?s=' + search 
                
                INDEX(url)

