#Metal Video module by o9r1sh
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,main,urlresolver,xbmc,os

net = main.net
artwork = main.artwork
settings = main.settings
base_url = 'http://www.metalvideo.com/'

def categories():
        main.addDir('Top Videos',base_url + '/topvideos.html','metalVideoIndex',artwork + '/main/toprated.png')
        #main.addDir('Newest Videos',base_url + '/newvideos.html','metalVideoIndex',artwork + '/main/recentlyadded.png')
        main.addDir('Categories',base_url + 'none','metalVideoGenres',artwork + '/main/categories.png')
        main.addDir('Search',base_url + 'none','metalVideoSearch',artwork + '/main/search.png')


def genres():
        main.addDir("Alternative",base_url + '/browse-alternative-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/alternative.png')
        main.addDir("Black Metal",base_url + '/browse-black_metal-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/blackmetal.png')
        main.addDir("Classic Metal",base_url + '/browse-classic_metal-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/classicmetal.png')
        main.addDir("Concerts",base_url + '/browse-concerts-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/concerts.png')
        main.addDir("Death Metal",base_url + '/browse-death_metal-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/deathmetal.png')
        main.addDir("Featured",base_url + '/browse-featured-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/featured.png')
        main.addDir("Folk Metal",base_url + '/browse-folk_metal-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/folkmetal.png')
        main.addDir("Gothic Metal",base_url + '/browse-gothic_metal-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/gothicmetal.png')
        main.addDir("Grindcore",base_url + '/browse-grindcore-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/grindcore.png')
        main.addDir("Hair Metal",base_url + '/browse-hair_metal-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/hairmetal.png')
        main.addDir("Hard Rock",base_url + '/browse-hard_rock-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/hardrock.png')
        main.addDir("Heavy Metal",base_url + '/browse-heavy_metal-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/heavymetal.png')
        main.addDir("Indie Metal",base_url + '/browse-indie_metal-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/indiemetal.png')
        main.addDir("Industrial",base_url + '/browse-industrial-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/industrial.png')
        main.addDir("Interviews",base_url + '/browse-Interviews-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/interviews.png')
        main.addDir("Megadeth",base_url + '/browse-megadeth-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/megadeth.png')
        main.addDir("Metal Blade Records",base_url + '/browse-metalblade-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/metalblade.png')
        main.addDir("Metalcore",base_url + '/browse-metalcore-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/metalcore.png')
        main.addDir("Metallica",base_url + '/browse-metallica-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/metallica.png')
        main.addDir("Promo Videos",base_url + '/browse-promo-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/promos.png')
        main.addDir("Punk And Hardcore",base_url + '/browse-punk_hardcore-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/hardcore.png')
        main.addDir("Relapse Records",base_url + '/browse-relapse-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/relapserecords.png')
        main.addDir("Slipknot",base_url + '/browse-slipknot-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/slipknot.png')
        main.addDir("Stoner Rock",base_url + '/browse-stoner_rock-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/stonerrock.png')
        main.addDir("Technical",base_url + '/browse-technical-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/technical.png')
        main.addDir("Thrash metal",base_url + '/browse-thrash-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/thrashmetal.png')
        main.addDir("Capitol Chaos",base_url + '/browse-Capital_Chaos-videos-1-date.html' ,'metalVideoIndex', artwork + '/music/capitolchaos.png')
                       
def index(url):
        match2 = ''
        npUrl = ''
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)">\n\t\t\t<img src="(.+?)"  alt=".+?" class=".+?" width=".+?" height=".+?" /><div class=".+?"><span class=".+?">.+?</span></div>\n\t\t\t</a>\n\t\t\t<a href=".+?">\n\t\t\t<span class="artist_name">(.+?)</span> <span class="song_name">(.+?)</span>').findall(link)
        match3=re.compile('<a href=".+?">\n\t\t\t<img src="(.+?)"  alt=".+?" class="imag" width=".+?" height=".+?" /><div class="tag"></div>\n\t\t\t</a>\n\t\t\t<a href="(.+?)">\n\t\t\t<span class="artist_name">(.+?)</span> <span class="song_name">(.+?)</span>').findall(link)
        match4=re.compile('<a href="(.+?)">\n\t\t\t<img src="(.+?)"  alt="(.+?)" class=".+?" width=".+?" height=".+?" /><div class="tag"><span class=".+?">.+?</span></div>\n\t\t\t</a>\n\t\t\t<span class="artist_name">(.+?)</span>').findall(link)
        match2=re.compile('<img src="(.+?)" alt=".+?" class=".+?" width=".+?" height=".+?" align=".+?" border=".?" /></a></td>\n\t\t\t\t<td class=".+?">(.+?)</td>\n<td class=".+?"><a href="(.+?)">(.+?)</a>').findall(link)

        np=re.compile('<a href="(.+?)">(.+?)</a>').findall(link)
        for url, name in np:
                if name == 'next &raquo;':
                        npUrl = base_url + '/' + url
                        if settings.getSetting('nextpagetop') == 'true':
                                main.addDir('[COLOR blue]Next Page[/COLOR]',npUrl,'metalVideoIndex',artwork + '/main/next.png')
        
        for url,thumbnail,artist,song in match:
                name = artist + ' - ' + song

                try:
                        main.addDir(name,url,'metalVideoVideoLinks',thumbnail)
                except:
                        pass

        for thumbnail,artist,url,song in match2:
                name = artist + ' - ' + song
                try:
                        main.addDir(name,url,'metalVideoVideoLinks',thumbnail)
                except:
                        pass

        for thumbnail,url,artist,song in match3:
                name = artist + ' - ' + song
                try:
                        main.addDir(name,url,'metalVideoVideoLinks',thumbnail)
                except:
                        pass

        for url,thumbnail,song,artist in match4:
                name = artist + ' - ' + song
                try:
                        main.addDir(name,url,'metalVideoVideoLinks',thumbnail)
                except:
                        pass
                
        if not npUrl == '':
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',npUrl,'metalVideoIndex',artwork + '/main/next.png')

def videoLinks(url,name):
        link = net.http_GET(url).content
        match=re.compile("file: \'(.+?)'").findall(link)
        if len(match) == 0:
                match=re.compile('src="(.+?)" frameborder=".+?" allowfullscreen>').findall(link)
        for url in match:
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
                
                url = base_url + '/search.php?keywords=' + search + '&btn=Search'
                
                index(url)


                


