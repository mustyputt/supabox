#TubePirate Module by o9r1sh October 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi

net = main.net
artwork = main.artwork
base_url = 'http://www.tubepirate.com'
settings = main.settings

def CATEGORIES():
        main.addDir('Latest Videos',base_url +'/videos.html','tubePirateIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Videos By Actresses','none','tubePirateActors',artwork + '/main/actresses.png')
        main.addDir('Videos By Category','none','tubePirateGenres',artwork + '/main/categories.png')
        main.addDir('Most Viewed','none','tubePirateMostViewed',artwork + '/main/mostviewed.png')
        main.addDir('Top Rated','none','tubePirateTopRated',artwork + '/main/featured.png')

def MOST_VIEWED():
        main.addDir('Today',base_url +'/videos.html?o=v1','tubePirateIndex',artwork + '/main/today.png')
        main.addDir('This Week',base_url +'/videos.html?o=v7','tubePirateIndex',artwork + '/main/thisweek.png')
        main.addDir('This Month',base_url +'/videos.html?o=30','tubePirateIndex',artwork + '/main/thismonth.png')
        main.addDir('All Time',base_url +'/videos.html?o=v','tubePirateIndex',artwork + '/main/alltime.png')

def TOP_RATED():
        main.addDir('Today',base_url +'/videos.html?o=r1','tubePirateIndex',artwork + '/main/today.png')
        main.addDir('This Week',base_url +'/videos.html?o=r7','tubePirateIndex',artwork + '/main/thisweek.png')
        main.addDir('This Month',base_url +'/videos.html?o=r30','tubePirateIndex',artwork + '/main/thismonth.png')
        main.addDir('All Time',base_url +'/videos.html?o=r','tubePirateIndex',artwork + '/main/alltime.png')

def ACTORS():
        main.addDir('By Letter','none','tubePirateLetters',artwork + '/main/a-z.png')
        main.addDir('Top Rated','none','tubePirateTopRatedActors',artwork + '/main/featured.png')
        main.addDir('Most Viewed','none','tubePirateMostViewedActors',artwork + '/main/mostviewed.png')

def TOP_RATED_ACTORS():
        main.addDir('Today',base_url +'/pornstars.html?o=r1','tubePirateMostActorIndex',artwork + '/main/today.png')
        main.addDir('This Week',base_url +'/pornstars.html?o=r7','tubePirateMostActorIndex',artwork + '/main/thisweek.png')
        main.addDir('This Month',base_url +'/pornstars.html?o=r30','tubePirateMostActorIndex',artwork + '/main/thismonth.png')
        main.addDir('All Time',base_url +'/pornstars.html?o=r','tubePirateMostActorIndex',artwork + '/main/alltime.png')

def MOST_VIEWED_ACTORS():
        main.addDir('Today',base_url +'/pornstars.html?o=v1','tubePirateMostActorIndex',artwork + '/main/today.png')
        main.addDir('This Week',base_url +'/pornstars.html','tubePirateMostActorIndex',artwork + '/main/thisweek.png')
        main.addDir('This Month',base_url +'/pornstars.html?o=v30','tubePirateMostActorIndex',artwork + '/main/thismonth.png')
        main.addDir('All Time',base_url +'/pornstars.html?o=v','tubePirateMostActorIndex',artwork + '/main/alltime.png')

def LETTERS():
        main.addDir('A', base_url + '/pornstars.html?l=A','tubePirateMostActorIndex',artwork + '/letters/a.png')
        main.addDir('B', base_url + '/pornstars.html?l=B','tubePirateMostActorIndex',artwork + '/letters/b.png')
        main.addDir('C', base_url + '/pornstars.html?l=C','tubePirateMostActorIndex',artwork + '/letters/c.png')
        main.addDir('D', base_url + '/pornstars.html?l=D','tubePirateMostActorIndex',artwork + '/letters/d.png')
        main.addDir('E', base_url + '/pornstars.html?l=E','tubePirateMostActorIndex',artwork + '/letters/e.png')
        main.addDir('F', base_url + '/pornstars.html?l=F','tubePirateMostActorIndex',artwork + '/letters/f.png')
        main.addDir('G', base_url + '/pornstars.html?l=G','tubePirateMostActorIndex',artwork + '/letters/g.png')
        main.addDir('H', base_url + '/pornstars.html?l=H','tubePirateMostActorIndex',artwork + '/letters/h.png')
        main.addDir('I', base_url + '/pornstars.html?l=I','tubePirateMostActorIndex',artwork + '/letters/i.png')
        main.addDir('J', base_url + '/pornstars.html?l=J','tubePirateMostActorIndex',artwork + '/letters/j.png')
        main.addDir('K', base_url + '/pornstars.html?l=K','tubePirateMostActorIndex',artwork + '/letters/k.png')
        main.addDir('L', base_url + '/pornstars.html?l=L','tubePirateMostActorIndex',artwork + '/letters/l.png')
        main.addDir('M', base_url + '/pornstars.html?l=M','tubePirateMostActorIndex',artwork + '/letters/m.png')
        main.addDir('N', base_url + '/pornstars.html?l=N','tubePirateMostActorIndex',artwork + '/letters/n.png')
        main.addDir('O', base_url + '/pornstars.html?l=O','tubePirateMostActorIndex',artwork + '/letters/o.png')
        main.addDir('P', base_url + '/pornstars.html?l=P','tubePirateMostActorIndex',artwork + '/letters/p.png')
        main.addDir('Q', base_url + '/pornstars.html?l=Q','tubePirateMostActorIndex',artwork + '/letters/q.png')
        main.addDir('R', base_url + '/pornstars.html?l=R','tubePirateMostActorIndex',artwork + '/letters/r.png')
        main.addDir('S', base_url + '/pornstars.html?l=S','tubePirateMostActorIndex',artwork + '/letters/s.png')
        main.addDir('T', base_url + '/pornstars.html?l=T','tubePirateMostActorIndex',artwork + '/letters/t.png')
        main.addDir('U', base_url + '/pornstars.html?l=U','tubePirateMostActorIndex',artwork + '/letters/u.png')
        main.addDir('V', base_url + '/pornstars.html?l=V','tubePirateMostActorIndex',artwork + '/letters/v.png')
        main.addDir('W', base_url + '/pornstars.html?l=W','tubePirateMostActorIndex',artwork + '/letters/w.png')
        main.addDir('X', base_url + '/pornstars.html?l=X','tubePirateMostActorIndex',artwork + '/letters/x.png')
        main.addDir('Y', base_url + '/pornstars.html?l=Y','tubePirateMostActorIndex',artwork + '/letters/y.png')
        main.addDir('Z', base_url + '/pornstars.html?l=Z','tubePirateMostActorIndex',artwork + '/letters/z.png')
 
def GENRES():
                main.addDir('Amateur',base_url +'/videos/amateur.html','tubePirateIndex',artwork + '/adult/amateur.png')
                main.addDir('Anal / Ass',base_url +'/videos/anal-ass.html','tubePirateIndex',artwork + '/adult/anal.png')
                main.addDir('Anime / Toon',base_url +'/videos/anime-toon.html','tubePirateIndex',artwork + '/adult/anime.png')
                main.addDir('Asian',base_url +'/videos/asian.html','tubePirateIndex',artwork + '/adult/asian.png')
                main.addDir('Babysitter',base_url +'/videos/babysitter.html','tubePirateIndex',artwork + '/adult/babysitter.png')
                main.addDir('BBW / Fat',base_url +'/videos/bbw-fat.html','tubePirateIndex',artwork + '/adult/bbw.png')
                main.addDir('BDSM',base_url +'/videos/bdsm.html','tubePirateIndex',artwork + '/adult/bdsm.png')
                main.addDir('Bi-Sexual',base_url +'/videos/bi-sexual.html','tubePirateIndex',artwork + '/adult/bisexual.png')
                main.addDir('Big Asses',base_url +'/videos/big-asses.html','tubePirateIndex',artwork + '/adult/bigbutts.png')
                main.addDir('Big Tits',base_url +'/videos/big-tits.html','tubePirateIndex',artwork + '/adult/bigtits.png')
                main.addDir('Black',base_url +'/videos/black.html','tubePirateIndex',artwork + '/adult/black.png')
                main.addDir('Blowjob',base_url +'/videos/blowjob.html','tubePirateIndex',artwork + '/adult/blowjob.png')
                main.addDir('CFMN',base_url +'/videos/cfnm.html','tubePirateIndex',artwork + '/adult/cfmn.png')
                main.addDir('Classic',base_url +'/videos/classic.html','tubePirateIndex',artwork + '/adult/classic.png')
                main.addDir('Cream Pie',base_url +'/videos/cream-pie.html','tubePirateIndex',artwork + '/adult/creampie.png')
                main.addDir('Cumshot',base_url +'/videos/cumshot.html','tubePirateIndex',artwork + '/adult/cumshot.png')
                main.addDir('Escort / Hooker',base_url +'/videos/escort-hooker.html','tubePirateIndex',artwork + '/adult/escort.png')
                main.addDir('Fetish',base_url +'/videos/fetish.html','tubePirateIndex',artwork + '/adult/fetish.png')
                main.addDir('Footjob',base_url +'/videos/footjob.html','tubePirateIndex',artwork + '/adult/footjob.png')
                main.addDir('Gang Bang',base_url +'/videos/gangbang.html','tubePirateIndex',artwork + '/adult/gangbang.png')
                main.addDir('Grannies',base_url +'/videos/grannies.html','tubePirateIndex',artwork + '/adult/grannies.png')
                main.addDir('Group Sex',base_url +'/videos/group-sex.html','tubePirateIndex',artwork + '/adult/groupsex.png')
                main.addDir('Hairy',base_url +'/videos/hairy.html','tubePirateIndex',artwork + '/adult/hairy.png')
                main.addDir('Handjob',base_url +'/videos/handjob.html','tubePirateIndex',artwork + '/adult/handjob.png')
                main.addDir('Hardcore',base_url +'/videos/hardcore.html','tubePirateIndex',artwork + '/adult/hardcore.png')
                main.addDir('Housewifes',base_url +'/videos/housewives.html','tubePirateIndex',artwork + '/adult/housewifes.png')
                main.addDir('Indian',base_url +'/videos/indian.html','tubePirateIndex',artwork + '/adult/indian.png')
                main.addDir('Insertions',base_url +'/videos/insertions.html','tubePirateIndex',artwork + '/adult/insertions.png')
                main.addDir('Interracial',base_url +'/videos/interracial.html','tubePirateIndex',artwork + '/adult/interracial.png')
                main.addDir('Latina',base_url +'/videos/latina.html','tubePirateIndex',artwork + '/adult/latina.png')
                main.addDir('Lesbian',base_url +'/videos/lesbian.html','tubePirateIndex',artwork + '/adult/lesbian.png')
                main.addDir('Masturbation',base_url +'/videos/masturbation.html','tubePirateIndex',artwork + '/adult/masturbation.png')
                main.addDir('Mature',base_url +'/videos/mature.html','tubePirateIndex',artwork + '/adult/mature.png')
                main.addDir('Midget',base_url +'/videos/midget.html','tubePirateIndex',artwork + '/adult/midget.png')
                main.addDir('MILF',base_url +'/videos/milf.html','tubePirateIndex',artwork + '/adult/milf.png')
                main.addDir('Other / Bizarre',base_url +'/videos/other-bizarre.html','tubePirateIndex',artwork + '/adult/bizarre.png')
                main.addDir('Panties',base_url +'/videos/panties.html','tubePirateIndex',artwork + '/adult/panties.png')
                main.addDir('Party Girls',base_url +'/videos/party-girls.html','tubePirateIndex',artwork + '/adult/partygirls.png')
                main.addDir('Point Of View',base_url +'/videos/point-of-view.html','tubePirateIndex',artwork + '/adult/pov.png')
                main.addDir('Pregnant',base_url +'/videos/pregnant.html','tubePirateIndex',artwork + '/adult/pregnant.png')
                main.addDir('Sex Guides',base_url +'/videos/sex-guides.html','tubePirateIndex',artwork + '/adult/sexguides.png')
                main.addDir('Solo Girl',base_url +'/videos/solo-girl.html','tubePirateIndex',artwork + '/adult/solo.png')
                main.addDir('Squirting',base_url +'/videos/squirting.html','tubePirateIndex',artwork + '/adult/squirting.png')
                main.addDir('Teen / Coed',base_url +'/videos/teen-coed.html','tubePirateIndex',artwork + '/adult/teen.png')
                main.addDir('Threesomes',base_url +'/videos/threesomes.html','tubePirateIndex',artwork + '/adult/threesome.png')
                main.addDir('Transsexual',base_url +'/videos/transsexual.html','tubePirateIndex',artwork + '/adult/tranny.png')
                main.addDir('Uniform',base_url +'/videos/uniform.html','tubePirateIndex',artwork + '/adult/uniform.png')
                main.addDir('Voyeur',base_url +'/videos/voyeur.html','tubePirateIndex',artwork + '/adult/voyeur.png')
 
def INDEX(url):
        next_page = ''
        link = net.http_GET(url).content
        match=re.compile('<a href=".+?" title=".+?" class="thumb" style="background-image:url(.+?);"></a><a href=".+?" class="add"></a><h5><a href="(.+?)" title=".+?">(.+?)</a>').findall(link)
        np=re.compile('<link rel="next" href="(.+?)" />').findall(link)
        if len(np) > 0:
                npc = str(np[0]).replace('&amp;','&')
                next_page = base_url + npc
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'tubePirateIndex',artwork + '/main/next.png')
        for thumbnail,url,name in match:
                
                        thumbnail = re.sub('[()]','',thumbnail)
                        url = base_url + url
                        
                        try:
                                links = net.http_GET(url).content
                                vid_link=re.compile('var streams={"low":"(.+?)"}').findall(links)
                        except:
                                continue
                        try:       
                                main.addDir(name,vid_link[0],'resolve',thumbnail)
                        except:
                                continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'tubePirateIndex',artwork + '/main/next.png')
    
def ACTOR_INDEX(url):
        next_page = ''
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href=".+?" class="thumb" style="background-image:url(.+?);"></a><h5><a href="(.+?)">(.+?)</a>').findall(link)
        np=re.compile('<link rel="next" href="(.+?)" />').findall(link)
        if len(np) > 0:
                npc = str(np[0]).replace('&amp;','&')
                next_page = base_url + npc
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'tubePirateMostActorIndex',artwork + '/main/next.png')
        for thumbnail,url,name in match:
                
                        thumbnail = re.sub('[()]','',thumbnail)
                        url = base_url + url

                        try:       
                                main.addDir(name,url,'tubePirateIndex',thumbnail)
                        except:
                                continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'tubePirateMostActorIndex',artwork + '/main/next.png')
   

        

