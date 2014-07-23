#Videocloud Module by o9r1sh October 2013

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os
import urlresolver

artwork = main.artwork
base_url = 'http://videocloud.in'

def CATEGORIES():
        main.addDir('Action',base_url +'/category/action/','videoCloudIndex',artwork + '/genres/action.png')
        main.addDir('Adventure',base_url +'/category/adventure/','videoCloudIndex',artwork + '/genres/adventure.png')
        main.addDir('Comedy',base_url +'/category/comedy/','videoCloudIndex',artwork + '/genres/comedy.png')
        main.addDir('Crime',base_url +'/category/crime/','videoCloudIndex',artwork + '/genres/crime.png')
        main.addDir('Drama',base_url +'/category/drama/','videoCloudIndex',artwork + '/genres/drama.png')
        main.addDir('Family',base_url +'/category/family/','videoCloudIndex',artwork + '/genres/family.png')
        main.addDir('Fantasy',base_url +'/category/fantasy/','videoCloudIndex',artwork + '/genres/fantasy.png')
        main.addDir('Horror',base_url +'/category/horror/','videoCloudIndex',artwork + '/genres/horror.png')
        main.addDir('Mystery',base_url +'/category/mystery/','videoCloudIndex',artwork + '/genres/mystery.png')
        main.addDir('Others',base_url +'/category/others/','videoCloudIndex',artwork + '/genres/others.png')
        main.addDir('Romance',base_url +'/category/romance/','videoCloudIndex',artwork + '/genres/romance.png')
        main.addDir('Sci-Fi',base_url +'/category/sci-fi/','videoCloudIndex',artwork + '/genres/sci-fi.png')
        main.addDir('Thriller',base_url +'/category/thriller/','videoCloudIndex',artwork + '/genres/thriller.png')
        main.addDir('War',base_url +'/category/war/','videoCloudIndex',artwork + '/genres/war.png')
        main.addDir('Western',base_url +'/category/western/','videoCloudIndex',artwork + '/genres/western.png')

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href=".+?" title=".+?">(.+?)</a></h1>\n\t\t\n\t\t\n\t</header>\n\n\t<div class=".+?">\n\t\t<a href="(.+?)"><img src="(.+?)" alt=".+?" width=".+?" height=".+?" class=".+?" /></a>').findall(link)
        np=re.compile('<strong>.+?</strong><a href="(.+?)">').findall(link)
        if len(np) > 0:
                next_page = np[0]
                main.addDir('Next Page',next_page,'videoCloudIndex',artwork + '/main/next.png')
        for name,url,thumbnail in match:
                if len(match) > 0:
                        head, sep, tail = name.partition(')')
                        name = head[:-5]
                        year = head[-5:] + sep

                        try:
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                links=response.read()
                                response.close()
                                vid_link=re.compile('<source src="(.+?)"').findall(links)
                        except:
                                continue
                        try:       
                                main.addMDir(name,vid_link[0],'resolve',thumbnail,year,False)
                        except:
                                continue

        main.AUTOVIEW('movies')

