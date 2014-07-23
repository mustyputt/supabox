# -*- coding: iso-8859-1 -*-
import urllib,urllib2,cookielib,base64,re,xbmcplugin,xbmcgui,urlresolver,xbmc,xbmcaddon,os,time,json,socket,sys
from metahandler import metahandlers
from addon.common.addon import Addon
from addon.common.net import Net
import silent


#All You See (alluc.to) - by The_Silencer 2013 v3.5
#Art Work provided by azad720



#Paths
addon_id = 'plugin.video.alluc'
local = xbmcaddon.Addon(id=addon_id)
allucpath = local.getAddonInfo('path')
addon = Addon(addon_id)
datapath = addon.get_profile()
cookie_path = os.path.join(datapath)
art = allucpath+'/art'
cookiejar = os.path.join(cookie_path,'alluc.lwp')
cookiejar1 = os.path.join(cookie_path,'un.lwp')

#Global constants
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
net = Net()
ALLUC_URL = 'http://www.alluc.to/'
ALLUC_FORUMS = 'http://board.alluc.to/'
socket.setdefaulttimeout(40) #Set default timout some unristriced.li links slowly returned
metaget = metahandlers.MetaData()

#Unristrict guest and registered captcha class
class InputWindow(xbmcgui.WindowDialog):# Cheers to Bastardsmkr code already done in Putlocker PRO resolver.
    
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        xposition = 335
        yposition = 30
        hposition = 180
        wposition = 624
        self.img = xbmcgui.ControlImage(xposition,yposition,wposition,hposition,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        time.sleep(3)        
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        self.close()
        return False

#ALLUC Logon
def FINDSID(url):
        content = net.http_GET(url).content
        match=re.search('<input type="hidden" name="pageid" value="5" />\r\n\t\t<input type="hidden" name="sid" value="(.+?)" />\r\n\t\t<input type="hidden" name="sysparam" value="" />', content) #<input type="hidden" name="sid" value="(.+?)"
        return match

def CHECKUSER(url):
        hide_message = local.getSetting('hide-successful-login-messages')
        net.set_cookies(cookiejar)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('href="/logout.html">Logout (.+?)</a>').findall(link)
        if match:
                if hide_message == 'false':
                        print 'ALLUC Account: login successful'
                        silent.Notify('small','ALLUC', 'Account login successful.',5000)
        if not match:
                print 'ALLUC Account: login failed'
                silent.Notify('big','ALLUC','Login failed: check your username and password', '')
        pass

def LoginStartup():
        alluc_account = local.getSetting('alluc-account')
        hide_message = local.getSetting('hide-successful-login-messages')
        if alluc_account == 'true':
                loginurl = ALLUC_URL
                login = local.getSetting('alluc-username')
                password = local.getSetting('alluc-password')
                
                sid = FINDSID(loginurl)
                form = {'action' : 'login_out_box', 'loginid' : login, 'passwd' : password, 'remember' : '1', 'pageid' : '5', 'sid' : sid}
                
                net.http_POST(loginurl, form)
                net.save_cookies(cookiejar)        
                CHECKUSER(ALLUC_URL)
                
#unrestrict.li routines
def UNLoginStartup():
        #VIP Login
        unrestrict_account = local.getSetting('unrestrict-account')
        unrestirct_regaccount = local.getSetting('unrestrict-regaccount')
        hide_message = local.getSetting('hide-successful-login-messages2')
        if unrestrict_account == 'true':
                login = local.getSetting('unrestrict-username')
                password = local.getSetting('unrestrict-password')
                url='http://unrestrict.li/sign_in'

                data = net.http_POST(url,{'return':'vip','username':login,'password':password,'signin':'Sign+in'}).content
                success=re.compile('href="http://unrestrict.li/profile">(.+?)</a>.+?href="http://unrestrict.li/sign_out">(.+?)</a>',re.DOTALL).findall(data)
                if success:
                        net.save_cookies(cookiejar1)
                        if hide_message == 'false':
                                print 'Unrestrict VIP Account: login successful'
                                silent.Notify('small','Unrestrict', 'VIP account login successful.',5000)
                if not success:
                        print 'Unrestrict VIP Account: login failed'
                        silent.Notify('big','Unrestrict','VIP Login failed: check your username and password', '')
                        
        #Free registered login
        if unrestirct_regaccount == 'true':
                login = local.getSetting('unrestrict-regusername')
                password = local.getSetting('unrestrict-regpassword')
                url='http://unrestrict.li/sign_in'

                data = net.http_POST(url,{'return':'registered','username':login,'password':password,'signin':'Sign+in'}).content
                success=re.compile('href="http://unrestrict.li/profile">(.+?)</a>.+?href="http://unrestrict.li/sign_out">(.+?)</a>',re.DOTALL).findall(data)
                if success:
                        net.save_cookies(cookiejar1)
                        if hide_message == 'false':
                                print 'Unrestrict Registered Account: login successful'
                                silent.Notify('small','Unrestrict', 'Account login successful.',5000)
                if not success:
                        print 'Unrestrict Registered Account: login failed'
                        silent.Notify('big','Unrestrict','Registered Login failed: check your username and password', '')

def UNLINK(url):
        #UNLoginStartup()
        net.set_cookies(cookiejar1)
        link = net.http_POST('http://unrestrict.li/unrestrict.php',{'link':url,'domain':'long'}).content
        addon.log((url,link))
        download_link = json.loads(link).items()[0][0] # The response is JSON list, therfore need to iterate the list and select item[0] - item[0]
        addon.log(download_link)
        if '404' in download_link:
                silent.Notify('small','Link Removed:', 'Please try another one.',6000)
        else:
                if 'http://unrestrict.li' in download_link:
                    addon.log('UNRESTRICT.LI STATUS: REGISTERED - NOT VIP')
                    
                    try:
                        captcha_dir = os.path.join( datapath, 'resources')
                        captcha_img = os.path.join(captcha_dir, 'unrestrict_li_puzzle.png')
                        if not os.path.exists(captcha_dir):
                            os.makedirs(captcha_dir)
                        os.remove(captcha_img)
                    except: 
                        pass
                    
                    try:
                        response = net.http_GET(download_link)
                        html =  response.content                    
                        media_id=re.compile('id="link" type="hidden" value="(.+?)" />').findall(html)[0]
                        noscript=re.compile('<iframe src="(.+?)"').findall(html)[0]
                        check = net.http_GET(noscript).content
                        hugekey=re.compile('id="adcopy_challenge" value="(.+?)">').findall(check)[0]
                        captcha_headers= {'User-Agent':'Mozilla/6.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4',
                             'Host':'api.solvemedia.com','Referer':response.get_url(),'Accept':'image/png,image/*;q=0.8,*/*;q=0.5'}
                        open(captcha_img, 'wb').write( net.http_GET("http://api.solvemedia.com%s"%re.compile('<img src="(.+?)"').findall(check)[0]).content)
                        solver = InputWindow(captcha=captcha_img)
                        puzzle = solver.get()
                        if puzzle:
                            addon.log('CAPTCHA')
                            data={'response':urllib.quote_plus(puzzle),'challenge':hugekey,'link':media_id}
                            html = net.http_POST('http://unrestrict.li/download.php',data).content
                            download_link = json.loads(html).items()[0][1]
                            addon.log(download_link)
                    except:
                        raise   
                #Reload link to pull into player *attempt to fix slow link response* Working not sure if the best way to handle this issue?
                req = urllib2.Request(download_link)
                req.add_header('User-Agent', USER_AGENT)
                streamlink = urllib2.urlopen(req).url
        
                addLink(streamlink,streamlink,'')

def VIPSTATUS():
        net.set_cookies(cookiejar1)
        vip = net.http_GET('http://unrestrict.li/profile').content
        match=re.compile('<span class="purplefont">Status</span></h3></td>.+?<td style="border-right:none;" align="left"><p>(.+?)</p>',re.DOTALL).findall(vip)
        for name in match:
                name = name.replace('&nbsp;',' ')
                addDir(name,'','','',None,'')

#Download Routines
def DOWNLOADINFO(name,url):
        name = url.split('@')[1]
        url = url.split('@')[0]
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        downloadlink = urlresolver.resolve(urllib2.urlopen(req).url)
        print downloadlink
       
        url = downloadlink
        dir = local.getSetting('download-folder')
        DOWNLOAD(name,url,dir)

def DOWNLOAD(name,url, dir):
        download_status = local.getSetting('download-status')
        file_name = url
        file_name = file_name.replace('http://','')
        file_name = file_name.replace('/','')
        new_name = file_name[-4:]
        file_name = name+new_name
        u = urllib2.urlopen(url)
        f = open(dir+file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        silent.Notify('small','Downloading:', '%s Bytes: %s' % (file_name, file_size) ,5000)
        file_size_dl = 0
        block_sz = 20480
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            if download_status == 'false':
                    silent.Notify('small','Downloading: '+name, status ,'')
        f.close()
        silent.Notify('small','Download: '+name, 'Completed' ,8000)

#Cleaner for names
def CLEAN(name):
        codes = ('(2015)', '(2014)', '(2013)', '(2012)', '(2011)', '(2010)', '(2009)', '(2008)', '(2007)', '(2006)', '(2005)', '(2004)', '(2003)', '(2002)',
                 '(2001)', '(2000)', '(1999)', '(1998)', '(1997)', '(1996)', '(1995)', '(1994)', '(1993)', '(1992)', '(1991)', '(1990)', '(1989)',
                 '(1988)', '(1987)', '(1986)', '(1985)', '(1984)', '(1983)', '(1982)', '(1981)', '(1980)', '(1979)', '(1978)', '(1977)', '(1976)',
                 '(1975)', '(1974)', '(1973)', '(1972)', '(1971)', '(1970)', '(1969)', '(1968)', '(1967)', '(1966)', '(1965)', '(1964)', '(1963)',
                 '(1962)', '(1961)', '(1960)', '(1959)', '(1958)', '(1957)', '(1956)', '(1955)', '(1954)', '(1953)', '(1953)', '(1952)', '(1951)',
                 '(1951)')
        if not any(c in name for c in codes):
                return name
        return name[:min(name.find(c) for c in codes if c in name)]

#Urlresolver setttings
def ResolverSettings():
        urlresolver.display_settings()

#Return Favorites List *temp need to fix in silent*
def GETMYFAVS():
        MYFAVS = silent.getFavorites()
        for name,url,types in MYFAVS:
                addFAVDir(name,url,types)

#Metahandlers passing name
grab = metahandlers.MetaData(preparezip = False)
def GRABMETA(name,types):
        type = types
        EnableMeta = local.getSetting('Enable-Meta')       
        if EnableMeta == 'true':
                if 'Movie' in type:
                        meta = grab.get_meta('movie',name,'','',None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                          'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                          'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                elif 'tvshow' in type:
                        meta = grab.get_meta('tvshow',name,'','',None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                              'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                              'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                              'backdrop_url': meta['backdrop_url'],'status': meta['status']}
        return infoLabels

#Metahandlers passing imdb
def GRABMETA2(imdb,types):
        type = types
        EnableMeta = local.getSetting('Enable-Meta')       
        if EnableMeta == 'true':
                if 'Movie' in type:
                        meta = grab.get_meta('movie','',imdb,'',None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                          'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                          'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                elif 'tvshow' in type:
                        meta = grab.get_meta('tvshow','',imdb,'',None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                              'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                              'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                              'backdrop_url': meta['backdrop_url'],'status': meta['status']}
        return infoLabels
                
#Menus
def CATEGORIES():
        LoginStartup()
        UNLoginStartup()
        alluc_account = local.getSetting('alluc-account')
        HideXXX = local.getSetting('Hide-XXX')

        addDir('Movies',ALLUC_URL,1,os.path.join(art,'movies.png'),None,'')
        addDir('TV-SHOWS',ALLUC_URL,4,os.path.join(art,'tv-shows.png'),None,'')
        addDir('Anime',ALLUC_URL,5,os.path.join(art,'anime.png'),None,'')
        addDir('Cartoons',ALLUC_URL,6,os.path.join(art,'cartoons.png'),None,'')
        addDir('Documentaries',ALLUC_URL,7,os.path.join(art,'documentaries.png'),None,'')
        addDir('Sports',ALLUC_URL,10,os.path.join(art,'sports.png'),None,'')
        if HideXXX == 'false':
                addDir('XXX',ALLUC_URL+'adult.html?',21,os.path.join(art,'xxx.png'),None,'')
        addDir('Search',ALLUC_URL,51,os.path.join(art,'search.png'),None,'')
        addDir('New Forum Links',ALLUC_FORUMS,44,os.path.join(art,'forum.png'),None,'')
        addDir('Favorites',ALLUC_URL,65,os.path.join(art,'favorites.png'),None,'')
        addDir('Settings',ALLUC_URL,62,os.path.join(art,'settings.png'),None,'')
        addDir('','','','',None,'')
        if alluc_account == 'true':
                #addDir('Check Login Status','http://alluc.to',13,'',None,'') #Check for ALLUC username for troubleshooting only
                
                #Check for new messages before adding Messagebox menu
                net.set_cookies(cookiejar)
                req = urllib2.Request(ALLUC_URL)
                req.add_header('User-Agent', USER_AGENT)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('title="Your Profile">Your Profile (.+?)</a></div>').findall(link)
                if match:
                        addDir('My Messagebox'+str(match),ALLUC_URL+'member-messagebox.html',37,os.path.join(art,'messagebox.png'),None,'')
                if not match:
                        addDir('My Messagebox',ALLUC_URL+'member-messagebox.html',37,os.path.join(art,'messagebox.png'),None,'')
                addDir('My Watchlist',ALLUC_URL+'watchlist.html',40,os.path.join(art,'watchlist.png'),None,'')
                addDir('Top 50 from Other Watchlist','http://www.alluc.to/watchlist.html?mode=top',39,os.path.join(art,'top-50.png'),None,'')

def FORUMS():
        addDir('New Movie Links',ALLUC_FORUMS+'forumdisplay.php?fid=30',45,os.path.join(art,'updated.png'),None,'')
        addDir('New TV-Show Links',ALLUC_FORUMS+'forumdisplay.php?fid=13',46,os.path.join(art,'updated.png'),None,'')
        addDir('New Documentaries Links',ALLUC_FORUMS+'forumdisplay.php?fid=31',47,os.path.join(art,'updated.png'),None,'')

def SETTINGS():
        unrestrict_account = local.getSetting('unrestrict-account')
        addDir('Resolver Settings',ALLUC_FORUMS,63,os.path.join(art,'settings.png'),None,'')
        if unrestrict_account == 'true':
                addDir('Check Unresitricted VIP status',ALLUC_FORUMS,64,os.path.join(art,'settings.png'),None,'')

def MOVIES():
        addDir('A-Z',ALLUC_URL+'movies.html',2,os.path.join(art,'a-z.png'),None,'')
        addDir('Genres',ALLUC_URL+'movies.html',3,os.path.join(art,'genres.png'),None,'')
        addDir('Actors',ALLUC_URL+'movies.html?mode=allactors',53,os.path.join(art,'actors.png'),None,'')
        addDir('Featured Movies',ALLUC_URL+'movies.html',25,os.path.join(art,'featured.png'),None,'')
        addDir('Updated Movies',ALLUC_URL+'movies.html?mode=updated',14,os.path.join(art,'updated.png'),None,'')
        addDir('Popular Movies',ALLUC_URL+'movies.html',14,os.path.join(art,'popular.png'),None,'')
        addDir('Search Movies',ALLUC_URL+'movies.html',28,os.path.join(art,'search.png'),None,'')

def ACTORSDIR():
        addDir('A-Z',ALLUC_URL+'movies.html?mode=allactors',54,os.path.join(art,'a-z.png'),None,'')
        addDir('Search Actors',ALLUC_URL+'movies.html?mode=allactors',55,os.path.join(art,'search.png'),None,'')
        
def ACTORSAZ():
        addDir('A',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('B',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('C',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('D',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('E',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('F',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('G',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('H',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('I',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('J',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('K',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('L',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('M',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('N',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('O',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('P',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('Q',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('R',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('S',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('T',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('U',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('V',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('W',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('X',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('Y',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        addDir('Z',ALLUC_URL+'movies.html?mode=allactors',49,'',None,'')
        
def ACTORSEARCH():
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search ALLUC for Actors')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                search = str(search).replace(' ','+')
                encode=urllib.quote(search)
                surl=ALLUC_URL+'movies/actor/'+encode+''
                req = urllib2.Request(surl)
                req.add_header('User-Agent', USER_AGENT)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('href="(.+?)" title="watch (.+?)\s\(([\d]{4})\) online"').findall(link)
                for url,name,year in match:
                        if EnableMeta == 'true':
                                addDir(name,ALLUC_URL+url,18,'','Movie',year)
                        if EnableMeta == 'false':
                                addDir(name,ALLUC_URL+url,18,'',None,year)

def MOVIESAZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="linklist2 linklist_header" title=".+?">\r\n \t\t\t\t(.+?)\r\n \t\t\t</a>').findall(link)
        for url,name in match:
                url = str(url).replace('&amp;','&')
                addDir(name,ALLUC_URL+url,14,'',None,None)

def MOVIESGEN(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<option value="(.+?)\|(.+?)" >(.+?)</option>').findall(link)
        for url,url2,name in match:
                addDir(name,'http://www.alluc.to/movies/'+url2+'/'+url+'.html',14,'',None,None)

def TVSHOWS():
        addDir('A-Z',ALLUC_URL+'tv-shows.html',19,os.path.join(art,'a-z.png'),None,'')
        addDir('Actors',ALLUC_URL+'tv-shows.html?mode=allactors',49,os.path.join(art,'actors.png'),None,'')
        addDir('Featured TV-SHOWS',ALLUC_URL+'tv-shows.html',26,os.path.join(art,'featured.png'),None,'')
        addDir('Updated TV-SHOWS',ALLUC_URL+'tv-shows.html?mode=updated',15,os.path.join(art,'updated.png'),None,'')
        addDir('Popular TV-SHOWS',ALLUC_URL+'tv-shows.html',15,os.path.join(art,'popular.png'),None,'')
        addDir('Search TV-SHOWS',ALLUC_URL+'tv-shows.html',29,os.path.join(art,'search.png'),None,'')

def TVSHOWSAZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="linklist2 linklist_header" title=".+?">\r\n \t\t\t\t(.+?)\r\n \t\t\t</a>').findall(link)
        for url,name in match:
                url = str(url).replace('&amp;','&')
                addDir(name,ALLUC_URL+url,15,'',None,None)

def ANIME():
        addDir('Featured',ALLUC_URL+'anime.html',26,os.path.join(art,'featured.png'),None,'')
        addDir('A-Z',ALLUC_URL+'anime.html',30,os.path.join(art,'a-z.png'),None,'')
        addDir('Search Anime',ALLUC_URL+'anime.html',31,os.path.join(art,'search.png'),None,'')

def ANIMEAZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="linklist2 linklist_header" title=".+?">\r\n \t\t\t\t(.+?)\r\n \t\t\t</a>').findall(link)
        for url,name in match:
                url = str(url).replace('&amp;','&')
                addDir(name,ALLUC_URL+url,15,'',None,None)

def CARTOONS():
        addDir('Featured',ALLUC_URL+'cartoons.html',26,os.path.join(art,'featured.png'),None,'')
        addDir('A-Z',ALLUC_URL+'cartoons.html',32,os.path.join(art,'a-z.png'),None,'')
        addDir('Search Cartoons',ALLUC_URL+'cartoons.html',33,os.path.join(art,'search.png'),None,'')
        
def CARTOONSAZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="linklist2 linklist_header" title=".+?">\r\n \t\t\t\t(.+?)\r\n \t\t\t</a>').findall(link)
        for url,name in match:
                url = str(url).replace('&amp;','&')
                addDir(name,ALLUC_URL+url,15,'',None,None)
        
def DOCUMENTARIES():
        addDir('A-Z',ALLUC_URL+'documentaries.html',8,os.path.join(art,'a-z.png'),None,'')
        addDir('Genres',ALLUC_URL+'documentaries.html',9,os.path.join(art,'genres.png'),None,'')
        addDir('Search Documentaries',ALLUC_URL,34,os.path.join(art,'search.png'),None,'')

def DOCUMENTARIESAZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="linklist2 linklist_header" title=".+?">\r\n \t\t\t\t(.+?)\r\n \t\t\t</a>').findall(link)
        for url,name in match:
                url = str(url).replace('&amp;','&')
                addDir(name,ALLUC_URL+url,15,'',None,None)

def DOCUMENTARIESGEN(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<option value="(.+?)\|(.+?)" >(.+?)</option>').findall(link)
        for url,url2,name in match:
                name = str(name).replace('&quot;','"')
                addDir(name,'http://alluc.to/documentaries/'+url2+'/'+url+'.html',14,'',None,None)

def SPORTS():
        addDir('A-Z',ALLUC_URL+'sport.html',11,os.path.join(art,'a-z.png'),None,'')
        addDir('Genres',ALLUC_URL+'sport.html',12,os.path.join(art,'genres.png'),None,'')

def SPORTSAZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="linklist2 linklist_header" title=".+?">\r\n \t\t\t\t(.+?)\r\n \t\t\t</a>').findall(link)
        for url,name in match:
                url = str(url).replace('&amp;','&')
                addDir(name,ALLUC_URL+url,15,'',None,None)

def SPORTSGEN(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<option value="(.+?)\|(.+?)" >(.+?)</option>').findall(link)
        for url,url2,name in match:
                addDir(name,'http://alluc.to/sport/'+url2+'/'+url+'.html',14,'',None,None)

def ADULT():
        addDir('A-Z',ALLUC_URL+'adult.html',23,os.path.join(art,'a-z.png'),None,'')
        addDir('Genres',ALLUC_URL+'adult.html',24,os.path.join(art,'genres.png'),None,'')
        addDir('Pornstars',ALLUC_URL+'adult.html?mode=allactors',70,os.path.join(art,'pornstars.png'),None,'')
        addDir('Featured XXX',ALLUC_URL+'adult.html',68,os.path.join(art,'featured.png'),None,'')
        addDir('Updated XXX',ALLUC_URL+'adult.html?mode=updated',69,os.path.join(art,'updated.png'),None,'')
        addDir('Popular XXX',ALLUC_URL+'adult.html?mode=popular',69,os.path.join(art,'popular.png'),None,'')
        addDir('Search XXX',ALLUC_URL+'adult.html',35,os.path.join(art,'search.png'),None,'')

def ADULTA():
        addDir('A',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('B',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('C',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('D',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('E',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('F',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('G',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('H',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('I',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('J',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('K',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('L',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('M',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('N',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('O',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('P',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('Q',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('R',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('S',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('T',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('U',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('V',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('W',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('X',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('Y',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')
        addDir('Z',ALLUC_URL+'adult.html?mode=allactors',67,'',None,'')

def ADULTAZ(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="linklist2 linklist_header" title=".+?">\r\n \t\t\t\t(.+?)\r\n \t\t\t</a>').findall(link)
        for url,name in match:
                url = str(url).replace('&amp;','&')
                addDir(name,ALLUC_URL+url,69,'',None,None)

def ADULTGEN(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<option value="(.+?)\|(.+?)" >(.+?)</option>').findall(link)
        for url,url2,name in match:
                addDir(name,'http://www.alluc.to/adult/'+url2+'/'+url+'.html',69,'',None,None)

#Search
def SEARCH():
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search ALLUC')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            encode=urllib.quote(search)
            surl=ALLUC_URL+'search.html?sword='+encode+''
            req = urllib2.Request(surl)
            req.add_header('User-Agent', USER_AGENT)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
            for url,name in match:
                if 'tv-shows' in url:
                        if EnableMeta == 'true':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                 addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')
                if 'cartoons' in url:
                        if EnableMeta == 'true':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')
                if 'anime' in url:
                        if EnableMeta == 'true':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')
                else:
                        if EnableMeta == 'true':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'','Movie','')
                        if EnableMeta == 'false':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')

#Universal search from other addons *pass title*
def UNIVERSALSEARCH(name):
        EnableMeta = local.getSetting('Enable-Meta')
        surl=ALLUC_URL+'search.html?sword='+name+''
        req = urllib2.Request(surl)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
        for url,name in match:
            if 'tv-shows' in url:
                    if EnableMeta == 'true':
                            addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                    if EnableMeta == 'false':
                            addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')
            if 'cartoons' in url:
                    if EnableMeta == 'true':
                            addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                    if EnableMeta == 'false':
                            addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')
            if 'anime' in url:
                    if EnableMeta == 'true':
                            addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                    if EnableMeta == 'false':
                            addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')
            else:
                    if EnableMeta == 'true':
                            addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'','Movie','')
                    if EnableMeta == 'false':
                            addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')

def SEARCHMOVIES():
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search ALLUC for Movies')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                surl=ALLUC_URL+'movies.html?mode=search&filter=&sort=&sword='+encode+''
                req = urllib2.Request(surl)
                req.add_header('User-Agent', USER_AGENT)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
                for url,name in match:
                        if EnableMeta == 'true':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'','Movie','')
                        if EnableMeta == 'false':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')

def SEARCHTV():
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search ALLUC for TV-Shows')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                surl=ALLUC_URL+'tv-shows.html?mode=search&filter=&sort=&sword='+encode+''
                req = urllib2.Request(surl)
                req.add_header('User-Agent', USER_AGENT)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
                for url,name in match:
                        if EnableMeta == 'true':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')

def SEARCHANIME():
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search ALLUC for TV-Shows')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                surl=ALLUC_URL+'anime.html?mode=search&filter=&sort=&sword='+encode+''
                req = urllib2.Request(surl)
                req.add_header('User-Agent', USER_AGENT)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
                for url,name in match:
                        if EnableMeta == 'true':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')
                                
def SEARCHCARTOON():
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search ALLUC for Cartoons')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                surl=ALLUC_URL+'cartoon.html?mode=search&filter=&sort=&sword='+encode+''
                req = urllib2.Request(surl)
                req.add_header('User-Agent', USER_AGENT)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
                for url,name in match:
                        if EnableMeta == 'true':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')

def SEARCHDOCUMENTARIES():
        EnableMeta = local.getSetting('Enable-Meta')
        keyb = xbmc.Keyboard('', 'Search ALLUC for Documentaries')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                surl=ALLUC_URL+'documentaries.html?mode=search&filter=&sort=&sword='+encode+''
                req = urllib2.Request(surl)
                req.add_header('User-Agent', USER_AGENT)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
                for url,name in match:
                        if EnableMeta == 'true':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'','Movie','')
                        if EnableMeta == 'false':
                                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')

def SEARCHADULT():
        keyb = xbmc.Keyboard('', 'Search ALLUC for XXX')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                surl=ALLUC_URL+'adult.html?mode=search&filter=&sort=&sword='+encode+''
                req = urllib2.Request(surl)
                req.add_header('User-Agent', USER_AGENT)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
                for url,name in match:
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')

#After login routines
def INDEX1(url):
        net.set_cookies(cookiejar)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('href="/logout.html">Logout (.+?)</a>').findall(link)
        for name in match:
               addDir('Logged in as: '+name,url,18,'',None,None)

def NEWMESSAGES(url):
        net.set_cookies(cookiejar)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('title="Your Profile">Your Profile (.+?)</a></div>').findall(link)
        return match

def MESSAGES(url):
        net.set_cookies(cookiejar)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<td class="msgsubjecteven"><a class="messageboxlink" href="(.+?)">(.+?)</a></td>.+?<a class="messageboxlink" href=".+?">(.+?)</a></td>.+?<td class="msgdateeven">(.+?)</td>',re.DOTALL).findall(link)#<a class="messageboxlink" href="(.+?)">(.+?)</a></td>.+?<a class="messageboxlink" href=".+?">(.+?)</a></td>
        for url,name,user,date in match:
                addDir("Subject: %s      From: %s        Date: %s"%(name,user,date),'http://www.alluc.to'+url,38,'',None,None)

def READMESSAGES(url):
        net.set_cookies(cookiejar)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div style="font-size:12px;width:768px;overflow:hidden;background-color:#fff;color:#000;padding:4px 4px 4px 4px;">(.+?)</div>',re.DOTALL).findall(link)
        for name in match:
               addDir(name,url,18,'',None,None)

def MYWATCHLIST(url):
        net.set_cookies(cookiejar)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div class="deflist" style="width:520px">.+?href="(.+?)".+?onmouseout=".+?".+?>(.+?)</a>',re.DOTALL).findall(link)
        #match = str(match).replace('&gt;','>')
        for url,name in match:
               addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,20,'',None,None)
        
def OTHERWATCHLIST(url):
        EnableMeta = local.getSetting('Enable-Meta')
        net.set_cookies(cookiejar)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<td class=".+?" style="width:15px;text-align:right;">(.+?).</td>.+?<a href="(.+?)".+?onmouseover=".+?".+?onmousemove=".+?".+?onmouseout=".+?".+?>(.+?)</a>',re.DOTALL).findall(link)
        #match = str(match).replace('&gt;',' ')
        for rank,url,name in match:
                if 'season' in url:
                        addDir("# %s  %s"%(rank,name.encode('UTF-8','ignore')),ALLUC_URL+url,17,'',None,'')
                if 'tv-shows' in url:
                        if EnableMeta == 'true':
                                addDir("# %s  %s"%(rank,name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                addDir("# %s  %s"%(rank,name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,16,'',None,'')
                if 'cartoons' in url:
                        if EnableMeta == 'true':
                                addDir("# %s  %s"%(rank,name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                addDir("# %s  %s"%(rank,name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,16,'',None,'')
                if 'anime' in url:
                        if EnableMeta == 'true':
                                addDir("# %s  %s"%(rank,name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,16,'','tvshow','')
                        if EnableMeta == 'false':
                                addDir("# %s  %s"%(rank,name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,16,'',None,'')
                else:
                        if EnableMeta == 'true':
                                addDir("# %s  %s"%(rank,name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,18,'','Movie','')
                        if EnableMeta == 'false':
                                addDir("# %s  %s"%(rank,name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,18,'',None,'')
               
#Movies              
def INDEX2(url):
        EnableMeta = local.getSetting('Enable-Meta')
        if EnableMeta == 'true': dialog = 'Please wait while Metadata is added.'
        if EnableMeta == 'false': dialog = 'Please wait while Movie list is created.'
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class="linklist2">\r\n\t\t\t\t\t<a href="(.+?)" title="watch (.+?) online">').findall(link)#<li class="linklist2">\r\n\t\t\t\t\t<a href="(.+?)" title="watch (.+?)\s\(([\d]{4})\) online">
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create(dialog)
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'',remaining_display)
        for url,name in match:
                loadedLinks = loadedLinks + 1 
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'',remaining_display)
                name = str(name).replace('&quot;','"')
                if EnableMeta == 'true':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'','Movie','')
                if EnableMeta == 'false':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait

#TV-SHOWS       
def INDEX3(url):
        EnableMeta = local.getSetting('Enable-Meta')
        if EnableMeta == 'true': dialog = 'Please wait while Metadata is added.'
        if EnableMeta == 'false': dialog = 'Please wait while Tv-Show list is created.'
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class="linklist2">\r\n\t\t\t\t\t<a href="(.+?)" title="watch (.+?) online">').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create(dialog)
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Tv-Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'',remaining_display)
        for url,name in match:
                name = str(name).replace('&quot;','"')
                if EnableMeta == 'true':
                        addDir2(CLEAN(name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,16,'','tvshow','')
                if EnableMeta == 'false':
                        addDir2(CLEAN(name.decode('iso-8859-1').encode('UTF-8','ignore')),ALLUC_URL+url,16,'',None,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Tv-Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'',remaining_display)
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait

#XXX      
def INDEX4(url):
        dialog = 'Please wait while the XXX list is created.'
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class="linklist2">\r\n\t\t\t\t\t<a href="(.+?)" title="(.+?)">').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create(dialog)
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'XXX loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'',remaining_display)
        for url,name in match:
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'XXX loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'',remaining_display)
                name = name.replace('watch', '')
                name = name.replace('online', '')
                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait

#Featured Movies
def FEATURED(url):
        EnableMeta = local.getSetting('Enable-Meta')
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="featuredlink" title=""\r\n\t\t\t\tonmouseover="vorschau\(\\\'ttfeatured\\\',true,\\\'(.+?)\s\(([\d]{4})\)').findall(link)
        for url,name,year in match:
                if EnableMeta == 'true':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),url,18,'','Movie',year)
                if EnableMeta == 'false':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),url,18,'',None,year)

#Featured TV-Shows
def FEATUREDTV(url):
        EnableMeta = local.getSetting('Enable-Meta')
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class="featuredlink" title=""\r\n\t\t\t\tonmouseover="vorschau\(\\\'ttfeatured\\\',true,\\\'(.+?)\s\(([\d]{4})\)').findall(link)
        for url,name,year in match:
                if 'season' in url:
                        addDir(name,url,17,'',None,year)
                else:
                        if EnableMeta == 'true':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),url,16,'','tvshow',year)
                        if EnableMeta == 'false':
                                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),url,16,'',None,year)
#Featured XXX
def FEATUREDXXX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div class="featuredlink">\r\n\t\t<a href="(.+?)" class="featuredlink" title=""\r\n\t\t\t\tonmouseover=".+?" \r\n\t\t\t\tonmouseout=".+?" \r\n\t\t\t\tonmousemove="vorschau\(\'ttfeatured\',true,\'(.+?)\',0,1\);"\r\n\t\t\t>\r\n\t\t\r\n\t\t\t<img class="featuredlink" alt=".+?" src=".+?">',re.DOTALL).findall(link)
        for url,name in match:
                name = name.replace('(Adult)', '')
                addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')

#Similar to                                
def SIMILAR(name,url):
        EnableMeta = local.getSetting('Enable-Meta')
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a class="newlinks" href="(.+?)" title="watch (.+?) online"').findall(link)
        for url,name in match:
            if 'movies' in url:
                if EnableMeta == 'true':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'','Movie','')
                if EnableMeta == 'false':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')
            else:
                if EnableMeta == 'true':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'','tvshow','')
                if EnableMeta == 'false':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,16,'',None,'')

#Comments                                
def COMMENTS(url):
        EnableMeta = local.getSetting('Enable-Meta')
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<td id=".+?" class="commentstext" style="word-wrap:break-word">(.+?)</td>').findall(link)
        if len(match) <= 0:
                        name = '[B][COLOR blue]Sorry no Comments have been left[/COLOR][/B]'
                        addDir(name,'','','',None,'')
        for name in match:
                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),'','','',None,'')
        
#ACTORS
def ACTORS(url,name):
        dialog = 'Please wait while loading Actors list.'
        actor = name
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title="watch (.+?) online">',re.DOTALL).findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create(dialog)
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Actors loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'',remaining_display)
        for url,name in match:
                match.sort()
                if name.startswith(actor):
                        addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,50,'',None,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Actors loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'',remaining_display)
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait

def XXXACTORS(url,name):
        dialog = 'Please wait while loading Pornstar list.'
        actor = name
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title="watch (.+?) online">',re.DOTALL).findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create(dialog)
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Pornstars loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'',remaining_display)
        for url,name in match:
                match.sort()
                if name.startswith(actor):
                    addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,50,'',None,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Actors loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'',remaining_display)
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait
        
def ACTORSLINKS(url,name):
        EnableMeta = local.getSetting('Enable-Meta')
        dialog = 'Please wait while finding moves with:' +name
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('href="(.+?)" title="watch (.+?) online"').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create(dialog)
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'',remaining_display)
        for url,name in match:
                if EnableMeta == 'true':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'','Movie','')
                if EnableMeta == 'false':
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'',remaining_display)
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait

#FORUMS
def FORUM(url):
        net.set_cookies(cookiejar)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('',re.DOTALL).findall(link)
        for url,name in match:
               addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,20,'',None,None)
               
def FORUMSMOVIE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class=" subject_new" id=".+?">(.+?)</a>').findall(link)
        nextpage=re.search('<a href="(.+?)" class="pagination_next">Next.+?</a>',(net.http_GET(url).content))
        for url,name in match:
                nono = ['Non-english movie list thread (updated)','Trailer BBcode','IMDB BBcode tags', 'MOVIE LINKS PLEASE READ', 'Forum Rules: Movie Links']
                if name not in str(nono):
                        addDir2(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_FORUMS+url,48,'','Movie','')
        if nextpage:
                url = nextpage.group(1)
                url = url.replace('&amp;', '&')
                addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',ALLUC_FORUMS+url,45,'',None,'')
        

def FORUMSTV(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class=" subject_new" id=".+?">(.+?)</a>').findall(link)
        nextpage=re.search('<a href="(.+?)" class="pagination_next">Next.+?</a>',(net.http_GET(url).content))
        for url,name in match:
                nono = ['Weekly WWE/TNA Shows & Monthly PPV','which sites can be linked?','Free Live tv from the world', 'Forum Rules: TV Links', 'Forum Rules: Movie Links', 'Important: Link-Hunters please read!', 'TV LINKS PLEASE READ']
                if name not in str(nono):
                        addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_FORUMS+url,48,'',None,'')
        if nextpage:
                url = nextpage.group(1)
                url = url.replace('&amp;', '&')
                addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',ALLUC_FORUMS+url,46,'',None,'')

def FORUMSDOC(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class=" subject_new" id=".+?">(.+?)</a>').findall(link)
        nextpage=re.search('<a href="(.+?)" class="pagination_next">Next.+?</a>',(net.http_GET(url).content))
        for url,name in match:
                nono = ['A List of Lists listing Documentaries','New Subforum ','BBC Horizon Collection (290+ Episodes)', 'Forum Rules: Documentaries']
                if name not in str(nono):
                        addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_FORUMS+url,48,'',None,'')
        if nextpage:
                url = nextpage.group(1)
                url = url.replace('&amp;', '&')
                addDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',ALLUC_FORUMS+url,47,'',None,'')

def FORUMSLINKS(url):
        unrestrict_account = local.getSetting('unrestrict-account')
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" target="_blank">').findall(link)
        for url in match:
                name = url
                if 'sockshare' in url:
                        if unrestrict_account == 'true':
                                un = "[B][COLOR purple]Unrestricted[/COLOR][/B]"
                                addDir("%s : %s"%(un,name),url,58,'',None,'')
                        else:
                                addDir(name,url,56,'',None,'')
                if 'movreel' in url:
                        addDir(name,url,56,'',None,'')
                if 'putlocker' in url:
                        if unrestrict_account == 'true':
                                un = "[B][COLOR purple]Unrestricted[/COLOR][/B]"
                                addDir("%s : %s"%(un,name),url,58,'',None,'')
                        else:
                                addDir(name,url,56,'',None,'')
                if 'filenuke' in url:
                        addDir(name,url,56,'',None,'')
                if 'billionuploads' in url:
                        addDir(name,url,56,'',None,'')
                if 'movshare' in url:
                        addDir(name,url,56,'',None,'')
                if 'uploadc' in url:
                        addDir(name,url,56,'',None,'')
                if '180upload' in url:
                        addDir(name,url,56,'',None,'')
                if 'vidxden' in url:
                        addDir(name,url,56,'',None,'')
                if 'vidhog' in url:
                        addDir(name,url,56,'',None,'')
                if 'vidbux' in url:
                        addDir(name,url,56,'',None,'')
                

#Seasons
def SEASONS(url,name):
        EnableMeta = local.getSetting('Enable-Meta')
        if EnableMeta == 'true': dialog = 'Please wait while Metadata is added.'
        if EnableMeta == 'false': dialog = 'Please wait while Seasons list is created.'
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a class="linklist2 linklist_header" style="font-weight:bold;padding-left:2px; width:auto;margin-bottom:2px;" \r\n\t\t\t\thref="(.+?)" title="watch (.+?) online">').findall(link) #"watch (.+?)\s\(([\d]{4})\)\s(.+?) online"
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create(dialog)
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Seasons loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'',remaining_display)
        for url,name in match:
                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,17,'',None,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Seasons loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'',remaining_display)
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait

#Episodes
def EPISODES(url,name):
        EnableMeta = local.getSetting('Enable-Meta')
        if EnableMeta == 'true': dialog = 'Please wait while Metadata is added.'
        if EnableMeta == 'false': dialog = 'Please wait while Episodes list is created.'
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a class="linklist2" style="font-weight:bold;padding-left:10px;width:auto;" \r\n\t\t\t\thref="(.+?)" title="watch (.+?) online">').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create(dialog)
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'',remaining_display)
        for url,name in match:
                addDir(name.decode('iso-8859-1').encode('UTF-8','ignore'),ALLUC_URL+url,18,'',None,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'',remaining_display)
                if (dialogWait.iscanceled()):
                        return False
        dialogWait.close()
        del dialogWait

#Get Videolinks passing special X variable and User Agent for special response from ALLUC to XBMC addon
def VIDEOLINKS(url):
        Enable_Streamcloud = local.getSetting('Enable-Streamcloud')
        unrestrict_account = local.getSetting('unrestrict-account')
        unrestrict_regaccount = local.getSetting('unrestrict-regaccount')
        unrestrict_guestaccount = local.getSetting('unrestrict-guestaccount')
        similar = url
        arg = { 'x':'1'}
        encoded_arg = urllib.urlencode(arg)
        req = urllib2.Request(url, encoded_arg)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.8.1.18) Gecko/22082049 Firefox/2.0.0.18')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addDir("[B][COLOR blue]Find Similar Movies[/COLOR][/B]",url,59,'',None,'')
        match=re.compile('[H](.+?)[L](.+?)\|(.+?)[U](.+?)[X]').findall(link) #'[H](.+?)[L].+?\|(.+?)[U](.+?)[X]'
        match2=re.compile('[H](.+?)[L](.+?)\|(.+?)\|(.+?)[U](.+?)[X]').findall(link)
        if 'tv-shows' in url:
            for name,sub,sub2,sub3,url in match2:
                name = name.replace(']','')
                name = name.replace('[','')
                url = url.replace(']','')
                url = url.replace('[','')
                sub = sub.replace(']','')
                sub = sub.replace('[','')
                sub3 = sub3.replace(']','')
                sub3 = sub3.replace('[','')
                sub = sub.replace('&quot;','"')
                sub = sub+' '+sub2+' '+sub3
                #List of allowed Hosters to show links for
                if Enable_Streamcloud == 'false':
                        hosters = ['Uptobox ','Ul','Billionuploads','Putlocker','Novamov','Sockshare','Filenuke','Movshare','Vidbux','Played','Movpod','Daclips','Movdivx','Vidhog','Vidbull','Divxstage','Zalaa','Movreel','Sharerepo','Uploadc','Sharesix','Watchfreeinhd','Videoweed','Vidxden','2gb-hosting']
                else:
                        hosters = ['Uptobox ','Streamcloud','Ul','Billionuploads','Putlocker','Novamov','Sockshare','Filenuke','Movshare','Vidbux','Played','Movpod','Daclips','Movdivx','Vidhog','Vidbull','Divxstage','Zalaa','Movreel','Sharerepo','Uploadc','Sharesix','Watchfreeinhd','Videoweed','Vidxden','2gb-hosting']
                if name in str(hosters):
                        if unrestrict_account == 'true':
                                unhosters = ['Uptobox ','Ul','Vimeo', 'Dailymotion ', 'Streamcloud', 'Putlocker', 'Sockshare']
                        elif unrestrict_regaccount == 'true':
                                unhosters = ['Uptobox ','Vimeo', 'Dailymotion ', 'Streamcloud', 'Putlocker', 'Sockshare']
                        elif unrestrict_guestaccount == 'true':
                                unhosters = ['Streamcloud']
                        else:
                                unhosters = ['Nono']
                        nono = ['']
                        if name not in str(nono):
                            un = "[B][COLOR purple]Unrestricted[/COLOR][/B]"
                            if name in str(unhosters):
                                    addDir("%s : %s : %s"%(un,name,sub),url+'@'+sub,58,'',None,'')
                            else:
                                    addDir("%s : %s"%(name,sub),url+'@'+sub,20,'',None,'')
                    
        else:
            for name,sub,desc,url in match:
                name = name.replace(']','')
                name = name.replace('[','')
                desc = desc.replace('[','')
                desc = desc.replace('[','')
                url = url.replace(']','')
                url = url.replace('[','')
                sub = sub.replace(']','')
                sub = sub.replace('[','')
                sub = sub.replace('&quot;','"')
                #List of allowed Hosters to show links for
                if Enable_Streamcloud == 'false':
                        hosters = ['Uptobox ','Ul','Billionuploads','Putlocker','Novamov','Sockshare','Filenuke','Movshare','Vidbux','Played','Movpod','Daclips','Movdivx','Vidhog','Vidbull','Divxstage','Zalaa','Movreel','Sharerepo','Uploadc','Sharesix','Watchfreeinhd','Videoweed','Vidxden','2gb-hosting']
                else:
                        hosters = ['Uptobox ','Vimeo','Ul','Dailymotion','Streamcloud','Billionuploads','Putlocker','Novamov','Sockshare','Filenuke','Movshare','Vidbux','Played','Movpod','Daclips','Movdivx','Vidhog','Vidbull','Divxstage','Zalaa','Movreel','Sharerepo','Uploadc','Sharesix','Watchfreeinhd','Videoweed','Vidxden','2gb-hosting']
                
                if name in str(hosters):
                        if unrestrict_account == 'true':
                                unhosters = ['Uptobox ','Ul','Vimeo', 'Dailymotion ', 'Streamcloud', 'Putlocker', 'Sockshare']
                        elif unrestrict_regaccount == 'true':
                                unhosters = ['Uptobox ','Vimeo', 'Dailymotion ', 'Streamcloud', 'Putlocker', 'Sockshare']
                        elif unrestrict_guestaccount == 'true':
                                unhosters = ['Streamcloud']
                        else:
                                unhosters = 'Nope'
                        nono = ['']
                        if name not in str(nono):
                                un = "[B][COLOR purple]Unrestricted[/COLOR][/B]"
                                if name in str(unhosters):
                                        addDir("%s : %s : %s"%(un,name,desc),url+'@'+sub,58,'',None,'')
                                else:
                                        addDir("%s : %s"%(name,desc),url+'@'+sub,20,'',None,'')

#Resolve Movie and TV links
def STREAM(url):
        name = url.split('@')[1]
        url = url.split('@')[0]
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
        print streamlink
        addLink(name,streamlink,'')
        #except:
        #        silent.Notify('small','Link Removed:', 'Please try another one.',6000)

#Resolve Forum links
def STREAM2(url):
                req = urllib2.Request(url)
                req.add_header('User-Agent', USER_AGENT)
                streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
                print streamlink
                addLink(name,streamlink,'')
            #except:
            #    silent.Notify('small','Link Removed:', 'Please try another one.',6000)

#Resolve Unristricted links
def UNSTREAM(url):
        try:
            name = url.split('@')[1]
        except:
            name = url
        try:
            url = url.split('@')[0]
        except:
            url = url
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', USER_AGENT)
            streamlink = urllib2.urlopen(req).url
            UNLINK(streamlink)
        except urllib2.HTTPError, e:
            streamlink = e.url
            UNLINK(streamlink)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,iconimage):        
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('Video', infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok
        
def addDir(name,url,mode,iconimage,types,year):
        ok=True
        type = types   
        if type != None:
                infoLabels = GRABMETA(name,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        contextMenuItems = []
        if mode == 20 or mode == 58:
                contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=61&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if mode == 18 or mode == 16:
                contextMenuItems.append(('Add to Favorites', 'XBMC.RunPlugin(%s?mode=71&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
                liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

#addDir with find similar movie context menu
def addDir2(name,url,mode,iconimage,types,year):
        EnableFanArt = local.getSetting('Enable-Fanart')
        EnableMeta = local.getSetting('Enable-Meta')
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = GRABMETA(name,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except:img = iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        #####get xxx image or pass to ''
        if 'adult' in url:
                if EnableMeta == 'true':
                        try: img=re.compile('<meta property="og:image" content="(.+?)" />').findall(net.http_GET(url).content)[0]
                        except: img = ''
        ###############################
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        try:liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        except: liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png")
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        contextMenuItems = []
        if mode == 18 or mode == 16:
                contextMenuItems.append(('Add to Favorites', 'XBMC.RunPlugin(%s?mode=71&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if 'movies' in url:
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if 'tv-shows' in url:
            contextMenuItems.append(('TV-Show Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if 'movies' in url:
            contextMenuItems.append(('Find Similar Movies', 'XBMC.Container.Update(%s?mode=59&name=%s&url=%s)' % (sys.argv[0], name, url)))
            liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if 'tv-shows' in url:
            contextMenuItems.append(('Find Similar TV-Shows', 'XBMC.Container.Update(%s?mode=59&name=%s&url=%s)' % (sys.argv[0], name, url)))
            liz.addContextMenuItems(contextMenuItems, replaceItems=False)

        contextMenuItems.append(('View Comments', 'XBMC.Container.Update(%s?mode=60&name=%s&url=%s)' % (sys.argv[0], name, url)))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
#addDir for Fourm links
def addDir3(name,url,mode,iconimage,types,year):
        ok=True
        type = types
        try:
            match=re.search('http://www.imdb.com/title/(.+?)/',(net.http_GET(url).content))
            imdb = match
            print imdb
        except: imdb = ''
        if type != None:
                infoLabels = GRABMETA2(imdb,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        contextMenuItems = []
        if mode == 20 or mode == 58:
                contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=61&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addFAVDir(name,url,types):
        EnableFanArt = local.getSetting('Enable-Fanart')
        if types == 'Movie':
                mode = 18
        if types == 'tvshow':
                mode = 16
        ok=True
        type = types
        fimg = addon.get_fanart()
        if type != None:
                infoLabels = GRABMETA(name,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        if EnableFanArt == 'true':
                try:    fimg = infoLabels['backdrop_url']
                except: fimg = addon.get_fanart()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        contextMenuItems = []
        contextMenuItems.append(('Remove from Favorites', 'XBMC.RunPlugin(%s?mode=72&name=%s&url=%s&types=%s)' % (sys.argv[0], name, urllib.quote_plus(url), types)))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        

params=get_params()
url=None
name=None
mode=None
types=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        types=params["types"]
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        
elif mode==1:
        MOVIES()

elif mode==2:
        print ""+url
        MOVIESAZ(url)

elif mode==3:
        print ""+url
        MOVIESGEN(url)

elif mode==4:
        TVSHOWS()

elif mode==5:
        ANIME()

elif mode==6:
        CARTOONS()

elif mode==7:
        DOCUMENTARIES()

elif mode==8:
        print ""+url
        DOCUMENTARIESAZ(url)

elif mode==9:
        print ""+url
        DOCUMENTARIESGEN(url)

elif mode==10:
        SPORTS()

elif mode==11:
        print ""+url
        SPORTSAZ(url)

elif mode==12:
        print ""+url
        SPORTSGEN(url)

elif mode==13:
        print ""+url
        INDEX1(url)
        
elif mode==14:
        print ""+url
        INDEX2(url)

elif mode==15:
        print ""+url
        INDEX3(url)

elif mode==16:
        print ""+url
        SEASONS(url,name)

elif mode==17:
        print ""+url
        EPISODES(url,name)

elif mode==18:
        print ""+url
        VIDEOLINKS(url)

elif mode==19:
        print ""+url
        TVSHOWSAZ(url)

elif mode==20:
        print ""+url
        STREAM(url)

elif mode==21:
        ADULT()

elif mode==22:
        print ""+name
        UNIVERSALSEARCH(name)
        
elif mode==23:
        print ""+url
        ADULTAZ(url)
        
elif mode==24:
        print ""+url
        ADULTGEN(url)

elif mode==25:
        print ""+url
        FEATURED(url)

elif mode==26:
        print ""+url
        FEATUREDTV(url)
                                 
elif mode==27:
        print ""+url
        SIMILAR(url)

elif mode==28:
        SEARCHMOVIES()

elif mode==29:
        SEARCHTV()

elif mode==30:
        print ""+url
        ANIMEAZ(url)

elif mode==31:
        SEARCHANIME()

elif mode==32:
        print ""+url
        CARTOONSAZ(url)

elif mode==33:
        SEARCHCARTOON()

elif mode==34:
        SEARCHDOCUMENTARIES()

elif mode==35:
        SEARCHADULT()

elif mode==36:
        print ""+url
        FINDSID(url)

elif mode==37:
        print ""+url
        MESSAGES(url)

elif mode==38:
        print ""+url
        READMESSAGES(url)

elif mode==39:
        print ""+url
        OTHERWATCHLIST(url)

elif mode==40:
        print ""+url
        MYWATCHLIST(url)

elif mode==41:
        print ""+url
        FORUM(url)

elif mode==42:
        print ""+url
        UNRESTRICT(url)

elif mode==43:
        print ""+url
        UNCHECK(url)

elif mode==44:
        FORUMS()

elif mode==45:
        print ""+url
        FORUMSMOVIE(url)

elif mode==46:
        print ""+url
        FORUMSTV(url)

elif mode==47:
        print ""+url
        FORUMSDOC(url)

elif mode==48:
        print ""+url
        FORUMSLINKS(url)

elif mode==49:
        print ""+url
        ACTORS(url,name)

elif mode==50:
        print ""+url
        ACTORSLINKS(url,name)

elif mode==51:
        SEARCH()

elif mode==52:
        print ""+url
        UNTRY(url)

elif mode==53:
        ACTORSDIR()

elif mode==54:
        ACTORSAZ()

elif mode==55:
        ACTORSEARCH()

elif mode==56:
        STREAM2(url)

elif mode==57:
        UNLINK(url)

elif mode==58:
        UNSTREAM(url)

elif mode==59:
        SIMILAR(name,url)

elif mode==60:
        COMMENTS(url)

elif mode==61:
        DOWNLOADINFO(name,url)

elif mode==62:
        SETTINGS()

elif mode==63:
        ResolverSettings()

elif mode==64:
        VIPSTATUS()

elif mode==65:
        GETMYFAVS()

elif mode==66:
        OPENDOWNLOADS()

elif mode==67:
        XXXACTORS(url,name)

elif mode==68:
        FEATUREDXXX(url)

elif mode==69:
        INDEX4(url)

elif mode==70:
        ADULTA()

elif mode==71:
        print ""+url
        silent.addFavorite(name,url,types)

elif mode==72:
        print ""+url
        silent.removeFavorite(name,url,types)

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

