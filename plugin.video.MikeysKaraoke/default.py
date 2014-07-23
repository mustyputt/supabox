import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,xbmcvfs,string
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
import settings
import json
import datetime
import time


PLUGIN='plugin.video.MikeysKaraoke'


begurl='http://www.sunflykaraoke.com/search/genre/'
          
endurl='?sort_Karaoke Tracks=popularity-desc'
youtubeaddon = xbmcaddon.Addon(id='plugin.video.youtube')
downloads= youtubeaddon.getSetting('download_path')

local = xbmcaddon.Addon(id=PLUGIN)

ADDON = settings.addon()
home = ADDON.getAddonInfo('path')
sfdownloads= ADDON.getSetting('sfdownloads')
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
font=ADDON.getSetting('font') 


if os.path.exists(datapath)==False:
    os.mkdir(datapath) 
if ADDON.getSetting('sfenable') == True:
    os.makedirs(sfdownloads)
if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))
    
K_db='http://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.MikeysKaraoke/Karaoke.db'
updatetxt='http://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.MikeysKaraoke/update.txt'


addon = Addon('plugin.video.MikeysKaraoke',sys.argv)
art= "%s/KaraokeArt/"%local.getAddonInfo("path")
from sqlite3 import dbapi2 as database
db_dir = os.path.join(xbmc.translatePath("special://database"), 'Karaoke.db')


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def Update():
    import downloader
    dp = xbmcgui.DialogProgress()
    dp.create("Mikeys Karaoke","",'Building Database Please Wait', ' ')
    downloader.download(K_db, db_dir,dp)
    
if os.path.exists(db_dir)==False:
    link=OPEN_URL(updatetxt)
    match=re.compile('id=<(.+?)>').findall (link)
    dp = xbmcgui.Dialog()
    dp.ok("Mikeys Karaoke","",'There is a New Database Update', 'Please Wait')
    Update()
    ADDON.setSetting('id',match[0])     
       
        
db = database.connect(db_dir)
db.execute('CREATE TABLE IF NOT EXISTS tracklist (sunfly_name, number, artist, track, iconimage, url)')
db.execute('CREATE TABLE IF NOT EXISTS favourites (track_name, artist, track, iconimage, url)')
db.commit()
db.close()

def GRABBER(type,mode,item):
    db = database.connect( db_dir );cur = db.cursor()
    if type == 1:#EXACT MATCH ALL
        item = '%'+item+'%'
        cached = cur.fetchall()
        try: cur.execute('SELECT * FROM tracklist WHERE %s = "%s"' %(mode,item))
        except:pass
    elif type == 2: #EXACT MATCH ONE
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s = "%s"' %(mode,item))
        except:pass
        cached = cur.fetchone()
    elif type == 3:#NEAREST MATCH ONE
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchone()
    elif type == 4:# NEAREST MATCH ALL
        item = '%'+item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchall()
    elif type == 5:# NEAREST MATCH ALL BY FIRST LETTER
        item = item+'%'
        try: cur.execute('SELECT * FROM tracklist WHERE %s LIKE "%s"' %(mode,item))
        except:pass
        cached = cur.fetchall()
    if cached:
        db.close()
        return cached

def STRIP(name):
  return re.sub(r'\[.*?\]|\(.*?\)|\W -', ' ', name).strip()

  
def download_DB():
    import downloader
    dp = xbmcgui.DialogProgress()
    dp.create("Mikeys Karaoke","",'Building Database Please Wait', ' ')
    downloader.download(K_db, db_dir,dp)
  
  
def CATEGORIES():
        link=OPEN_URL(updatetxt)
        match=re.compile('id=<(.+?)>').findall (link)
        if int(match[0]) > int(ADDON.getSetting('id')):
            dp = xbmcgui.Dialog()
            dp.ok("Mikeys Karaoke","",'There is a New Database Update', 'Please Wait')
            Update()
            ADDON.setSetting('id',match[0])        
        addDir('[COLOR '+font+']'+'Youtube[/COLOR] Karaoke','url',19,art+'Main/youtube.png','none',1)
        addDir('[COLOR '+font+']'+'Sunfly[/COLOR] Karaoke','url',20,art+'Main/SUNFLY.png','none',1) 
        addDir('[COLOR '+font+']'+'Favourites[/COLOR]','url',2,art+'Main/SUNFLY.png','none',1)
        setView('movies', 'MAIN')
            
def mikeyyoutube(url):
        addDir('[COLOR '+font+']'+'Search[/COLOR]-[COLOR '+font+']'+'Y[/COLOR]outube Karaoke','url',3,art+'Main/Search.png','none',1)
        if ADDON.getSetting('downloads') == 'true':
            addDir('[COLOR '+font+']'+'D[/COLOR]ownloads','url',15,art+'Main/favorites.png','',1)
        addDir('[COLOR '+font+']'+'Most[/COLOR] Popular','http://www.sunflykaraoke.com/browse/tracks/?sort_BrowseTracksAll=popularity-desc&pg_BrowseTracksAll=&show_BrowseTracksAll=500',7,art+'AtoZ/P.png','none',1)
        addDir('[COLOR '+font+']'+'L[/COLOR]atest','http://www.sunflykaraoke.com/browse/tracks/?sort_BrowseTracksAll=Latest&pg_BrowseTracksAll=&show_BrowseTracksAll=500',7,art+'AtoZ/L.png','none',1)
        addDir('[COLOR '+font+']'+'Browse[/COLOR] Artist','http://www.lyricsmania.com/lyrics/%s.html',1,art+'Main/Artist.png','none',4)
        addDir('[COLOR '+font+']'+'Browse[/COLOR] Tracks','http://www.sunflykaraoke.com/browse/tracks/%s?pgBrowseTracksAll=&show_BrowseTracksAll=50',1,art+'Main/Title.png','none',7)
        addDir('[COLOR '+font+']'+'G[/COLOR]enre','http://www.sunflykaraoke.com/',8,art+'Main/Genre.png','none',1)
        setView('movies', 'MAIN')
        
def mikeysunfly(url):
        addDir('[COLOR '+font+']'+'Search[/COLOR]-[COLOR '+font+']'+'X[/COLOR]unity Karaoke','url',16,art+'Main/Search.png','none',1)
        if ADDON.getSetting('sfenable') == 'true':
            addDir('[COLOR '+font+']'+'D[/COLOR]ownloads','url',31,art+'Main/favorites.png','',1)
        addDir('[COLOR '+font+']'+'Search[/COLOR] By Number','url',25,art+'Main/Search.png','none',1)
        addDir('[COLOR '+font+']'+'Browse[/COLOR] Artist','http://www.sunflykaraoke.com/',1,art+'Main/Artist.png','none',23)
        addDir('[COLOR '+font+']'+'Browse[/COLOR] Tracks','http://www.sunflykaraoke.com/',1,art+'Main/Title.png','none',24)
        addDir('[COLOR '+font+']'+'G[/COLOR]enre','http://www.sunflykaraoke.com/',32,art+'Main/Genre.png','none',1)
        addDir('[COLOR '+font+']'+'D[/COLOR]ownload Database','http://www.sunflykaraoke.com/',103,'','none',1)
        setView('movies', 'MAIN')

def AtoZ(url,number,fanart):
    if 'lyrics' in url:
        addDir('0-9',url%'num',number,"%s/KaraokeArt/AtoZ/0-9.png"%local.getAddonInfo("path"),fanart,1)
        setView('movies', 'A-Z')
    if '%s' in url:
        for i in string.ascii_uppercase:
            addDir(i,url%i,number,"%s/KaraokeArt/AtoZ/%s.png"%(local.getAddonInfo("path"),i),fanart,1)
            setView('movies', 'A-Z')
    else:
        for i in string.ascii_uppercase:
            addDir(i,url,number,"%s/KaraokeArt/AtoZ/%s.png"%(local.getAddonInfo("path"),i),fanart,1)

def FAVOURITES(switch,name,iconimage,url):
    IMAGE = os.path.join(ADDON.getAddonInfo('path'), 'icon.jpg')
    print IMAGE
    db = database.connect( db_dir );cur = db.cursor()
    if switch == 'add':
        sql = "INSERT OR REPLACE INTO favourites (track_name,iconimage,url) VALUES(?,?,?)"
        cur.execute(sql, (STRIP(name).replace('  ',' ').upper(),iconimage.replace(' ','%20'),url.replace(' ','%20')))
        db.commit(); db.close()
        xbmc.executebuiltin('XBMC.Notification('+name.upper().replace('  ',' ')+',Added to Favorites,2000,'+IMAGE+')')
    if switch == 'delete':
        name=name.upper().replace('[/COLOR]','').replace('[COLOR '+font+']'+'','').replace('[COLOR GREY3]','').replace('  ',' ')
        cur.execute("DELETE FROM favourites WHERE track_name='%s'"%name.upper())
        db.commit(); db.close()
        xbmc.executebuiltin('XBMC.Notification('+name.upper().replace('  ',' ')+',Deleted from Favorites,2000,'+IMAGE+')')
        xbmc.executebuiltin("XBMC.Container.Refresh")
    if switch == 'display':
        cur.execute("SELECT * FROM favourites")
        cached = cur.fetchall()
        if cached:
            for name,artist,track,iconimage,url in cached:
                addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR][COLOR grey3]%s[/COLOR]'%(name.split('~')[0],name.split('~')[1]),url,url.replace('.avi','.jpg'))
        
def GENRE(url):
        addDir('40s/50s',begurl+'40-s-and-50-s-pop3429190/'+endurl,10,art+'Genre/4050POP.png',art+'Main/Fanart_G.jpg',1)
        addDir('60s',begurl+'60-s-pop/karaoke-tracks,albums,artists/3429191/'+endurl,10,art+'Genre/60POP.png',art+'Main/Fanart_G.jpg',1) 
        addDir('70s',begurl+'70-s-pop/karaoke-tracks,albums,artists/3429192/'+endurl,10,art+'Genre/70POP.png',art+'Main/Fanart_G.jpg',1)
        addDir('80s',begurl+'80-s-pop/karaoke-tracks,albums,artists/3429193/'+endurl,10,art+'Genre/80POP.png',art+'Main/Fanart_G.jpg',1)
        addDir('90s',begurl+'90-s-pop/karaoke-tracks,albums,artists/3429194/'+endurl,10,art+'Genre/90POP.png',art+'Main/Fanart_G.jpg',1)
        addDir('2000s',begurl+'00-s-pop/karaoke-tracks,albums,artists/3429189/'+endurl,10,art+'Genre/2000sPOP.png',art+'Main/Fanart_G.jpg',1) 
        addDir('2010s',begurl+'10-s-pop/karaoke-tracks,albums,artists/3429195/'+endurl,10,art+'Genre/2010sPOP.png',art+'Main/Fanart_G.jpg',1)
        addDir('Boybands',begurl+'boybands/karaoke-tracks,albums,artists/3429196/'+endurl,10,art+'Genre/Boybands.png',art+'Main/Fanart_G.jpg',1)
        addDir('R&B',begurl+'r-n-b/karaoke-tracks,albums,artists/3429220/'+endurl,10,art+'Genre/RnB.png',art+'Main/Fanart_G.jpg',1)
        addDir('Brit Pop',begurl+'brit-pop/karaoke-tracks,albums,artists/3429229/'+endurl,10,art+'Genre/Britpop.png',art+'Main/Fanart_G.jpg',1)
        addDir('Broadway',begurl+'broadway/karaoke-tracks,albums,artists/3429197/'+endurl,10,art+'Genre/Broadway.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Elvis',begurl+'elvis/karaoke-tracks,albums,artists/3429204/'+endurl,10,art+'Genre/Elvis.png',art+'Main/Fanart_G.jpg',1)
        addDir('Childrens',begurl+'children-s/karaoke-tracks,albums,artists/3429198/'+endurl,10,art+'Genre/Childrens.png',art+'Main/Fanart_G.jpg',1)        
        addDir('Christmas',begurl+'christmas/karaoke-tracks,albums,artists/3429199/'+endurl,10,art+'Genre/Christmas.png',art+'Main/Fanart_G.jpg',1)
        addDir('Comedy',begurl+'comedy/karaoke-tracks,albums,artists/3429200/'+endurl,10,art+'Genre/Comedy.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Country',begurl+'country/karaoke-tracks,albums,artists/3429201/'+endurl,10,art+'Genre/Country.png',art+'Main/Fanart_G.jpg',1)
        addDir('Dance',begurl+'dance/karaoke-tracks,albums,artists/3429202/'+endurl,10,art+'Genre/Dance.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Duets',begurl+'duets/karaoke-tracks,albums,artists/3429203/'+endurl,10,art+'Genre/Duets.png',art+'Main/Fanart_G.jpg',1)
        addDir('Male Superstars',begurl+'male-superstars/karaoke-tracks,albums,artists/3429213/'+endurl,10,art+'Genre/Male.png',art+'Main/Fanart_G.jpg',1)
        addDir('Female Superstars',begurl+'female-superstars/karaoke-tracks,albums,artists/3429205/'+endurl,10,art+'Genre/Female.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Folk',begurl+'folk/karaoke-tracks,albums,artists/3429230/'+endurl,10,art+'Genre/Folk.png',art+'Main/Fanart_G.jpg',1)
        addDir('Football Anthems',begurl+'football-anthems/karaoke-tracks,albums,artists/3429228/'+endurl,10,art+'Genre/Football.png',art+'Main/Fanart_G.jpg',1)        
        addDir('Foreign',begurl+'foreign/karaoke-tracks,albums,artists/3429206/'+endurl,10,art+'Genre/Foreign.png',art+'Main/Fanart_G.jpg',1)
        addDir('Funk',begurl+'funk/karaoke-tracks,albums,artists/3429231/'+endurl,10,art+'Genre/Funk.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Girlbands',begurl+'girlbands/karaoke-tracks,albums,artists/3429207/'+endurl,10,art+'Genre/Girlbands.png',art+'Main/Fanart_G.jpg',1)
        addDir('Glee',begurl+'glee/karaoke-tracks,albums,artists/14196105/'+endurl,10,art+'Genre/GAYCUNTS.png',art+'Main/Fanart_G.jpg',1)
        addDir('Grunge',begurl+'grunge-post-grunge/karaoke-tracks,albums,artists/18813424/'+endurl,10,art+'Genre/Grunge.png',art+'Main/Fanart_G.jpg',1)
        addDir('Halloween',begurl+'halloween/karaoke-tracks,albums,artists/3429208/'+endurl,10,art+'Genre/Halloween.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Heavy Metal',begurl+'heavy-metal-alt-metal/karaoke-tracks,albums,artists/3429209/'+endurl,10,art+'Genre/Metal.png',art+'Main/Fanart_G.jpg',1)
        addDir('Jazz/Blues',begurl+'jazz-blues/karaoke-tracks,albums,artists/3429212/'+endurl,10,art+'Genre/JazzBlues.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Indie',begurl+'indie/karaoke-tracks,albums,artists/3429210/'+endurl,10,art+'Genre/Indie.png',art+'Main/Fanart_G.jpg',1)
        addDir('Irish',begurl+'irish/karaoke-tracks,albums,artists/3429211/'+endurl,10,art+'Genre/Irish.png',art+'Main/Fanart_G.jpg',1)
        addDir('Medleys',begurl+'medley-s/karaoke-tracks,albums,artists/3429214/'+endurl,10,art+'Genre/Medleys.png',art+'Main/Fanart_G.jpg',1)
        addDir('Movies & TV',begurl+'movie-s-and-tv/karaoke-tracks,albums,artists/3429215/'+endurl,10,art+'Genre/Movies.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Multiplex',begurl+'multiplex/karaoke-tracks,albums,artists/3429216/'+endurl,10,art+'Genre/Multiplex.png',art+'Main/Fanart_G.jpg',1)
        addDir('Punk Rock',begurl+'punk-rock/karaoke-tracks,albums,artists/3429217/'+endurl,10,art+'Genre/PunkRock.png',art+'Main/Fanart_G.jpg',1)        
        addDir('Rap/Hip-Hop',begurl+'rap-hip-hop/karaoke-tracks,albums,artists/3429218/'+endurl,10,art+'Genre/HipHop.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Reggae',begurl+'reggae/karaoke-tracks,albums,artists/3429219/'+endurl,10,art+'Genre/Reggae.png',art+'Main/Fanart_G.jpg',1)
        addDir('Religious/Gospel',begurl+'religious-gospel/karaoke-tracks,albums,artists/3429227/'+endurl,10,art+'Genre/GODFREAKS.png',art+'Main/Fanart_G.jpg',1)
        addDir('Rock',begurl+'rock/karaoke-tracks,albums,artists/3429221/'+endurl,10,art+'Genre/Rock.png',art+'Main/Fanart_G.jpg',1)
        addDir('Rock & Roll/Disco',begurl+'rock-and-roll-disco/karaoke-tracks,albums,artists/3429222/'+endurl,10,art+'Genre/RnR.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Sea Shanties',begurl+'sea-shanties/karaoke-tracks,albums,artists/30174405/'+endurl,10,art+'Genre/Shanties.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Sing A Long',begurl+'sing-a-long/karaoke-tracks,albums,artists/3429223/'+endurl,10,art+'Genre/Sing.png',art+'Main/Fanart_G.jpg',1)
        addDir('Skate/Soft Rock',begurl+'skate-soft-rock/karaoke-tracks,albums,artists/3429224/'+endurl,10,art+'Genre/Skate.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Soul/Motown',begurl+'soul-motown/karaoke-tracks,albums,artists/3429225/'+endurl,10,art+'Genre/Soul.png',art+'Main/Fanart_G.jpg',1)
        addDir('Swing/Standards',begurl+'swing-standards/karaoke-tracks,albums,artists/3429226/'+endurl,10,art+'Genre/Swing.png',art+'Main/Fanart_G.jpg',1) 
        setView('movies', 'GENRE')
        
def GENRESF(url):
        addDir('40s/50s',begurl+'40-s-and-50-s-pop/karaoke-tracks,albums,artists/3429190/'+endurl,33,art+'Genre/4050POP.png',art+'Main/Fanart_G.jpg',1)
        addDir('60s',begurl+'60-s-pop/karaoke-tracks,albums,artists/3429191/'+endurl,33,art+'Genre/60POP.png',art+'Main/Fanart_G.jpg',1) 
        addDir('70s',begurl+'70-s-pop/karaoke-tracks,albums,artists/3429192/'+endurl,33,art+'Genre/70POP.png',art+'Main/Fanart_G.jpg',1)
        addDir('80s',begurl+'80-s-pop/karaoke-tracks,albums,artists/3429193/'+endurl,33,art+'Genre/80POP.png',art+'Main/Fanart_G.jpg',1)
        addDir('90s',begurl+'90-s-pop/karaoke-tracks,albums,artists/3429194/'+endurl,33,art+'Genre/90POP.png',art+'Main/Fanart_G.jpg',1)
        addDir('2000s',begurl+'00-s-pop/karaoke-tracks,albums,artists/3429189/'+endurl,33,art+'Genre/2000sPOP.png',art+'Main/Fanart_G.jpg',1) 
        addDir('2010s',begurl+'10-s-pop/karaoke-tracks,albums,artists/3429195/'+endurl,33,art+'Genre/2010sPOP.png',art+'Main/Fanart_G.jpg',1)
        addDir('Boybands',begurl+'boybands/karaoke-tracks,albums,artists/3429196/'+endurl,33,art+'Genre/Boybands.png',art+'Main/Fanart_G.jpg',1)
        addDir('R&B',begurl+'r-n-b/karaoke-tracks,albums,artists/3429220/'+endurl,33,art+'Genre/RnB.png',art+'Main/Fanart_G.jpg',1)
        addDir('Brit Pop',begurl+'brit-pop/karaoke-tracks,albums,artists/3429229/'+endurl,33,art+'Genre/Britpop.png',art+'Main/Fanart_G.jpg',1)
        addDir('Broadway',begurl+'broadway/karaoke-tracks,albums,artists/3429197/'+endurl,33,art+'Genre/Broadway.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Elvis',begurl+'elvis/karaoke-tracks,albums,artists/3429204/'+endurl,33,art+'Genre/Elvis.png',art+'Main/Fanart_G.jpg',1)
        addDir('Childrens',begurl+'children-s/karaoke-tracks,albums,artists/3429198/'+endurl,33,art+'Genre/Childrens.png',art+'Main/Fanart_G.jpg',1)        
        addDir('Christmas',begurl+'christmas/karaoke-tracks,albums,artists/3429199/'+endurl,33,art+'Genre/Christmas.png',art+'Main/Fanart_G.jpg',1)
        addDir('Comedy',begurl+'comedy/karaoke-tracks,albums,artists/3429200/'+endurl,33,art+'Genre/Comedy.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Country',begurl+'country/karaoke-tracks,albums,artists/3429201/'+endurl,33,art+'Genre/Country.png',art+'Main/Fanart_G.jpg',1)
        addDir('Dance',begurl+'dance/karaoke-tracks,albums,artists/3429202/'+endurl,33,art+'Genre/Dance.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Duets',begurl+'duets/karaoke-tracks,albums,artists/3429203/'+endurl,33,art+'Genre/Duets.png',art+'Main/Fanart_G.jpg',1)
        addDir('Male Superstars',begurl+'male-superstars/karaoke-tracks,albums,artists/3429213/'+endurl,33,art+'Genre/Male.png',art+'Main/Fanart_G.jpg',1)
        addDir('Female Superstars',begurl+'female-superstars/karaoke-tracks,albums,artists/3429205/'+endurl,33,art+'Genre/Female.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Folk',begurl+'folk/karaoke-tracks,albums,artists/3429230/'+endurl,33,art+'Genre/Folk.png',art+'Main/Fanart_G.jpg',1)
        addDir('Football Anthems',begurl+'football-anthems/karaoke-tracks,albums,artists/3429228/'+endurl,33,art+'Genre/Football.png',art+'Main/Fanart_G.jpg',1)        
        addDir('Foreign',begurl+'foreign/karaoke-tracks,albums,artists/3429206/'+endurl,33,art+'Genre/Foreign.png',art+'Main/Fanart_G.jpg',1)
        addDir('Funk',begurl+'funk/karaoke-tracks,albums,artists/3429231/'+endurl,33,art+'Genre/Funk.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Girlbands',begurl+'girlbands/karaoke-tracks,albums,artists/3429207/'+endurl,33,art+'Genre/Girlbands.png',art+'Main/Fanart_G.jpg',1)
        addDir('Glee',begurl+'glee/karaoke-tracks,albums,artists/14196105/'+endurl,33,art+'Genre/GAYCUNTS.png',art+'Main/Fanart_G.jpg',1)
        addDir('Grunge',begurl+'grunge-post-grunge/karaoke-tracks,albums,artists/18813424/'+endurl,33,art+'Genre/Grunge.png',art+'Main/Fanart_G.jpg',1)
        addDir('Halloween',begurl+'halloween/karaoke-tracks,albums,artists/3429208/'+endurl,33,art+'Genre/Halloween.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Heavy Metal',begurl+'heavy-metal-alt-metal/karaoke-tracks,albums,artists/3429209/'+endurl,33,art+'Genre/Metal.png',art+'Main/Fanart_G.jpg',1)
        addDir('Jazz/Blues',begurl+'jazz-blues/karaoke-tracks,albums,artists/3429212/'+endurl,33,art+'Genre/JazzBlues.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Indie',begurl+'indie/karaoke-tracks,albums,artists/3429210/'+endurl,33,art+'Genre/Indie.png',art+'Main/Fanart_G.jpg',1)
        addDir('Irish',begurl+'irish/karaoke-tracks,albums,artists/3429211/'+endurl,33,art+'Genre/Irish.png',art+'Main/Fanart_G.jpg',1)
        addDir('Medleys',begurl+'medley-s/karaoke-tracks,albums,artists/3429214/'+endurl,33,art+'Genre/Medleys.png',art+'Main/Fanart_G.jpg',1)
        addDir('Movies & TV',begurl+'movie-s-and-tv/karaoke-tracks,albums,artists/3429215/'+endurl,33,art+'Genre/Movies.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Multiplex',begurl+'multiplex/karaoke-tracks,albums,artists/3429216/'+endurl,33,art+'Genre/Multiplex.png',art+'Main/Fanart_G.jpg',1)
        addDir('Punk Rock',begurl+'punk-rock/karaoke-tracks,albums,artists/3429217/'+endurl,33,art+'Genre/PunkRock.png',art+'Main/Fanart_G.jpg',1)        
        addDir('Rap/Hip-Hop',begurl+'rap-hip-hop/karaoke-tracks,albums,artists/3429218/'+endurl,33,art+'Genre/HipHop.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Reggae',begurl+'reggae/karaoke-tracks,albums,artists/3429219/'+endurl,33,art+'Genre/Reggae.png',art+'Main/Fanart_G.jpg',1)
        addDir('Religious/Gospel',begurl+'religious-gospel/karaoke-tracks,albums,artists/3429227/'+endurl,33,art+'Genre/GODFREAKS.png',art+'Main/Fanart_G.jpg',1)
        addDir('Rock',begurl+'rock/karaoke-tracks,albums,artists/3429221/'+endurl,33,art+'Genre/Rock.png',art+'Main/Fanart_G.jpg',1)
        addDir('Rock & Roll/Disco',begurl+'rock-and-roll-disco/karaoke-tracks,albums,artists/3429222/'+endurl,33,art+'Genre/RnR.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Sea Shanties',begurl+'sea-shanties/karaoke-tracks,albums,artists/30174405/'+endurl,33,art+'Genre/Shanties.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Sing A Long',begurl+'sing-a-long/karaoke-tracks,albums,artists/3429223/'+endurl,33,art+'Genre/Sing.png',art+'Main/Fanart_G.jpg',1)
        addDir('Skate/Soft Rock',begurl+'skate-soft-rock/karaoke-tracks,albums,artists/3429224/'+endurl,33,art+'Genre/Skate.png',art+'Main/Fanart_G.jpg',1) 
        addDir('Soul/Motown',begurl+'soul-motown/karaoke-tracks,albums,artists/3429225/'+endurl,33,art+'Genre/Soul.png',art+'Main/Fanart_G.jpg',1)
        addDir('Swing/Standards',begurl+'swing-standards/karaoke-tracks,albums,artists/3429226/'+endurl,33,art+'Genre/Swing.png',art+'Main/Fanart_G.jpg',1) 
        setView('movies', 'GENRE')
            
def Next_Page(link):
    link = link.split('class="paging-bar-pages">')[1]
    link=link.split('<a href=')
    for l in link:
        match=re.compile('"(.+?)#.+?" class="arrow">&gt;</a>').findall(l)        
        if match:
            return match
    return None 


    
    
def SEARCH(url):
        keyboard = xbmc.Keyboard('', '[COLOR white]Search[/COLOR] [COLOR '+font+']'+'X[/COLOR][COLOR white]unity Karaoke[/COLOR] ')
        keyboard.doModal()
        if keyboard.isConfirmed() and len(keyboard.getText())>0:
           html=OPEN_URL('http://m.youtube.com/results?gl=GB&client=mv-google&hl=en-GB&q=%s+karaoke&submit=Search' % (keyboard.getText().replace(' ','+')))
        else: addDir('[COLOR '+font+']'+'[B]Nothing found[/B][/COLOR]',url,19,'','',1);return
        link=html.split('yt-lockup-title')
        for links in link:
            if not '__video_id__' or not '__title__' in links:
                match=re.compile('title="(.+?)".+?href=".+?=(.+?)"',re.DOTALL).findall(links)
                for items in match:
                    url= match[0][1]
                    name=match[0][0]
                    name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                    iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
                    if not 'YouTube Video Search' in name:
                        addLink(name,url,iconimage,'')        
        if '<span class="yt-uix-button-content">Next' in html:        
            match1=re.compile('href="(.+?)".+?">Next ').findall(html)
            nxtp=match1[0]
            nextpage='http://m.youtube.com'+str(nxtp)
            addDir('[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]',nextpage,11,art+'next.png','','')
        setView('movies', 'VIDEO')
                                                                                
def ARTIST_INDEX(url, iconimage):
        link=net().http_GET(url).content.encode('ascii','ignore')
        match = re.compile('<li><a href="(.+?)" title="(.+?)">.+?</a></li>').findall(link)
        for url, name in match:
            url = 'http://www.lyricsmania.com'+url   
            name = str(name).replace("lyrics","")
            addDir(name,url,5,iconimage,art+'Main/Fanart_A.jpg',1)
            setView('movies', 'DEFAULT')


def ARTIST_SONG_INDEX(url,name):
        link=net().http_GET(url).content
        match = re.compile('<a href="(.+?)">.+? in alphabetical order</a></b><br>').findall(link)
        url1 = 'http://www.lyricsmania.com'+match[0]
        link1=net().http_GET(url1).content
        match1 = re.compile('<a href=".+?_lyrics_(.+?).html" title="(.+?) lyrics">').findall(link1)
        fanart = art+'Main/Fanart_A.jpg'
        for url, name, in match1:
            name = str(name).replace("&Agrave;","A").replace('&eacute;','e').replace('&ecirc;','e').replace('&egrave;','e').replace("&agrave;","A")
            addDir(name.encode('ascii','ignore'),url,6,iconimage,fanart,1)
            setView('tvshow', 'DEFAULT')
            

    
def TRACK_INDEX(url, iconimage):
        link1=OPEN_URL(url.replace(' ','%20'))
        link=str(link1).replace('&___c=___c#listingTrack0_link','')
        match = re.compile('target="_self">(.+?)</a></td><td class="listing-col-artist"><a href=".+?" target="_self">(.+?)</a>').findall(link)
        nextpageurl=Next_Page(link)[0]       
        uniques = []        
        for name, url, in match:
            if name not in uniques and url not in uniques:
                uniques.append(name)
                uniques.append(url)
                name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")  
                url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
                name = name+ '   ('+ url+')'
                addDir(name,url,9,iconimage,art+'Main/Fanart_T.jpg',1)
                setView('movies', 'DEFAULT')
        try:
                url='http://www.sunflykaraoke.com'+str(nextpageurl)
                name= '[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]'
                addDir(name,url,7,art+'next.png','none',1)    
                setView('movies', 'DEFAULT') 
        except:
                pass
                
def GENRE_INDEX(name,url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        match = re.compile('target="_self">(.+?)</a></td><td class="listing-col-artist"><a href=".+?" target="_self">(.+?)</a>').findall(link)
        nextpageurl=Next_Page(link)[0]       
        for name, url, in match:
            name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","")  
            url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
            name = name+ '   ('+ url+')'
            addDir(name,url,9,iconimage,art+'Main/Fanart_G.jpg',1)
            setView('movies', 'DEFAULT')
        try:
                url='http://www.sunflykaraoke.com'+str(nextpageurl)
                name= '[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]'
                addDir(name,url,7,art+'next.png','none',1)    
                setView('movies', 'DEFAULT') 
        except:
                pass
            
            
def GENRE_INDEXSF(name,url, iconimage):
        link=OPEN_URL(url.replace(' ','%20'))
        nextpageurl=Next_Page(link)[0]       
        match = re.compile('target="_self">(.+?)</a></td><td class="listing-col-artist"><a href=".+?" target="_self">(.+?)</a>').findall(link)
        for name, url, in match:
            passto = re.sub('[\(\)\{\}<>]', '', name.replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("&quot;",""))
            name = re.sub('[\(\)\{\}<>]', '', name.replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("&quot;","").replace("'",""))
            url = str(url).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","") 
            addDir('[COLOR '+font+']'+'%s[/COLOR] - %s'%(passto,url),name,34,iconimage,art+'Main/Fanart_G.jpg',1)
            setView('movies', 'DEFAULT')
        try:
                url='http://www.sunflykaraoke.com'+str(nextpageurl)
                name= '[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]'
                addDir(name,url,33,art+'next.png','none',1)    
                setView('movies', 'DEFAULT') 
        except:
                pass
            
        
def SEARCH_GENRE(url,name):
    print url
    db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The)\s','',url))
    if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
        if artist in name.split('-')[1].strip():
            addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)
        
def YOUTUBE_SONG_INDEX(name, url, iconimage, fanart):
        url = str(url).replace(' ','+').replace('_','+')  
        name = str(name).replace(' ','+') 
        url = 'http://m.youtube.com/results?gl=GB&client=mv-google&hl=en-GB&q=%s+%s+karaoke&submit=Search' % (name, url) 
        html=OPEN_URL(url)
        link=html.split('yt-lockup-title')
        for links in link:
            if not '__video_id__' or not '__title__' in links:
                match=re.compile('title="(.+?)".+?href=".+?=(.+?)"',re.DOTALL).findall(links)
                for items in match:
                    url= match[0][1]
                    name=match[0][0]
                    name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                    iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
                    if not 'YouTube Video Search' in name:
                        addLink(name,url,iconimage,'')        
        if '<span class="yt-uix-button-content">Next' in html:        
            match1=re.compile('href="(.+?)".+?">Next ').findall(html)
            nxtp=match1[0]
            nextpage='http://m.youtube.com'+str(nxtp)
            addDir('[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]',nextpage,11,art+'next.png','','')
        setView('movies', 'VIDEO')
            
def TITLE_ORDERS_YOUTUBE(name, url,fanart):
        name = str(name).replace('   (','+') .replace(' ','+') .replace(')','')
        url = 'http://m.youtube.com/results?gl=GB&client=mv-google&hl=en-GB&q=%s+karaoke&submit=Search' % (name) 
        print url
        html=OPEN_URL(url)
        link=html.split('yt-lockup-title')
        for links in link:
            if not '__video_id__' or not '__title__' in links:
                match=re.compile('title="(.+?)".+?href=".+?=(.+?)"',re.DOTALL).findall(links)
                for items in match:
                    url= match[0][1]
                    name=match[0][0]
                    name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                    iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
                    if not 'YouTube Video Search' in name:
                        addLink(name,url,iconimage,'')        
        if '<span class="yt-uix-button-content">Next' in html:        
            match1=re.compile('href="(.+?)".+?">Next ').findall(html)
            nxtp=match1[0]
            nextpage='http://m.youtube.com'+str(nxtp)
            addDir('[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]',nextpage,11,art+'next.png','','')
        setView('movies', 'VIDEO')
        
        
def SF_Download(name,url,iconimage,split):
    import downloader
    name=name.replace(' [/color]','').split('~')[split]
    dp = xbmcgui.DialogProgress()
    dp.create("Mikeys Karaoke","",'Downloading', name)
    path = xbmc.translatePath(os.path.join(sfdownloads,''))
    name=name.upper()
    lib=os.path.join(path, name+'.avi')
    downloader.download(iconimage.replace('.jpg','.avi'),lib,dp)
    lib=os.path.join(path, name+'.jpg')
    downloader.download(iconimage,lib,dp)
    
    
def DOWNLOADS(downloads):
     import glob
     path = downloads
     for infile in glob.glob(os.path.join(path, '*.*')):
         addFile(infile)
    
    
def SFDOWNLOADS(sfdownloads):
     import glob
     path = sfdownloads
     for infile in glob.glob(os.path.join(path, '*.avi')):
         addFileSF(infile)
        
            
def nextpage(url):
        html=OPEN_URL(url)
        link=html.split('yt-lockup-title')
        for links in link:
            if not '__video_id__' or not '__title__' in links:
                match=re.compile('title="(.+?)".+?href=".+?=(.+?)"',re.DOTALL).findall(links)
                for items in match:
                    url= match[0][1]
                    name=match[0][0]
                    name = str(name).replace("&#39;","'") .replace("&amp;","and") .replace("&#252;","u") .replace("&quot;","").replace("[","").replace("]","").replace("-"," ")
                    iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % url
                    if not 'YouTube Video Search' in name:
                        addLink(name,url,iconimage,'')        
        if '<span class="yt-uix-button-content">Next' in html:        
            match1=re.compile('href="(.+?)".+?">Next ').findall(html)
            nxtp=match1[0]
            nextpage='http://m.youtube.com'+str(nxtp)
            addDir('[COLOR '+font+']'+'[B]Next Page >>[/B][/COLOR]',nextpage,11,art+'next.png','','')
        setView('movies', 'VIDEO')
            
def addFile(file):
        name = file.replace(downloads,'').replace('.mp4','')
        name = name.split('-[')[-2]
        thumb = icon(file)[0]
        iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % thumb
        url=file
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        contextMenu = []
        contextMenu.append(('Delete', 'XBMC.RunPlugin(%s?mode=102&url=%s&iconimage=%s)'% (sys.argv[0], file,iconimage)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url,listitem = liz, isFolder = False)
        setView('movies', 'VIDEO')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)    

def addFileSF(file):
        iconimage = file.replace('.avi','.jpg').replace('.mp4','.jpg')
        name = file.replace(sfdownloads,'').replace('.avi','').replace('.mp4','')
        url=file
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        contextMenu = []
        contextMenu.append(('Delete', 'XBMC.RunPlugin(%s?mode=102&url=%s&iconimage=%s)'% (sys.argv[0], file,iconimage)))
        liz.addContextMenuItems(contextMenu,replaceItems=True)
        xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url=url,listitem = liz, isFolder = False)
        setView('movies', 'VIDEO')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)   
        
                
def deleteFileSF(file,iconimage):
    tries    = 0
    maxTries = 10
    while os.path.exists(file) and tries < maxTries:
        try:
            os.remove(file)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1
    while os.path.exists(iconimage) and tries < maxTries:
        try:
            os.remove(iconimage)
            break
        except:
            xbmc.sleep(500)
            tries = tries + 1
            
            
    if os.path.exists(file):
        d = xbmcgui.Dialog()
        d.ok('Mikeys Karaoke', 'Failed to delete file')         
                           
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
        

def Sunflysearch(url):
    keyboard = xbmc.Keyboard('', '[COLOR grey3]Search by[/COLOR] [COLOR '+font+']'+'Artist[/COLOR] [COLOR grey3]or[/COLOR] [COLOR '+font+']'+'Track[/COLOR]')
    keyboard.doModal()
    if keyboard.isConfirmed():
        db=GRABBER(4,'artist',keyboard.getText())
        if not db: db=GRABBER(4,'artist',re.sub('\A(a|A|the|THE|The)\s','',keyboard.getText()))
        if not db: db=GRABBER(4,'track',keyboard.getText())
        if not db: db=GRABBER(4,'track',re.sub('\A(a|A|the|THE|The)\s','',keyboard.getText()))
        if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
        for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon)
    
                
             
def AZ_ARTIST_SEARCH(name):
    db=GRABBER(5,'artist',name)
    if not db: addLinkSF('[COLOR red]ARTIST NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR]%s'%(artist,track),burl,icon,split=1)
    
def SF_SEARCH(url):
    sunfly = 'SF'
    keyboard = xbmc.Keyboard(sunfly, 'Enter Sunfly Disc Number:-')
    keyboard.doModal()
    if keyboard.isConfirmed():
        db=GRABBER(4,'sunfly_name',keyboard.getText())
        if not db: addLinkSF('[COLOR red]DISC NOT AVAILABLE.[/COLOR]',url,'');return
        for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+font+']'+'%s:-%s ~ [/COLOR]%s'%(sf,number,track),burl,icon,split=1)
        
        
def AZ_TRACK_SEARCH(name):
    db=GRABBER(5,'track',re.sub('\A(a|A|the|THE|The)\s','',name))
    if not db: addLinkSF('[COLOR red]TRACK NOT AVAILABLE.[/COLOR]',url,'');return
    for sf,number,artist,track,icon,burl in db:
            addLinkSF('[COLOR '+font+']'+'%s ~ [/COLOR]%s'%(track,artist),burl,icon,split=0)    
        
def addDir(name,url,mode,iconimage,fanart,number):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&number="+str(number)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty( "Fanart_Image", fanart )
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        if (mode == 2000)or mode==103:         
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)
        if not mode==1 and mode==20 and mode==19:
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        
def addLink(name,url,iconimage, fanart,showcontext=True):
                #name=name.encode('ascii', 'ignore')
                #url=url.encode('ascii', 'ignore')
                cmd = 'plugin://plugin.video.youtube/?path=root/video&action=download&videoid=%s' % url
                youtube = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % url
                liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
                liz.setInfo( type="Video", infoLabels={ "Title": name } )
                liz.setProperty("IsPlayable","true")
                liz.setProperty("Fanart_Image", fanart )
                menu = []
                if showcontext:
                    try:
                        if name in FAV:
                            menu.append(('Remove YouTube Favorites','XBMC.RunPlugin(%s?name=%s&mode=14&iconimage=None&fanart=None&url=None)' %(sys.argv[0],name)))
                        else:
                            menu.append(('Add to YouTube Favorites','XBMC.RunPlugin((%s?fanart=%s&mode=13&iconimage=%s&url=%s&name=%s)' %(sys.argv[0],fanart,iconimage,url,name)))
                    except:
                        menu.append(('Add to YouTube Favorites','XBMC.RunPlugin(%s?fanart=%s&mode=13&iconimage=%s&url=%s&name=%s)' %(sys.argv[0],fanart,iconimage,url,name)))
                if ADDON.getSetting('downloads') == 'true':
                    menu.append(('Download', 'XBMC.RunPlugin(%s)' % cmd))   
                liz.addContextMenuItems(items=menu, replaceItems=True)
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=youtube,listitem=liz,isFolder=False)
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

                                
def addLinkSF(name,url,iconimage,showcontext=True,split=None):
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty("IsPlayable","true")
        liz.setProperty('mimetype', 'video/x-msvideo')
        menu = []
        if showcontext:
            menu.append(('[COLOR green]Add[/COLOR] to Xunity Karaoke Favorites','XBMC.RunPlugin(%s?mode=2&iconimage=%s&url=%s&name=%s&switch=%s)' %(sys.argv[0],iconimage,url,name,'add')))
            menu.append(('[COLOR red]Remove[/COLOR] Xunity Karaoke from Favourites','XBMC.RunPlugin(%s?name=%s&mode=2&iconimage=%s&url=%s&switch=%s)' %(sys.argv[0],name,iconimage,url,'delete')))
        if ADDON.getSetting('sfenable') == 'true':
            menu.append(('Download', 'XBMC.Container.Update(%s?&mode=30&url=%s&name=%s&iconimage=%s&split=%s)' %(sys.argv[0],url,name,iconimage,split)))  
        liz.addContextMenuItems(items=menu, replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        switch=urllib.unquote_plus(params["switch"])
except:
        switch='display'
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        number=int(params["number"])
except:
        pass
try:        
        split=int(params["split"])
except:
        pass
                
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
print "FanartImage: "+str(fanart)
try:print "number: "+str(number)
except:pass

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
    AtoZ(url,number,fanart)

elif mode==2:
    FAVOURITES(switch,name,iconimage,url)
        
elif mode==3:
        print ""+url
        SEARCH(url)
        
elif mode==4:
        ARTIST_INDEX(url, iconimage) 
        
elif mode==5:
        ARTIST_SONG_INDEX(url,name)
        
elif mode==6:
        YOUTUBE_SONG_INDEX(name, url, iconimage, fanart)
                                                             
elif mode==7:
        TRACK_INDEX(url, iconimage)
        
elif mode==8:
        GENRE(url)   
        
elif mode==9:
        TITLE_ORDERS_YOUTUBE(name, url, fanart)   
        
elif mode==10:
        GENRE_INDEX(name,url, iconimage)
                      
elif mode==11:
        nextpage(url)  
        
elif mode==12:
    pass
elif mode==13:
    addFavorite(name,url,iconimage,fanart)

elif mode==14:
    rmFavorite(name)
        
elif mode==15:
    DOWNLOADS(downloads)
    
elif mode==16:
    Sunflysearch(url)
    
elif mode==17:
    Sunflyurl(name)
    
elif mode==19:
    mikeyyoutube(url)

elif mode==20:
    mikeysunfly(url)

elif mode==23:
    AZ_ARTIST_SEARCH(name)
    
elif mode==24:
    AZ_TRACK_SEARCH(name)
    
elif mode==25:
    SF_SEARCH(name) 
    
elif mode==26:
    print ""
    LATEST_LIST(url)    
    
elif mode==27:
    addSF_Favorite(name,url,iconimage)

elif mode==28:
    rmSF_Favorite(name)
    
elif mode==29:
    getSF_Favorites()
    
elif mode==30:
    SF_Download(name,url,iconimage,split)
    
elif mode==31:
    SFDOWNLOADS(sfdownloads)
    
elif mode==32:
        GENRESF(url)   
elif mode==33:
        GENRE_INDEXSF(name,url, iconimage)
        
elif mode==34:
        SEARCH_GENRE(url,name)
       
elif mode==102:
    deleteFileSF(url,iconimage)
    xbmc.executebuiltin("Container.Refresh")
    
elif mode==103:
    download_DB()
    
    
elif mode==3000:
    test()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
