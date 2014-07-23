#Cartoon Freak Module by o9r1sh October 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

net = main.net

artwork = main.artwork
base_url = 'http://www.cartoonfreak.net'
settings = main.settings

def CARTOONS():
        INDEX(base_url + '/cartoon/')

def ANIME():
        main.addDir('Anime Series','none','cartoonFreakAnimeSeries',artwork + '/main/tv.png')
        main.addDir('Anime Movies','none','cartoonFreakAnimeMovies',artwork + '/main/movie.png')

def ANIMESERIES():
        main.addDir('All', base_url + '/anime/','cartoonFreakIndex',artwork + '/main/all.png')
        main.addDir('A', base_url + '/anime/?alpha=a','cartoonFreakIndex',artwork + '/letters/a.png')
        main.addDir('B', base_url + '/anime/?alpha=b','cartoonFreakIndex',artwork + '/letters/b.png')
        main.addDir('C', base_url + '/anime/?alpha=c','cartoonFreakIndex',artwork + '/letters/c.png')
        main.addDir('D', base_url + '/anime/?alpha=d','cartoonFreakIndex',artwork + '/letters/d.png')
        main.addDir('E', base_url + '/anime/?alpha=e','cartoonFreakIndex',artwork + '/letters/e.png')
        main.addDir('F', base_url + '/anime/?alpha=f','cartoonFreakIndex',artwork + '/letters/f.png')
        main.addDir('G', base_url + '/anime/?alpha=g','cartoonFreakIndex',artwork + '/letters/g.png')
        main.addDir('H', base_url + '/anime/?alpha=h','cartoonFreakIndex',artwork + '/letters/h.png')
        main.addDir('I', base_url + '/anime/?alpha=i','cartoonFreakIndex',artwork + '/letters/i.png')
        main.addDir('J', base_url + '/anime/?alpha=j','cartoonFreakIndex',artwork + '/letters/j.png')
        main.addDir('K', base_url + '/anime/?alpha=k','cartoonFreakIndex',artwork + '/letters/k.png')
        main.addDir('L', base_url + '/anime/?alpha=l','cartoonFreakIndex',artwork + '/letters/l.png')
        main.addDir('M', base_url + '/anime/?alpha=m','cartoonFreakIndex',artwork + '/letters/m.png')
        main.addDir('N', base_url + '/anime/?alpha=n','cartoonFreakIndex',artwork + '/letters/n.png')
        main.addDir('O', base_url + '/anime/?alpha=o','cartoonFreakIndex',artwork + '/letters/o.png')
        main.addDir('P', base_url + '/anime/?alpha=p','cartoonFreakIndex',artwork + '/letters/p.png')
        main.addDir('Q', base_url + '/anime/?alpha=q','cartoonFreakIndex',artwork + '/letters/q.png')
        main.addDir('R', base_url + '/anime/?alpha=r','cartoonFreakIndex',artwork + '/letters/r.png')
        main.addDir('S', base_url + '/anime/?alpha=s','cartoonFreakIndex',artwork + '/letters/s.png')
        main.addDir('T', base_url + '/anime/?alpha=t','cartoonFreakIndex',artwork + '/letters/t.png')
        main.addDir('U', base_url + '/anime/?alpha=u','cartoonFreakIndex',artwork + '/letters/u.png')
        main.addDir('V', base_url + '/anime/?alpha=v','cartoonFreakIndex',artwork + '/letters/v.png')
        main.addDir('W', base_url + '/anime/?alpha=w','cartoonFreakIndex',artwork + '/letters/w.png')
        main.addDir('X', base_url + '/anime/?alpha=x','cartoonFreakIndex',artwork + '/letters/x.png')
        main.addDir('Y', base_url + '/anime/?alpha=y','cartoonFreakIndex',artwork + '/letters/y.png')
        main.addDir('Z', base_url + '/anime/?alpha=z','cartoonFreakIndex',artwork + '/letters/z.png')

def ANIMEMOVIES():
        main.addDir('All', base_url + '/movie/','cartoonFreakMovieIndex',artwork + '/main/a.png')
        main.addDir('A', base_url + '/movie/?alpha=a','cartoonFreakMovieIndex',artwork + '/letters/a.png')
        main.addDir('B', base_url + '/movie/?alpha=b','cartoonFreakMovieIndex',artwork + '/letters/b.png')
        main.addDir('C', base_url + '/movie/?alpha=c','cartoonFreakMovieIndex',artwork + '/letters/c.png')
        main.addDir('D', base_url + '/movie/?alpha=d','cartoonFreakMovieIndex',artwork + '/letters/d.png')
        main.addDir('E', base_url + '/movie/?alpha=e','cartoonFreakMovieIndex',artwork + '/letters/e.png')
        main.addDir('F', base_url + '/movie/?alpha=f','cartoonFreakMovieIndex',artwork + '/letters/f.png')
        main.addDir('G', base_url + '/movie/?alpha=g','cartoonFreakMovieIndex',artwork + '/letters/g.png')
        main.addDir('H', base_url + '/movie/?alpha=h','cartoonFreakMovieIndex',artwork + '/letters/h.png')
        main.addDir('I', base_url + '/movie/?alpha=i','cartoonFreakMovieIndex',artwork + '/letters/i.png')
        main.addDir('J', base_url + '/movie/?alpha=j','cartoonFreakMovieIndex',artwork + '/letters/j.png')
        main.addDir('K', base_url + '/movie/?alpha=k','cartoonFreakMovieIndex',artwork + '/letters/k.png')
        main.addDir('L', base_url + '/movie/?alpha=l','cartoonFreakMovieIndex',artwork + '/letters/l.png')
        main.addDir('M', base_url + '/movie/?alpha=m','cartoonFreakMovieIndex',artwork + '/letters/m.png')
        main.addDir('N', base_url + '/movie/?alpha=n','cartoonFreakMovieIndex',artwork + '/letters/n.png')
        main.addDir('O', base_url + '/movie/?alpha=o','cartoonFreakMovieIndex',artwork + '/letters/o.png')
        main.addDir('P', base_url + '/movie/?alpha=p','cartoonFreakMovieIndex',artwork + '/letters/p.png')
        main.addDir('Q', base_url + '/movie/?alpha=q','cartoonFreakMovieIndex',artwork + '/letters/q.png')
        main.addDir('R', base_url + '/movie/?alpha=r','cartoonFreakMovieIndex',artwork + '/letters/r.png')
        main.addDir('S', base_url + '/movie/?alpha=s','cartoonFreakMovieIndex',artwork + '/letters/s.png')
        main.addDir('T', base_url + '/movie/?alpha=t','cartoonFreakMovieIndex',artwork + '/letters/t.png')
        main.addDir('U', base_url + '/movie/?alpha=u','cartoonFreakMovieIndex',artwork + '/letters/u.png')
        main.addDir('V', base_url + '/movie/?alpha=v','cartoonFreakMovieIndex',artwork + '/letters/v.png')
        main.addDir('W', base_url + '/movie/?alpha=w','cartoonFreakMovieIndex',artwork + '/letters/w.png')
        main.addDir('X', base_url + '/movie/?alpha=x','cartoonFreakMovieIndex',artwork + '/letters/x.png')
        main.addDir('Y', base_url + '/movie/?alpha=y','cartoonFreakMovieIndex',artwork + '/letters/y.png')
        main.addDir('Z', base_url + '/movie/?alpha=Z','cartoonFreakMovieIndex',artwork + '/letters/z.png')
    
def INDEX(url):
        o_url = url
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" class=".+?"><img data-src=".+?" src="(.+?)" class="primary"/><span class="play"></span><span class=".+?">(.+?)</span>').findall(link)
        np=re.compile('<a class="pagination-next btn btn-inverse" href="(.+?)">').findall(link)
        if len(np) > 0:
                if settings.getSetting('nextpagetop') == 'true':
                        np_url = np[0]
                        next_page = base_url + np_url
                        next_page = next_page.replace('&#038;','&')
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'cartoonFreakIndex',artwork + '/main/next.png')
        for url,thumbnail,name in match:
                if 'anime' in o_url:       
                        try:
                                main.addAnimeDir(name,url,'cartoonFreakAnimeEpisodes',thumbnail,False)
                        except:
                                continue
                else:  
                        try:
                                main.addToonDir(name,url,'cartoonFreakEpisodes',thumbnail,False)
                        except:
                                continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        np_url = np[0]
                        next_page = base_url + np_url
                        next_page = next_page.replace('&#038;','&')
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'cartoonFreakIndex',artwork + '/main/next.png')
 
                
        main.AUTOVIEW('tvshows')

def MOVIEINDEX(url):
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" class=".+?"><img data-src=".+?" src="(.+?)" class="primary"/><span class="play"></span><span class=".+?">(.+?)</span>').findall(link)
        np=re.compile('<a class="pagination-next btn btn-inverse" href="(.+?)">').findall(link)
        if len(np) > 0:
                np_url = np[0]
                next_page = base_url + np_url
                next_page = next_page.replace('&#038;','&')
                main.addDir('Next Page',next_page,'cartoonFreakMovieIndex',artwork + '/main/next.png')
        for url,thumbnail,name in match:
                try:
                        main.addMDir(name,url,'cartoonFreakMovieEpisodes',thumbnail,'',False)
                except:
                        continue
                
        main.AUTOVIEW('movies')

def MOVIEEPISODES(url,thumb):
        link = net.http_GET(url).content
        match=re.compile('<li class=".+?"><a href="(.+?)"><i class="icon-chevron-right"></i>(.+?)</a></li>').findall(link)
        for url, name in match:
                VIDEOLINKS(name,url,thumb)
        main.AUTOVIEW('movies')           

def EPISODES(url):
        link = net.http_GET(url).content
        match=re.compile('<li class=".+?"><a href="(.+?)"><i class="icon-chevron-right"></i>(.+?)</a></li>').findall(link)
        for url, name in match:
                if 'Season' in name:
                        name = re.sub(' Episode ','x',name)
                show,sep,numbers = name.partition('Season')
                name = show + '' + numbers
                try:
                        main.addEDir(name,url,'cartoonFreakVideoLinks','',show)
                except:
                        continue
        main.AUTOVIEW('episodes')

def ANIMEEPISODES(url,thumb):
        link = net.http_GET(url).content
        match=re.compile('<li class=".+?"><a href="(.+?)"><i class="icon-chevron-right"></i>(.+?)</a></li>').findall(link)
        for url, name in match:
                try:
                        main.addEDir(name,url,'cartoonFreakVideoLinks',thumb,'')
                except:
                        continue
        main.AUTOVIEW('episodes')
        
def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        match=re.compile('<iframe src="(.+?)" width=".+?" height=".+?" scrolling=".+?" frameborder=".+?"></iframe>').findall(link)
        for url in match:
                if url == '/300x250.html':
                        continue
                else:
                        try:       
                                try:
                                        if main.resolvable(url):
                                                main.addHDir(name,url,'resolve','')
                                except:
                                        continue
                        except:
                                continue
                        


