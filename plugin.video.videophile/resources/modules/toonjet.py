#ToonJet Module by o9r1sh 
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os

net = main.net
artwork = main.artwork
base_url = 'http://www.toonjet.com'
settings = main.settings

def CATEGORIES():
        main.addDir('Featured', base_url + '/featured/','toonJetIndex',artwork + '/main/featured.png')
        main.addDir('Betty Boop', base_url + '/cartoons/BettyBoop/','toonJetIndex',artwork + '/main/bettyboop.png')
        main.addDir('Felix', base_url + '/cartoons/Felix/','toonJetIndex',artwork + '/main/felix.png')
        main.addDir('Looney Toons', base_url + '/cartoons/LooneyTunes/','toonJetIndex',artwork + '/main/looneytoons.png')
        main.addDir('Popeye', base_url + '/cartoons/Popeye/','toonJetIndex',artwork + '/main/popeye.png')
        main.addDir('Superman', base_url + '/cartoons/Superman/','toonJetIndex',artwork + '/main/superman.png')
        main.addDir('More Classics', base_url + '/cartoons/Classic/','toonJetIndex',artwork + '/main/moreclassics.png')

def INDEX(url):
        next_page = ''
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)"><img src="(.+?)" height=".+?" alt=".+?"><br />\r\n\t(.+?)<br /> "(.+?)"</a>').findall(link)
        np=re.compile('<<< Prev</a> | <a href="(.+?)">Next >></a></td></tr></table></div>\t\t\t\t\t</td>\r\n\t\t\t\t\t<td class=".+?" valign=".+?" align=".+?" width=".+?">').findall(link)
        if len(np) == 0:
                np=re.compile('<<< Prev</a> | <a href="(.+?)">Next >></a>').findall(link)
        if len(match) == 0:
                match=re.compile('<a href="(.+?)" class=".+?">(.+?)\r\n\t\t\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t<td valign=".+?">\r\n\t\t\t\t\t\t\t\t<table align=".+?" border=".+?" cellpadding=".+?" cellspacing=".+?" class=".+?">\r\n\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td>\r\n\t\t\t\t\t\t\t\t<a href=".+?"><img src="(.+?)" border=".+?" width=".+?" height=".+?" style="border: thin solid;">').findall(link)
        if len(np) == 0:
                np=re.compile('<a href="(.+?)" class="cartoons">More...</a>').findall(link)
        if len(match) == 0:
                match=re.compile('a href="(.+?)" class=".+?">(.+?)\r\n\t\t\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t<td valign=".+?">\r\n\t\t\t\t\t\t\t\t<table align=".+?" border=".+?" cellpadding=".+?" cellspacing=".+?" class=".+?">\r\n\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td>\r\n\t\t\t\t\t\t\t\t<a href=".+?"><img src="(.+?)" border=".+?" width=".+?" height=".+?">').findall(link)
        if len(np) == 0:
                np=re.compile('<a href="(.+?)">Next >></a>').findall(link)
        if settings.getSetting('nextpagetop') == 'true':
                try:
                        np_url = np[0]
                        next_page = base_url + '/' + np_url
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'toonJetIndex',artwork + '/main/next.png')
                except:
                        pass

        try:                
                for url,thumbnail,namea,nameb in match:
                        url = base_url + '/' + url
                        name = namea + nameb
                        try:
                                link = net.http_GET(url).content
                                match=re.compile('<iframe width=".+?" height=".+?" src="(.+?)" frameborder=".+?" allowfullscreen></iframe>').findall(link)
                                if len(match) > 0:
                                        for url in match:
                                                head,sep,tail = url.partition('autoplay=1')
                                                head = head.replace('embed/','watch?v=')
                                                main.addDir(name,head,'resolve',thumbnail)
                        except:
                                continue
        except:
                for url,name,thumbnail in match:
                        url = base_url + '/' + url
                        thumbnail = base_url + '/' + thumbnail
                        try:
                                link = net.http_GET(url).content
                                match=re.compile('<iframe width=".+?" height=".+?" src="(.+?)" frameborder=".+?" allowfullscreen></iframe>').findall(link)
                                if len(match) > 0:
                                        for url in match:
                                                head,sep,tail = url.partition('autoplay=1')
                                                head = head.replace('embed/','watch?v=')
                                                main.addDir(name,head,'resolve',thumbnail)
                        except:
                                continue
        if len(np) == 0:
                np=re.compile('<<< Prev</a> | <a href="(.+?)">Next >></a>').findall(link)
        if len(match) == 0:
                match=re.compile('<a href="(.+?)" class=".+?">(.+?)\r\n\t\t\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t<td valign=".+?">\r\n\t\t\t\t\t\t\t\t<table align=".+?" border=".+?" cellpadding=".+?" cellspacing=".+?" class=".+?">\r\n\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td>\r\n\t\t\t\t\t\t\t\t<a href=".+?"><img src="(.+?)" border=".+?" width=".+?" height=".+?" style="border: thin solid;">').findall(link)
        if len(np) == 0:
                np=re.compile('<a href="(.+?)" class="cartoons">More...</a>').findall(link)
        if len(match) == 0:
                match=re.compile('a href="(.+?)" class=".+?">(.+?)\r\n\t\t\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t<td valign=".+?">\r\n\t\t\t\t\t\t\t\t<table align=".+?" border=".+?" cellpadding=".+?" cellspacing=".+?" class=".+?">\r\n\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t<td>\r\n\t\t\t\t\t\t\t\t<a href=".+?"><img src="(.+?)" border=".+?" width=".+?" height=".+?">').findall(link)
        if len(np) == 0:
                np=re.compile('<a href="(.+?)">Next >></a>').findall(link)
        if settings.getSetting('nextpagetop') == 'true':
                try:
                        np_url = np[0]
                        next_page = base_url + '/' + np_url
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'toonJetIndex',artwork + '/main/next.png')
                except:
                        pass
                
                

                        


