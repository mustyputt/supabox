#FreeMoviesAddict Module by o9r1sh September 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os
import urlresolver

net = main.net

artwork = main.artwork
base_url = 'http://www.freemoviesaddict.com'
settings = main.settings

def CATEGORIES():
        main.addDir('Recent Movies',base_url,'fmaIndex',artwork + '/main/recentlyadded.png')
        main.addDir('A-Z','none','fmaLetters',artwork + '/main/a-z.png')
        main.addDir('Genres','none','fmaGenres',artwork + '/main/genres.png')
        main.addDir('Years','none','fmaYears',artwork + '/main/years.png')

def LETTERS():
        main.addDir('#',base_url + '/movies/letter/123','fmaIndex',artwork + '/letters/num.png')
        main.addDir('A',base_url + '/movies/letter/A','fmaIndex',artwork + '/letters/a.png')
        main.addDir('B',base_url + '/movies/letter/B','fmaIndex',artwork + '/letters/b.png')
        main.addDir('C',base_url + '/movies/letter/C','fmaIndex',artwork + '/letters/c.png')
        main.addDir('D',base_url + '/movies/letter/D','fmaIndex',artwork + '/letters/d.png')
        main.addDir('E',base_url + '/movies/letter/E','fmaIndex',artwork + '/letters/e.png')
        main.addDir('F',base_url + '/movies/letter/F','fmaIndex',artwork + '/letters/f.png')
        main.addDir('G',base_url + '/movies/letter/G','fmaIndex',artwork + '/letters/g.png')
        main.addDir('H',base_url + '/movies/letter/H','fmaIndex',artwork + '/letters/h.png')
        main.addDir('I',base_url + '/movies/letter/I','fmaIndex',artwork + '/letters/i.png')
        main.addDir('J',base_url + '/movies/letter/J','fmaIndex',artwork + '/letters/j.png')
        main.addDir('K',base_url + '/movies/letter/K','fmaIndex',artwork + '/letters/k.png')
        main.addDir('L',base_url + '/movies/letter/L','fmaIndex',artwork + '/letters/l.png')
        main.addDir('M',base_url + '/movies/letter/M','fmaIndex',artwork + '/letters/m.png')
        main.addDir('N',base_url + '/movies/letter/N','fmaIndex',artwork + '/letters/n.png')
        main.addDir('O',base_url + '/movies/letter/O','fmaIndex',artwork + '/letters/o.png')
        main.addDir('P',base_url + '/movies/letter/P','fmaIndex',artwork + '/letters/p.png')
        main.addDir('Q',base_url + '/movies/letter/Q','fmaIndex',artwork + '/letters/q.png')
        main.addDir('R',base_url + '/movies/letter/R','fmaIndex',artwork + '/letters/r.png')
        main.addDir('S',base_url + '/movies/letter/S','fmaIndex',artwork + '/letters/s.png')
        main.addDir('T',base_url + '/movies/letter/T','fmaIndex',artwork + '/letters/t.png')
        main.addDir('U',base_url + '/movies/letter/U','fmaIndex',artwork + '/letters/u.png')
        main.addDir('V',base_url + '/movies/letter/V','fmaIndex',artwork + '/letters/v.png')
        main.addDir('W',base_url + '/movies/letter/W','fmaIndex',artwork + '/letters/w.png')
        main.addDir('X',base_url + '/movies/letter/X','fmaIndex',artwork + '/letters/x.png')
        main.addDir('Y',base_url + '/movies/letter/Y','fmaIndex',artwork + '/letters/y.png')
        main.addDir('Z',base_url + '/movies/letter/Z','fmaIndex',artwork + '/letters/z.png')

def GENRES():
        main.addDir('Action',base_url + '/movies/genre/action','fmaIndex',artwork + '/genres/action.png')
        main.addDir('Adventure',base_url + '/movies/genre/adventure','fmaIndex',artwork + '/genres/adventure.png')
        main.addDir('Animation',base_url + '/movies/genre/animation','fmaIndex',artwork + '/genres/animation.png')
        main.addDir('Biography',base_url + '/movies/genre/biography','fmaIndex',artwork + '/genres/biography.png')
        main.addDir('Comedy',base_url + '/movies/genre/comedy','fmaIndex',artwork + '/genres/comedy.png')
        main.addDir('Crime',base_url + '/movies/genre/crime','fmaIndex',artwork + '/genres/crime.png')
        main.addDir('Documentary',base_url + '/movies/genre/documentary','fmaIndex',artwork + '/genres/docs.png')
        main.addDir('Drama',base_url + '/movies/genre/drama','fmaIndex',artwork + '/genres/drama.png')
        main.addDir('Family',base_url + '/movies/genre/family','fmaIndex',artwork + '/genres/family.png')
        main.addDir('Fantasy',base_url + '/movies/genre/fantasy','fmaIndex',artwork + '/genres/fantasy.png')
        main.addDir('Film-Noir',base_url + '/movies/genre/film-noir','fmaIndex',artwork + '/genres/film-noir.png')
        main.addDir('History',base_url + '/movies/genre/history','fmaIndex',artwork + '/genres/history.png')
        main.addDir('Horror',base_url + '/movies/genre/horror','fmaIndex',artwork + '/genres/horror.png')
        main.addDir('Music',base_url + '/movies/genre/music','fmaIndex',artwork + '/genres/music.png')
        main.addDir('Musical',base_url + '/movies/genre/musical','fmaIndex',artwork + '/genres/musical.png')
        main.addDir('Mystery',base_url + '/movies/genre/mystery','fmaIndex',artwork + '/genres/mystery.png')
        main.addDir('Romance',base_url + '/movies/genre/romance','fmaIndex',artwork + '/genres/romance.png')
        main.addDir('Sci-Fi',base_url + '/movies/genre/sci-fi','fmaIndex',artwork + '/genres/sci-fi.png')
        main.addDir('Short',base_url + '/movies/genre/short','fmaIndex',artwork + '/genres/short.png')
        main.addDir('Sport',base_url + '/movies/genre/sport','fmaIndex',artwork + '/genres/sport.png')
        main.addDir('Thriller',base_url + '/movies/genre/thriller','fmaIndex',artwork + '/genres/thriller.png')
        main.addDir('War',base_url + '/movies/genre/war','fmaIndex',artwork + '/genres/war.png')
        main.addDir('Western',base_url + '/movies/genre/western','fmaIndex',artwork + '/genres/western.png')

def YEARS():
        main.addDir('2013',base_url + '/movies/year/2013','fmaIndex',artwork + '/years/2013.png')
        main.addDir('2012',base_url + '/movies/year/2012','fmaIndex',artwork + '/years/2012.png')
        main.addDir('2011',base_url + '/movies/year/2011','fmaIndex',artwork + '/years/2011.png')
        main.addDir('2010',base_url + '/movies/year/2010','fmaIndex',artwork + '/years/2010.png')
        main.addDir('2009',base_url + '/movies/year/2009','fmaIndex',artwork + '/years/2009.png')
        main.addDir('2008',base_url + '/movies/year/2008','fmaIndex',artwork + '/years/2008.png')
        main.addDir('2007',base_url + '/movies/year/2007','fmaIndex',artwork + '/years/2007.png')
        main.addDir('2006',base_url + '/movies/year/2006','fmaIndex',artwork + '/years/2006.png')
        main.addDir('2005',base_url + '/movies/year/2005','fmaIndex',artwork + '/years/2005.png')
        main.addDir('2004',base_url + '/movies/year/2004','fmaIndex',artwork + '/years/2004.png')
        main.addDir('2003',base_url + '/movies/year/2003','fmaIndex',artwork + '/years/2003.png')
        main.addDir('2002',base_url + '/movies/year/2002','fmaIndex',artwork + '/years/2002.png')
        main.addDir('2001',base_url + '/movies/year/2001','fmaIndex',artwork + '/years/2001.png')
        main.addDir('2000',base_url + '/movies/year/2000','fmaIndex',artwork + '/years/2000.png')
        main.addDir('1999',base_url + '/movies/year/1999','fmaIndex',artwork + '/years/1999.png')
        main.addDir('1998',base_url + '/movies/year/1998','fmaIndex',artwork + '/years/1998.png')
        main.addDir('1997',base_url + '/movies/year/1997','fmaIndex',artwork + '/years/1997.png')
        main.addDir('1996',base_url + '/movies/year/1996','fmaIndex',artwork + '/years/1996.png')
        main.addDir('1995',base_url + '/movies/year/1995','fmaIndex',artwork + '/years/1995.png')
        main.addDir('1994',base_url + '/movies/year/1994','fmaIndex',artwork + '/years/1994.png')
        main.addDir('1993',base_url + '/movies/year/1993','fmaIndex',artwork + '/years/1993.png')
        main.addDir('1992',base_url + '/movies/year/1992','fmaIndex',artwork + '/years/1992.png')
        main.addDir('1991',base_url + '/movies/year/1991','fmaIndex',artwork + '/years/1991.png')
        main.addDir('1990',base_url + '/movies/year/1990','fmaIndex',artwork + '/years/1990.png')

def INDEX(url):
        next_page = ''
        link = net.http_GET(url).content
        match=re.compile('<a href=\'(.+?)\'>\r\n\t\t<img class=\'movie_img\' src=\'(.+?)\' alt=\'(.+?)\' />').findall(link)
        np=re.compile('class="pagination_next"><a class="pagination_link" href="(.+?)"></a></span>').findall(link)
        if len(np) > 0:
                np_url = np[0]
                next_page = base_url + np_url
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'fmaIndex',artwork + '/main/next.png')
        for url,thumbnail,name in match:
                url = base_url + url

                try:
                        main.addMDir(name,url,'fmaVideoLinks',thumbnail,'',False)
                except:

                        continue
        if len(np) > 0:  
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'fmaIndex',artwork + '/main/next.png')
    
                
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        match=re.compile('href="/movies/ext/(.+?)"').findall(link)
        for num in match:
                url = base_url + '/movies/ext/' + num
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                url = response.geturl()

                if url:
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
