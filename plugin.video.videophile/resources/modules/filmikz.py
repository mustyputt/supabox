#Filmikz module by o9r1sh

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,main,urlresolver,xbmc,os

net = main.net

artwork = main.artwork
base_url = 'http://filmikz.ch/'
settings = main.settings

def ADULT_CATEGORIES():
        main.addDir('Adult Movies',base_url + 'index.php?genre=14','filmikzAdultIndex',artwork + '/main/movie.png')  
        main.addDir('Adult Search','none','filmikzAdultSearch',artwork + '/main/search.png')  

def ADULT_INDEX(url):
        np_url = ''
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" width=".+?" height=".+?" border=".+?" /></a></div></td>\n                           \n                            <td width=".+?" valign=".+?" class=".+?"  align=".+?"><p><strong>(.+?): </strong></p>\n                                <p>.+?</p>\n                              <p><span class=".+?"><a href="/(.+?)">').findall(link)
        np=re.compile("href='(.+?)'>(.+?)</a></td><td><a style='color:red").findall(link)
        for url,name in np:
                if '&rsaquo' in name:
                        np_url = base_url + url
                        if settings.getSetting('nextpagetop') == 'true':
                                main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'filmikzAdultIndex', artwork + 'main/next.png')
                        
        for thumbnail,name,url in match:
                url = base_url + url
                thumbnail = base_url + thumbnail
                main.addDir(name,url,'filmikzVideoLinks',thumbnail)
        for url,name in np:
                if '&rsaquo' in name:
                        np_url = base_url + url
                        if settings.getSetting('nextpagebottom') == 'true':
                                main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'filmikzAdultIndex', artwork + 'main/next.png')

                                 
def VIDEOLINKS(url,name,thumb):
        hthumb = ''
        link = net.http_GET(url).content
        match=re.compile('<input type=button value="(.+?)" onClick="javascript:popUp((.+?))">').findall(link)
        for host, url,url2 in match:
                url = base_url + url
                url = re.sub("[')(]", '', url)
                link = net.http_GET(url).content
                links2=re.compile('<frameset  cols=".+?">\n  <frame src="(.+?)" />\n  <frame src=".+?" />').findall(link)
                if len(links2) > 0:
                        url = str(links2[0])
                if main.resolvable(url):
                        if host == 'Watch Part 1-ePornik':
                                hthumb = artwork + '/hosts/epornik1.png'
                        elif host == 'Watch Part 2-ePornik':
                                hthumb = artwork + '/hosts/epornik2.png'
                        elif host == 'Watch Part 3-ePornik':
                                hthumb = artwork + '/hosts/epornik3.png'
                        elif host == 'Watch Part 4-ePornik':
                                hthumb = artwork + '/hosts/epornik4.png'                         
                        elif host == 'Watch Part 1-YouWatch':
                                hthumb = artwork + '/hosts/youwatch1.png'
                        elif host == 'Watch Part 2-YouWatch':
                                hthumb = artwork + '/hosts/youwatch2.png'
                        elif host == 'Watch Part 3-YouWatch':
                                hthumb = artwork + '/hosts/youwatch3.png'
                        elif host == 'Watch Part 4-YouWatch':
                                hthumb = artwork + '/hosts/youwatch4.png'
                        elif host == 'Watch Part 1-Billionuploads':
                                hthumb = artwork + '/hosts/billionuploads1.png'
                        elif host == 'Watch Part 2-Billionuploads':
                                hthumb = artwork + '/hosts/billionuploads2.png'
                        elif host == 'Watch Part 3-Billionuploads':
                                hthumb = artwork + '/hosts/billionuploads3.png'
                        elif host == 'Watch Part 4-Billionuploads':
                                hthumb = artwork + '/hosts/billionuploads4.png'
                        elif host == 'Watch Part 1-Nosvideo':
                                hthumb = artwork + '/hosts/nosvideo1.png'
                        elif host == 'Watch Part 2-Nosvideo':
                                hthumb = artwork + '/hosts/nosvideo2.png'
                        elif host == 'Watch Part 3-Nosvideo':
                                hthumb = artwork + '/hosts/nosvideo3.png'
                        elif host == 'Watch Part 4-Nosvideo':
                                hthumb = artwork + '/hosts/nosvideo4.png'
                        else:
                                hthumb = main.GETHOSTTHUMB(main.getHost(url))
                        try:
                                main.addHDir(name,url,'resolve',hthumb)
                        except:
                                continue
       
         
def ADULT_SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                
                url = base_url + 'index.php?search=' + search
                ADULT_INDEX(url)
                



                


