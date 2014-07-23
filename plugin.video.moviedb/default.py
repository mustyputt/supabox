
#Default moviedb - Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys, os.path
import urlresolver
import cookielib
from resources.modules import status
import downloader
import extract
import time,re
import datetime
import shutil
from resources.modules import tvshow, ninestreams
from metahandler import metahandlers
from resources.modules import main,flix,sgmovie
from resources.modules import moviedc, afdah
from resources.modules import sgate,streamlic
from resources.modules import chia, supertoons, phub
from resources.modules import chanufc, epornik, live
from resources.utils import autoupdate
from resources.utils import buggalo
from resources.modules import oneeighty,iwo
from resources.sports import espn

from addon.common.addon import Addon
from addon.common.net import Net
net = Net(http_debug=True)
        
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
xmlpath = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/messages/skins/DefaultSkin/720p/'





try:
     from sqlite3 import dbapi2 as lite
except:
     from pysqlite2 import dbapi2 as lite

newagent ='Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
net.set_user_agent(newagent)

base_url = 'http://www.merdb.ru/'


#PATHS
buggalo.GMAIL_RECIPIENT ='blazetamer@gmail.com'
datapaths = xbmc.translatePath(ADDON.getAddonInfo('profile'))
UpdatePath=os.path.join(datapaths,'Update')
try: os.makedirs(UpdatePath)
except: pass
StreamPath=os.path.join(datapaths,'Stream Files')
try: os.makedirs(StreamPath)
except: pass
CookiesPath=os.path.join(datapaths,'Cookies')
try: os.makedirs(CookiesPath)
except: pass
DownloadPath=os.path.join(datapaths,'Downloads')
try: os.makedirs(DownloadPath)
except: pass
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg', ''))
else:
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart/fanart.jpg', ''))

addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')

#========================Alternate Param Stuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
repourl = addon.queries.get('repourl', '')
gomode = addon.queries.get('gomode', '')
page = addon.queries.get('page', '')
key = addon.queries.get('key', '')
#======================== END Alternate Param Stuff=======================

#========================Advanced Log Stuff=======================
if settings.getSetting('debug') == 'true':
        print 'Mode is: ' + mode
        print 'Url is: ' + url
        print 'Name is: ' + name
        print 'Thumb is: ' + thumb
        print 'Extension is: ' + ext
        print 'Filetype is: ' + console
        print 'DL Folder is: ' + dlfoldername
        print 'Favtype is: ' + favtype
        print 'Main Image is: ' + mainimg
        print 'Headers are ' +headers
        print 'Logged In Status is ' +loggedin
        print 'RepoUrl is ' +repourl
#======================== END Advanced Log Stuff=======================        
        
#########################Blazetamer's Startup Module########################################

cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def UPLOADLOGFILE():
    from resources.modules import logup
    logup.LogUploader()
        
def STARTUP():
        myversion=CheckVersion()
        if myversion == True:
                        print 'Version is TRUE'
        
        if myversion ==False:
                        print 'Version is FALSE'
        CHECK_POPUP()
        
def CheckVersion():
   try:        
    curver=xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviedb/','addon.xml'))    
    source= open( curver, mode = 'r' )
    link = source . read( )
    source . close ( )
    match=re.compile('" version="(.+?)" name="Cliq!"').findall(link)
    for vernum in match:
            print 'Original Version is ' + vernum
    try:
        link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/cliqupdate/master/addon.xml')
    except:
        link='nill'

    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('" version="(.+?)" name="Cliq!"').findall(link)
    if len(match)>0:
        if vernum != str(match[0]):
                dialog = xbmcgui.Dialog()
                confirm=xbmcgui.Dialog().yesno('[B]CLIQ Update Available![/B]', "                              Your version is outdated." ,'                    The current available version is '+str(match[0]),'                         Would you like to update now?',"Cancel","Update")
                #return False
                if confirm:
                        autoupdate.UPDATEFILES()
                return False
        else:
                return True
    
    else:
        return False
   except Exception:
        buggalo.onExceptionRaised()



def SPECIALANN():
   try:        

        link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/popupdate.txt').replace('\n','').replace('\r','')
        
        match=re.compile('ate="(.+?)"').findall(link)
        for popdate in match: 
                now   = datetime.date.today()
                today = str(now)
                print 'TODAY IS ' + today
                if settings.getSetting('announce') == 'true':
                         if today == popdate:
                               threshold = int(settings.getSetting('anno_intcliq') ) - 1
                               now   = datetime.datetime.today()
                               prev  = CHECKDATE(settings.getSetting('pop_time'))
                               delta = now - prev
                               nDays = delta.days

                               doUpdate = (nDays > threshold)
                               if  not doUpdate:
                                       CATEGORIES('false')
                               elif doUpdate:        
                                      settings.setSetting('pop_time', str(now).split('.')[0])
                                      status.ADDONSTATUS('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/announcepop.txt')
                                      CATEGORIES('false')
                         else:CATEGORIES('false')        
              
                else :CATEGORIES('false')
   except Exception:
        CATEGORIES('false')
        #buggalo.onExceptionRaised()
        

def CHECK_POPUP():
   try:
        if settings.getSetting('announce') == 'true':          
                        SPECIALANN()
        if settings.getSetting('announce') == 'false':                
                        CATEGORIES('false')
   except Exception:
        buggalo.onExceptionRaised()                
                                                  
#************************End Stratup****************************************************************************



def CATEGORIES(loggedin):
   try:        
        if settings.getSetting('adult') == 'true':
                text_file = None
                if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/")):
                        os.makedirs(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/"))

                if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/apc.69")):
                        pin = ''
                        notice = xbmcgui.Dialog().yesno('Would You Like To Set an Adult Passcode','Would you like to set a passcode for the adult movies section?','','')
                        if notice:
                                keyboard = xbmc.Keyboard(pin,'Choose A New Adult Movie Passcode')
                                keyboard.doModal()
                                if keyboard.isConfirmed():
                                        pin = keyboard.getText()
                                text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/apc.69"), "w")
                                text_file.write(pin)
                                text_file.close()
                        else:
                                text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.moviedb/apc.69"), "w")
                                text_file.write(pin)
                                text_file.close()
                live.addDir('Adults Only','none','adultcats',artwork +'adult.jpg','18+ Only - Adult Rated Video Section',fanart)
                
        live.addDir('Movies','none','moviecat',artwork +'movies.jpg','Movies from several popular source sites such as MerDb and Datacenter movies',fanart)
        live.addDir('TV Shows','none','tvcats',artwork +'tvshows.jpg','TV Shows from several popular source sites such as MerDb and Series Gate',fanart)
        if settings.getSetting('toons') == 'true':
                live.addDir('Cartoons','none','cartooncats',artwork +'cartoons.jpg','Cartoons galore, Includes Anime from Chia-Anime and Cartoons from SuperToons',fanart)
        if settings.getSetting('sports') == 'true':        
                live.addDir('Sports','none','sportcats',artwork +'sports.jpg','Sports such as UFC and more!',fanart)
        if settings.getSetting('streams') == 'true':        
                live.addDir('Live Streams','https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/streams/menus.xml','livecats',artwork +'live.jpg','Live streams from around the globe, User Sumbitted streams are also available, Be sure to check the special events section!!',fanart)        
        #live.addDir('User Submitted Playlists' ,'http://goo.gl/JQzOhw','database',artwork +'submitted.jpg','User Submitted Playlists ',fanart)
        #==============Custom Menu Creation======================================
        try:        
             link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/mainmenu.xml').replace('\n','').replace('\r','')
             match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
             for name,url,thumb,mode,desc in match:
                     print 'Description is  ' + desc
                     live.addDir(name,url,mode,thumb,desc,fanart)
        except: pass        
        #==============End Custom Menu Creation==================================
        live.addDir('CLIQ Favorites','none','viewstfavs',artwork +'mdbfavs.jpg','Manage and View your  Favorite Lists Here',fanart)        
        live.addDir('Manage Downloads','none','viewQueue',artwork +'downloadsmanage.jpg','Manage your download queue, Start, stop and or remove items from the Queue',fanart)
        live.addDir('Upload Logfile','none','uploadlogfile',artwork +'uploadlog.jpg','Need to upload a logfile? Here is the place to do it, Set your email from the addon settings area if you want a link emailed to you. .',fanart)
        live.addDir('Display Latest Announcement(s)','https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/announcepop.txt','addonstatus',artwork +'announcements.jpg','In case you missed the latest announcements, You can view them manually here.',fanart)
        if settings.getSetting('resolver') == 'true':
                live.addDir('Resolver Settings','none','resolverSettings',artwork +'resolversettings.jpg','Adjust your resolver settings here',fanart)
        if settings.getSetting('addons') == 'true':        
                live.addDir('More Addons by Blazetamer','http://addons.xbmchub.com/author/Blazetamer/','addonlist',artwork +'moreaddons.jpg','Check out and install more of my add-ons here.',fanart)
                #live.addDir('[COLOR blue]Get the Addon Browser Here[/COLOR]','http://addons.xbmchub.com/search/?keyword=browser','addonlist',artwork +'addonbrowser.jpg','Need the legendary Addon Browser?  Get it now!!',fanart)
        #if settings.getSetting('special') == 'true':        
                #live.addDir('[COLOR blue]Special Menus/Extras[/COLOR]','none','pop',artwork +'specialmenu.jpg','View Special Menus and more',fanart)
#======================Developer Testing Section========================================================================
        #live.addDir('[COLOR blue]Test Update[/COLOR]','none','updatefiles','','','')
        #live.addDir('[COLOR blue]Test Functions[/COLOR]','none','testfunction',artwork +'shutdown.png','','dir')
        #live.addDir('[COLOR blue]Whats My IP[/COLOR]','none','myip',artwork +'myip.png','','dir')      
        live.addDir('[COLOR gold]My Custom Streams[/COLOR]','none','nineindex',artwork +'customs.png','','dir')        
        live.addDir('[COLORgold]Testing Tools[/COLOR]','none','ninetools',artwork +'tools.png','','dir')
        main.AUTO_VIEW('')
   except Exception:
        buggalo.onExceptionRaised()

        
################################
###          My IP           ###
################################

def MYIP():
    url = 'http://www.iplocation.net/'
    match = re.compile("<td width='80'>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>.+?</td><td>(.+?)</td>").findall(net.http_GET(url).content)
    inc = 1
    for ip, region, country, isp in match:
            if inc <2:
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Cliq Knows!", "[B][COLOR gold]Your IP Address is: [/COLOR][/B] %s" % ip, '[B][COLOR gold]Your IP is based in: [/COLOR][/B] %s' % country, '[B][COLOR gold]Your Service Provider is:[/COLOR][/B] %s' % isp)
            inc = inc+1

################################
###        End My IP         ###
################################

def TESTFUNCTION():
     
     #testwin = MyClass('skin.xml','https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/','DefaultSkin')
     testwin = MyClass('skin.xml',ADDON.getAddonInfo('path'),'DefaultSkin')    
     testwin.doModal()
     del testwin
     
                
class MyClass( xbmcgui.WindowXMLDialog ): 
    def __init__( self, *args, **kwargs ):
        #self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    '''def onInit( self ):
        #xbmc.Player().play('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/getit.mp3'%ADDON.getAddonInfo('path'))# Music.
        #xbmc.Player().play('https://ia700200.us.archive.org/1/items/testmp3testfile/mpthreetest.mp3')# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut = 10
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog() 

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()
        if action == ACTION_PREVIOUS_MENU:
           self.close() '''   

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()     
                        
                     
            
        
def SHUTDOWNXBMC():
        xbmc.executebuiltin('XBMC.ActivateWindow(111)')

def ALLFAVS():
        live.addDir('iLive Favorites','none','viewfavs',artwork +'livefav.jpg','Manage and View your Favorite Live Streams',artwork +'livefav.jpg')
        live.addDir('Other CLIQ Favorites','none','viewstfavs',artwork +'mdbfavs.jpg','Manage and View your  Favorite Lists Here',artwork +'mdbfavs.jpg')

def MERDBMOVIES():
   try:        
        main.addDir('All Movies','http://www.merdb.ru/','movieindex',artwork +'all.jpg','','dir')
        main.addDir('Featured Movies','http://www.merdb.ru/?featured=1&sort=stamp','movieindex',artwork +'featured.jpg','','dir')
        main.addDir('Movies by Popularity','http://www.merdb.ru/?sort=views','movieindex',artwork +'popular.jpg','','dir')
        main.addDir('Movies by Rating','http://www.merdb.ru/?sort=ratingp','movieindex',artwork +'rating.jpg','','dir')
        main.addDir('Movies by Genre','none','genres',artwork +'genre.jpg','','dir')
        main.addDir('Movies by Release Date','http://www.merdb.ru/?sort=year','movieindex',artwork +'releasedate.jpg','','dir')
        main.addDir('Movies by Date Added','http://www.merdb.ru/?sort=stamp','movieindex',artwork +'dateadded.jpg','','dir')
        main.addDir('[COLOR blue]Search Movies[/COLOR]','http://www.merdb.ru/?search=','searchm',artwork + 'search.jpg','','dir')
        main.AUTO_VIEW('')
   except Exception:
        buggalo.onExceptionRaised()        
        
        

                       
def MOVIECAT():
        live.addDir('Afdah Movies','none','afdahcats',artwork +'afdahmovies.jpg','',fanart)
        live.addDir('MerDB ','none','merdbmovies',artwork +'merdbmovies.jpg','',fanart)
        live.addDir('SeriesGate Movies ','none','sgmoviecats',artwork +'sgatetv.jpg','',fanart)
        live.addDir('Movie DataCenter[COLOR red]OFFLINE[/COLOR]','none','moviedccats',artwork +'moviedcmovies.jpg','',fanart)
        live.addDir('IWatchOnline','none','catiwo',artwork +'iwatchonline.jpg','',fanart)
        live.addDir('ZMovies','none','catzeemovies',artwork +'zmovies.jpg','',fanart)
        live.addDir('PopcornFlix','none','popcats',artwork +'popcornflix.jpg','',fanart)
        #==============Custom Menu Creation======================================
        try:
             link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/moviemenu.xml').replace('\n','').replace('\r','')
             match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
             for name,url,thumb,mode,desc in match:
                     live.addDir(name,url,mode,thumb,desc,fanart)
        except: pass            
        #==============End Custom Menu Creation==================================
        
        
        
        main.AUTO_VIEW('')

def TVCATS():        
        live.addDir('TV Shows [COLOR red](MerDB)[/COLOR]','none','merdbtvcats',artwork +'merdbtv.jpg','',fanart)
        live.addDir('TV Shows [COLOR red](Series Gate)[/COLOR]','none','sgcats',artwork +'sgatetv.jpg','',fanart)
        #==============Custom Menu Creation======================================
        try:
             link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/tvmenu.xml').replace('\n','').replace('\r','')
             match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
             for name,url,thumb,mode,desc in match:
                     live.addDir(name,url,mode,thumb,desc,fanart)
        except: pass            
        #==============End Custom Menu Creation==================================
        
        main.AUTO_VIEW('')
  
def CARTOONCATS():
        live.addDir('[COLOR white]Chia-Anime[/COLOR]','none','chiacats',artwork +'chiaanime.jpg','',fanart)
        live.addDir('[COLOR white]SuperToons[/COLOR]','none','supertoonscats',artwork +'supertoons.jpg','',fanart)
        #==============Custom Menu Creation======================================
        try:
             link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/cartoonmenu.xml').replace('\n','').replace('\r','')
             match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
             for name,url,thumb,mode,desc in match:
                     live.addDir(name,url,mode,thumb,desc,fanart)
        except: pass            
        #==============End Custom Menu Creation==================================
        
def SPORTCATS():
        #live.addDir('UFC','none','chanufccats',artwork +'ufc.jpg','',fanart)
        live.addDir('ESPN','none','espnmain',artwork +'espn.jpg','',fanart)
        #==============Custom Menu Creation======================================
        try:
             link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/sportsmenu.xml').replace('\n','').replace('\r','')
             match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
             for name,url,thumb,mode,desc in match:
                     live.addDir(name,url,mode,thumb,desc,fanart)
        except: pass            
        #==============End Custom Menu Creation==================================
        
def ADULTCATS():
        live.addDir('[COLOR white]PornHub[/COLOR]','none','phcategories',artwork +'pornhub.png','',fanart)
        live.addDir('[COLOR white]Eporn[/COLOR]','none','epornikCategories',artwork +'eporn.jpg','',fanart)
        
        

def GENRES():
   try:        
        genurl = 'http://www.merdb.ru/?genre='
        live.addDir('Action',genurl +'Action','movieindex',artwork +'action.jpg','',fanart)
        live.addDir('Adventure',genurl +'Adventure','movieindex',artwork +'adventure.jpg','',fanart)
        live.addDir('Animation',genurl +'Animation','movieindex',artwork +'animation.jpg','',fanart)
        live.addDir('Biography',genurl +'Biography','movieindex',artwork +'biography.jpg','',fanart)
        live.addDir('Comedy',genurl +'Comedy','movieindex',artwork +'comedy.jpg','',fanart)
        live.addDir('Crime',genurl +'Crime','movieindex',artwork +'crime.jpg','',fanart)
        live.addDir('Documentary',genurl +'Documentary','movieindex',artwork +'documentary.jpg','',fanart)
        live.addDir('Drama',genurl +'Drama','movieindex',artwork +'drama.jpg','',fanart)
        live.addDir('Family',genurl +'Family','movieindex',artwork +'family.jpg','',fanart)
        live.addDir('Fantasy',genurl +'Fantasy','movieindex',artwork +'fantasy.jpg','',fanart)
        live.addDir('History',genurl +'History','movieindex',artwork +'history.jpg','',fanart)
        live.addDir('Horror',genurl +'Horror','movieindex',artwork +'horror.jpg','',fanart)
        live.addDir('Music',genurl +'Music','movieindex',artwork +'music.jpg','',fanart)
        live.addDir('Mystery',genurl +'Mystery','movieindex',artwork +'mystery.jpg','',fanart)
        live.addDir('Romance',genurl +'Romance','movieindex',artwork +'romance.jpg','',fanart)
        live.addDir('Sci-Fi',genurl +'Sci-Fi','movieindex',artwork +'scifi.jpg','',fanart)
        live.addDir('Thriller',genurl +'Thriller','movieindex',artwork +'thriller.jpg','',fanart)
        live.addDir('War',genurl +'War','movieindex',artwork +'western.jpg','',fanart)
        
        main.AUTO_VIEW('')
   except Exception:
        buggalo.onExceptionRaised()        

             
def MOVIEINDEX(url):
   try:        
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" class=".+?" alt=".+?"/></a><div class=".+?"><a href="(.+?)" title="Watch(.+?)">.+?</a>').findall(link)
        if len(match) > 0:
         for sitethumb,url,name in match:
                
                inc = 0
                movie_name = name[:-6]
                year = name[-6:]
                movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABMETA(movie_name,year)
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               

                favtype = 'movie'
                main.addDir(name,base_url + url,'linkpage',thumb,data,favtype)
                
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                     
                main.addDir('Page'+ pageno,base_url + pageurl,'movieindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()        

                 
def MOVIEINDEX1(url):
   try:        
        link = net.http_GET(url).content
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" class=".+?" alt=".+?"/></a><div class=".+?"><a href="(.+?)" title="Watch(.+?)">.+?</a>').findall(link)
        if len(match) > 0:
         for sitethumb,url,name in match:
                 try:     
                         inc = 0
                         movie_name = name[:-6]
                         year = name[-6:]
                         movie_name = movie_name.decode('UTF-8','ignore')
              
                         data = main.GRABMETA(movie_name,year)
                         thumb = data['cover_url']               
                         yeargrab = data['year']
                         year = str(yeargrab)
                 except:
                         data = ''
                         thumb = sitethumb
                         year = year
         favtype = 'movie'
                  #if 'watch_movie' in url:
         try:        
                   main.addDir(name,base_url + url,'linkpage',thumb,data,favtype)
         except:
                   pass
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0:
                for pageurl,pageno in nmatch:
                      main.addDir('Page'+ pageno,base_url + pageurl,'movieindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()        

             

def LINKPAGE(url,name):
   try:        
        inc = 0
        movie_name = name[:-6]
        year = name[-6:]
        movie_name = movie_name.decode('UTF-8','ignore')
        dlfoldername = name
        link = net.http_GET(url).content
        match=re.compile('<span class="movie_version_link"> <a href="/(.+?)"').findall(link)
  
        for url in match:
         url = base_url + url
              
            
                   
         if inc < 50:
                 link = net.http_GET(url).content
                 hostmatch=re.compile('name="bottom" src="(.+?)"/>\n</frameset>').findall(link)        
                 for urls in hostmatch:
                   print 'Pre HMF url is  ' +urls
                   hmf = urlresolver.HostedMediaFile(urls)
                  ##########################################
                   print 'URLS is ' +urls
                   if hmf:
                          #try:
                                  host = hmf.get_host()
                                  hthumb = main.GETHOSTTHUMB(host)
                                  #dlurl = urlresolver.resolve(vidUrl)
                                  data = main.GRABMETA(movie_name,year)
                                  thumb = data['cover_url']
                                  favtype = 'movie'
                                  mainimg = thumb
                                  hostname = main.GETHOSTNAME(host)
                                  try:
                                          main.addDLDir(movie_name+'[COLOR lime]'+hostname+'[/COLOR]',urls,'vidpage',hthumb,data,dlfoldername,favtype,mainimg)
                                          inc +=1
                                  except:
                                          continue
                          #except:
                                  #pass
   except Exception:
        buggalo.onExceptionRaised()                                        
                   


def VIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
        url = url
        name = name
        thumb=mainimg
                
        main.RESOLVE2(name,url,thumb)


def DLVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
        main.RESOLVEDL(name,url,thumb)

def DLSPECIAL(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
        main.SPECIALDL(name,url,thumb)        
                
                



            
                

	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCHM(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for Movies" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	MOVIEINDEX(searchUrl)

	main.AUTO_VIEW('movies')



	
def SEARCHT(url):
	searchUrl = url 
	vq = _get_keyboard( heading="TIME INTENSIVE!! Be Patient!!" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=tag' 
	print "Searching URL: " + searchUrl 
	MOVIEINDEX1(searchUrl)

	main.AUTO_VIEW('movies')        

                
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


#==============POP UP FUNCTION==================
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link


def ADVERT():
          
      if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = PUM('advert1.xml','https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/','DefaultSkin')
      elif xbmc.getCondVisibility('system.platform.android'):
        popup = PUM('advert1.xml','https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/','DefaultSkin')
      else:
        popup = PUM('advert.xml','https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/','DefaultSkin')

      popup.doModal()
      del popup


def POP():
     link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/controls/xmlcontrol.txt').replace('\n','').replace('\r','')
     match=re.compile('ame="(.+?)".+?ndroid="(.+?)"').findall(link)
     for xml,xmlone in match:       
                #status.ADDONSTATUS(url) 
    

    
      if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = PUM(xmlone,'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/','DefaultSkin')
      elif xbmc.getCondVisibility('system.platform.android'):
        popup = PUM(xmlone,'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/','DefaultSkin')
      else:
        popup = PUM(xml,'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/','DefaultSkin')

      popup.doModal()
      del popup
    
        
    
                
def CHECKDATE(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1000) #force update



                           

class PUM( xbmcgui.WindowXMLDialog ): 
    #def __init__( self, *args, **kwargs ):
    def __init__( self, *args ):
        #self.shut = kwargs['close_time']   
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
        
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()


def RESETPOPUP():
        settings.setSetting('pop_time', '2000-01-02 00:00:00')
        return

        
#==============END POP UP FUNCTION===============



              
params=get_params()
url=None
name=None
mode=None
year=None
imdb_id=None

#------added for Help Section
try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

try:        
        thumb=urllib.unquote_plus(params["thumb"])
except:
        pass

try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

try:        
        filetype=urllib.unquote_plus(params["filetype"])
except:
        pass    

# END OF HelpSection addition ===========================================
    
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
#May need toremove
#try:
 #       mode=int(params["mode"])
#except:
 #       pass

try:
        mode=urllib.unquote_plus(params["mode"])
except:
        pass

try:
        year=urllib.unquote_plus(params["year"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Year: "+str(year)


if mode==None or url==None or len(url)<1:
        print ""
        STARTUP()
        
elif mode=='categories':
        print ""+loggedin
        CATEGORIES(loggedin)

elif mode=='login':
        print ""+url
        LOGIN(url)

elif mode=='relogin':
        print ""
        RELOGIN()          

        
elif mode=='helpmenu':
        print ""
        HELPMENU()

elif mode == "help list menu": 
        items = HELP(name)

elif mode == "wizardstatus":
        print""+url    
        items = WIZARDSTATUS(url)        


        
elif mode=='moviecat':
        print ""
        MOVIECAT()
        
elif mode=='merdbmovies':
        print ""
        MERDBMOVIES()  
        

elif mode=='tvcats':
        print ""
        TVCATS()

elif mode=='cartooncats':
        print ""
        CARTOONCATS()

elif mode=='sportcats':
        print ""
        SPORTCATS()

elif mode=='adultcats':
        print ""
        ADULTCATS()        

elif mode=='merdbtvcats':
        print ""
        tvshow.MERDBTVCATS()        


elif mode=='adultallow':
        print ""
        ADULTALLOW()        
        
elif mode=='byyear':
        print ""
        BYYEAR()
        
elif mode=='tvbyyear':
        print ""
        tvshow.TVBYYEAR()
        


elif mode=='genres':
        print ""
        GENRES()

elif mode=='tvgenres':
        print ""
        tvshow.TVGENRES()


        
elif mode=='mazindex':
        print ""
        MAZINDEX() 
        

        
elif mode=='playyear':
        print ""+url
        PLAYYEAR(url)


elif mode=='tvindex':
        print ""+url
        tvshow.TVINDEX(url)

        

elif mode=='tvplaygenre':
        print ""+url
        tvshow.TVPLAYGENRE(url)        

        
elif mode=='adultmovieindex':
        print ""+url
        ADULTMOVIEINDEX(url)

        
elif mode=='movieindex':
        print ""+url
        MOVIEINDEX(url)

elif mode=='lateshow':
        print ""+url
        tvshow.LATESHOW(url)

elif mode=='searchshow':
        print ""+url
        tvshow.SEARCHSHOW(url)        

elif mode=='movietagindex':
        print ""+url
        MOVIETAGINDEX(url)        

elif mode=='movieindex1':
        print ""+url
        MOVIEINDEX1(url)

elif mode=='azindex':
        print ""+url
        AZINDEX(url)        

elif mode=='movietags':
        print ""+url
        MOVIETAGS(url)        
        
elif mode=='vidpage':
        print ""+url
        VIDPAGE(url,name)


elif mode=='dlvidpage':
        print ""+url
        DLVIDPAGE(url,name)

elif mode=='dlspecial':
        print ""+url
        DLSPECIAL(url,name)        

elif mode=='dltvvidpage':
        print ""+url
        tvshow.DLTVVIDPAGE(url,name)        


elif mode=='tvvidpage':
        print ""+url
        tvshow.TVVIDPAGE(url,name)



elif mode=='linkpage':
        print ""+url
        LINKPAGE(url,name)

elif mode=='azlinkpage':
        print ""+url
        tvshow.AZLINKPAGE(url,name)        

elif mode=='tvlinkpage':
        print ""+url
        tvshow.TVLINKPAGE(url,name,thumb,mainimg)

elif mode=='episodes':
        print ""+url
        tvshow.EPISODES(url,name,thumb)
       

elif mode=='resolve':
        print ""+url
        main.RESOLVE(url,name,iconimage)


elif mode=='videoresolve':
        print ""+url
        status.VIDEORESOLVE(url,name,iconimage)

elif mode=='ytvideoresolve':
        print ""+url
        status.YTVIDEORESOLVE(url,name,iconimage)        

elif mode=='resolve2':
        print ""+url
        main.RESOLVE2(name,url,thumb)

elif mode=='resolvedl':
        print ""+url
        main.RESOLVEDL(url,name,thumb,favtype)
        
elif mode=='resolvetvdl':
        print ""+url
        main.RESOLVETVDL(name,url,thumb,favtype)



elif mode=='searchm':
        print ""+url
        SEARCHM(url)




elif mode=='searchtv':
        print ""+url
        tvshow.SEARCHTV(url)

elif mode=='downloadFile':
        print ""+url
        main.downloadFile(url)

        
elif mode=='helpcatagories':
        print ""+url
        HELPCATEGORIES(url)

elif mode=='helpstat':
        HELPSTAT(name,url,description)
                


elif mode=='searcht':
        print ""+url
        SEARCHT(url)        

elif mode=='resolverSettings':
        print ""+url
        urlresolver.display_settings()

elif mode=='loginSettings':
        print ""+url
        addon.show_settings('tmovies_account')        

elif mode == "dev message":
    ADDON.setSetting('dev_message', value='run')
    dev_message()

elif mode=='helpwizard':
        HELPWIZARD(name,url,description,filetype)

#=================ForDL===========================
elif mode=='viewQueue':
        print ""+url
        main.viewQueue()

elif mode=='download':
        print ""+url
        main.download()

elif mode=='removeFromQueue':
        print ""+url
        main.removeFromQueue(name,url,thumb,ext,console)

elif mode=='killsleep':
        print ""+url
        main.KILLSLEEP()        

    

#==================END DL=====================================

# ===============Movie DC=====================================

elif mode=='moviedclinkpage':
        print ""+url
        moviedc.MOVIEDCLINKPAGE(url,name,thumb,mainimg)

elif mode=='moviedcindex':
        print ""+url
        moviedc.MOVIEDCINDEX(url)
        
elif mode=='moviedcindexsec':
        print ""+url
        moviedc.MOVIEDCINDEXSEC(url)
        
elif mode=='moviedccats':
        print ""
        moviedc.MOVIEDCCATS()        

elif mode=='searchmoviedc':
        print ""+url
        moviedc.SEARCHMOVIEDC(url)

elif mode=='moviedcsearch':
        print ""+url
        moviedc.MOVIEDCSEARCH(url)

# ===============Series Gate Movies=====================================

elif mode=='sgmovielinkpage':
        print ""+url
        sgmovie.SGMOVIELINKPAGE(url,name,thumb,mainimg)

elif mode=='sgmovieindex':
        print ""+url
        sgmovie.SGMOVIEINDEX(url)
        
elif mode=='sgmovieindexsec':
        print ""+url
        sgmovie.SGMOVIEINDEXSEC(url)
        
elif mode=='sgmoviecats':
        print ""
        sgmovie.SGMOVIECATS()        

elif mode=='searchsgmovie':
        print ""+url
        sgmovie.SEARCHSGMOVIE(url)

elif mode=='sgmoviesearch':
        print ""+url
        sgmovie.SGMOVIESEARCH(url)

#==================SGATE======================================

elif mode=='sgcats':
        print ""
        sgate.SGCATS()

elif mode=='sgindex':
        print ""+url
        sgate.SGINDEX(url)

elif mode=='sgepisodes':
        print ""+url
        sgate.SGEPISODES(url,name,thumb)

elif mode=='sgepisodelist':
        print ""+url
        sgate.SGEPISODELIST(url,name,thumb)

elif mode=='sgtvlinkpage':
        print ""+url
        sgate.SGTVLINKPAGE(url,name,thumb,mainimg)

elif mode=='sgsearchindex':
        print ""+url
        sgate.SGSEARCHINDEX(url)

elif mode=='searchsgtv':
        print ""+url
        sgate.SEARCHSGTV(url)

#====================POP UP STUFF=============================
elif mode=='pop':POP()
elif mode=='resetpopup':RESETPOPUP()
        
        
        
#==================Start Status/Help==========================

        
elif mode=='addonlist': print""+url; items=status.ADDONLIST(url)
elif mode=='searchaddon': print""+url; status.SEARCHADDON(url)
elif mode=='addonindex': print""+url; status.ADDONINDEX(name,url,filetype)        
elif mode == "statuscategories": print""+url; items=status.STATUSCATEGORIES(url)
elif mode == "addonstatus": print""+url; items=status.ADDONSTATUS(url)
elif mode=='getrepolink': print""+url; items=status.GETREPOLINK(url)
elif mode=='getshorts': print""+url; items=status.GETSHORTS(url)
elif mode=='getrepo': status.GETREPO(name,url,description,filetype)
elif mode=='getvideolink': print""+url; items=status.GETVIDEOLINK(url)
elif mode=='getvideo': status.GETVIDEO(name,url,iconimage,description,filetype)
elif mode=='addoninstall': status.ADDONINSTALL(name,url,description,filetype,repourl)
elif mode=='addshortcuts': status.ADDSHORTCUTS(name,url,description,filetype)
elif mode=='addsource': status.ADDSOURCE(name,url,description,filetype)
elif mode=='playstream': status.PLAYSTREAM(name,url,iconimage,description)

#=======================Cia Anime===========================
elif mode=='chiacats':
        print ""
        chia.CHIACATS()

elif mode=='chiaalph':
        print ""
        chia.CHIAALPH()

elif mode=='chiadlvidpage':
        print ""+url
        chia.CHIADLVIDPAGE(url,name)

elif mode=='chialinkpage':
        print ""+url
        chia.CHIALINKPAGE(url,name,thumb)

elif mode=='chialatest':
        print ""+url
        chia.CHIALATEST(url)
        
elif mode=='chiaalphmain':
        print ""+url
        chia.CHIAALPHMAIN(url)

elif mode=='chiagenremain':
        print ""+url
        chia.CHIAGENREMAIN(url)
        

elif mode=='chiagenres':
        print ""+url
        chia.CHIAGENRES(url)
        
elif mode=='chiaepisodes':
        print ""+url
        chia.CHIAEPISODES(url,name,year,thumb)

elif mode=='chiaresolve':
        print ""+url
        chia.CHIARESOLVE(url,name,iconimage)

elif mode=='searchanime':
        print ""+url
        chia.SEARCHANIME(url)

elif mode=='chiasearch':
        print ""+url
        chia.CHIASEARCH(url)

elif mode=='chiaresolvedl':
        print ""+url
        chia.CHIARESOLVEDL(url,name,thumb,favetype)

#================SHUTDOWN=================

elif mode=='shutdownxbmc':
        print ""+url
        SHUTDOWNXBMC()
   

#==========ChannelCut UFC================

elif mode=='chanufcindex':
        print ""+url
        chanufc.CHANUFCINDEX(url)

elif mode=='chanufccats':
        print ""+url
        chanufc.CHANUFCCATS()

elif mode=='ufclinkpage':
        print ""+url
        chanufc.UFCLINKPAGE(url,name)

elif mode=='dlsportvidpage':
        print ""+url
        chanufc.DLSPORTVIDPAGE(url,name)

#==========Eporn=========================

elif mode=='epornikCategories':
        print ""+url
        epornik.CATEGORIES()

elif mode=='epornikIndex':
        print ""+url
        epornik.INDEX(url)

elif mode=='epornikSearch':
        print ""+url
        epornik.SEARCH()

elif mode=='pornresolve':
        print ""+url
        epornik.PORNRESOLVE(name,url,thumb)

#==========LIVE Streams================

elif mode=='chanufcindex':
        print ""+url
        live.CHANUFCINDEX(url)

elif mode=='livecats':
        print ""+url
        live.LIVECATS(url)

elif mode=='commonstreams':
        print ""+url
        live.COMMONSTREAMS(url)

elif mode=='usersub':
        print ""+url
        live.USERSUB(url)        

elif mode=='livecatslist':
        print ""+url
        live.LIVECATSLIST(url)        

elif mode=='ufclinkpage':
        print ""+url
        live.UFCLINKPAGE(url,name)

elif mode=='liveresolve':
        print ""+url
        live.LIVERESOLVE(name,url,thumb)

elif mode=='ilivemain':
        print ""+url
        live.ILIVEMAIN()
    
elif mode=='ilivelists':
        print ""+url
        live.ILIVELISTS(url)
    
elif mode=='iliveplaylink':
    print ""+url
    live.ILIVEPLAYLINK(name,url,thumb)

elif mode=='searchilive':
        print ""+url
        live.SEARCHILIVE(url)

elif mode=='addtofavs':
        print ""+url
        live.ADDTOFAVS(name,url,thumb)

elif mode=='removefromfavs':
        print ""+url
        live.REMOVEFROMFAVS(name,url,thumb)

elif mode=='playfavs':
        print ""+url
        live.PLAYFAVS(name,url,thumb)        

elif mode=='viewfavs':
        print ""+url
        live.VIEWFAVS()

elif mode=='addsttofavs':
        print ""+url
        live.ADDSTTOFAVS(name,url,thumb,gomode)

elif mode=='removestfromfavs':
        print ""+url
        live.REMOVESTFROMFAVS(name,url,thumb,gomode)

elif mode=='playstfavs':
        print ""+url
        live.PLAYSTFAVS(name,url,thumb)        

elif mode=='viewstfavs':
        print ""+url
        live.VIEWSTFAVS()        

elif mode=='resolver':
        print ""+url
        live.RESOLVER(url,name)

elif mode=='allfavs':
        ALLFAVS()

elif mode=='userstreams':
        print ""+url
        live.USERSTREAMS(url)

elif mode=='usercatslist':
        print ""+url
        live.USERCATSLIST(url)        


#=============END LIVE STREAMS

#===============SUPERTOONS=================

elif mode=='supertoonscats':
        print ""+url
        supertoons.SUPERTOONSCATS()

elif mode=='supertoonsindex':
        print ""+url
        supertoons.SUPERTOONSINDEX(url)

elif mode=='supertoonsdeep':
        print ""+url
        supertoons.SUPERTOONSDEEP(url)

elif mode=='supertoonsdirect':
        print ""+url
        supertoons.SUPERTOONSDIRECT(url)        

elif mode=='supertoonsresolve':
        print ""+url
        supertoons.SUPERTOONSRESOLVE(name,url,thumb)

#==============PornHub ===============================

elif mode=='phcategories':
        print ""+url
        phub.PHCATEGORIES()
        
elif mode=='phindex':
        print ""+url
        phub.PHINDEX(url)
        

elif mode=='phvideolinks':
        print ""+url
        phub.PHVIDEOLINKS(url,name)

elif mode=='phsearch':
        print ""+url
        phub.PHSEARCH(url)

#===============181FM===============================
elif mode=='oneeightymain':
        oneeighty.ONEEIGHTYMAIN()

elif mode=='oneeightylist':
        oneeighty.ONEEIGHTYLIST(name,url)

elif mode=='oneeightylink':
        oneeighty.ONEEIGHTYLINK(name,url)        
        
#==================LOG FILE UPLOAD==================

elif mode=='uploadlogfile':UPLOADLOGFILE()
elif mode=='advert':ADVERT()

#===================Update Files=====================

elif mode=='updatefiles':
        autoupdate.UPDATEFILES()

#===============IwatchOnline=========================
elif mode=='catiwo':
        print ""+url
        iwo.CATIWO(url)

elif mode=='iwogenres':
        print ""+url
        iwo.IWOGENRES(url)

elif mode=='iwoalph':
        print ""+url
        iwo.IWOALPH()

elif mode=='iwohd':
        print ""+url
        iwo.IWOHD()

elif mode=='iwohdalph':
        print ""+url
        iwo.IWOHDALPH()        
        
elif mode=='iwomovies':
        print ""+url
        iwo.IWOMOVIES(url)

elif mode=='iwovidpage':
        print ""+url
        iwo.IWOVIDPAGE(url,name)
        
elif mode=='iwoforvid':
        print ""+url
        iwo.IWOFORVID(url,name)

#==================Zee Movies=======================
elif mode=='catzeemovies':
        print ""+url
        iwo.CATZEEMOVIES(url)

elif mode=='zeemovies':
        print ""+url
        iwo.ZEEMOVIES(url)

elif mode=='zeegenres':
        print ""+url
        iwo.ZEEGENRES(url)

elif mode=='zeevidpage':
        print ""+url
        iwo.ZEEVIDPAGE(url,name)

elif mode=='zeerepass':
        print ""+url
        iwo.ZEEREPASS(url,name)        
        
        

#==================ESPN==============================
elif mode=='espnmain':
        espn.ESPNMAIN()

elif mode=='espnlist':
        espn.ESPNLIST(url)

elif mode=='espnlink':
        espn.ESPNLINK(name,url,thumb)

#===================FLIXSERIES======================

elif mode=='popcats':
        print ""+url
        flix.POPCATS()
       
elif mode=='flixindex':
        print ""+url
        flix.FLIXINDEX(url,favtype)
        

elif mode=='flixvideolinks':
        print ""+url
        flix.FLIXVIDEOLINKS(name,url,thumb,favtype)

elif mode=='flixaddlink':
        print ""+url
        flix.FLIXADDLINK(name,url,thumb)                                   


elif mode=='flixindexdeep':
        print ""+url
        flix.FLIXINDEX_DEEP(url,favtype)

elif mode=='popcornsearch':
        print ""+url
        flix.POPCORNSEARCH(url)

elif mode=='frightpxsearch':
        print ""+url
        flix.FRIGHTPXSEARCH(url)

#==================StreamLicensing=====================

elif mode=='streamlic':
        print ""+url
        streamlic.STREAMLIC(url)

elif mode=='streamlicindex':
        streamlic.STREAMLICINDEX()

elif mode=='streamlicgenre':
        streamlic.STREAMLICGENRE()

elif mode=='streamlicsearch':
        print ""+url
        streamlic.STREAMLICSEARCH(url)


#==========9Streams======================
elif mode=='nineindex':
        print ""+url
        ninestreams.NINEINDEX()

elif mode=='ninetools':
        print ""+url
        ninestreams.NINETOOLS()        
        
elif mode=='ninemain':
        print ""+url
        ninestreams.NINEMAIN()

elif mode=='nineresolver':
        print ""+url
        ninestreams.NINERESOLVER(url,name)
        
elif mode=='sublinks':
        print ""+url
        ninestreams.SUBLINKS(url,name)         
        
elif mode=='ninemainlocal':
        print ""+url
        ninestreams.NINEMAINLOCAL()
        
elif mode=='ninelists':
        print ""+url
        ninestreams.NINELISTS(url)

elif mode=='ninelocallists':
        print ""+url
        ninestreams.NINELOCALLISTS(url)

elif mode=='addfile':
        print ""+url
        ninestreams.ADDFILE()

elif mode=='addplaylist':
        print ""+url
        ninestreams.ADDPLAYLIST()         


elif mode=='nineplaylink':
        print ""+url
        ninestreams.NINEPLAYLINK(name,url,thumb,page)

elif mode=='previousmenu':
        print ""+url
        ninestreams.PREVIOUSMENU()

elif mode=='database':
        print ""+url
        ninestreams.DATABASE(url)

elif mode=='standarddbtypes':
        print ""+url
        ninestreams.STANDARDDBTYPES()
        
elif mode=='boxdbtypes':
        print ""+url
        ninestreams.BOXDBTYPES()

elif mode=='authordbtypes':
        print ""+url
        ninestreams.AUTHORDBTYPES()

elif mode=='userdatabase':
        print ""+url
        ninestreams.USERDATABASE()

elif mode=='playlistdata':
        ninestreams.PLAYLISTDATA(url)        
        
#=======================AFDAH MODES===========================

elif mode=='afdahlinkpage':
        print ""+url
        afdah.AFDAHLINKPAGE(url,name,thumb,mainimg)

elif mode=='afdahindex':
        print ""+url
        afdah.AFDAHINDEX(url)
        
elif mode=='afdahindexsec':
        print ""+url
        afdah.AFDAHINDEXSEC(url)
        
elif mode=='afdahcats':
        print ""
        afdah.AFDAHCATS()        

elif mode=='searchmovieafdah':
        print ""+url
        afdah.SEARCHMOVIEAFDAH(url)

elif mode=='afdahgenre':
        print ""+url
        afdah.AFDAHGENRE(url)        

#===========TEST FUNCTIONS================
elif mode=='testfunction':
        print ""+url
        TESTFUNCTION()

elif mode=='myclass':
        print ""+url
        MyClass()

elif mode=='myip':
        print ""+url
        MYIP()          
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))


#CHECK_POPUP()

