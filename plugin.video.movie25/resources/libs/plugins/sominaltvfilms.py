import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urlresolver
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
from resources.libs import main
from decimal import Decimal
import time

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from resources.universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
datapath = addon.get_profile()


    
wh = watchhistory.WatchHistory('plugin.video.movie25')


def MAIN():
        main.GA("Plugin","SominalTv")
        main.addDir('Search','xoxe',624,art+'/search.png')
        main.addDir('Hindi','http://www.sominaltvfilms.com/category/hindi-movies',620,art+'/hindi.png')
        main.addDir('Telugu','http://www.sominaltvfilms.com/category/telugu',620,art+'/telugu.png')
        main.addDir('Tamil','http://www.sominaltvfilms.com/category/tamil',620,art+'/tamil.png')
        main.addDir('Malayalam','http://www.sominaltvfilms.com/category/malayalam',620,art+'/malayalam.png')
        main.addDir('Punjabi','http://www.sominaltvfilms.com/category/punjabi',620,art+'/punjabi.png')
        main.addDir('BluRay','http://www.sominaltvfilms.com/category/bluray',620,art+'/bluray.png')
        main.addDir('All English Subtitled Movies','http://www.sominaltvfilms.com/category/english-subtitled',620,art+'/subtitled.png')
        main.addDir('All Hindi Dubbed Movies','http://www.sominaltvfilms.com/category/hindi-dubbed',620,art+'/dubbed.png')


def AtoZ(url):
    main.addDir('0-9','http://www.sominaltvfilms.com/search/label/%23'+url+'?&max-results=15',620,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://www.sominaltvfilms.com/search/label/'+i+url+'?&max-results=15',620,art+'/'+i.lower()+'.png')
    main.GA("Watchseries","A-Z")
    main.VIEWSB()
    
def SEARCH():
        keyb = xbmc.Keyboard('', 'Search Movies')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                surl='http://www.sominaltvfilms.com/?s='+encode
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile("""<div class='inner'><figure><a href="([^<]+)"><img src="(.+?)" alt="(.+?)"/>.+?<div class='description'><div class='date'>.+?<p>(.+?)</p>""").findall(link)
        for thumb,url,name,desc in match:
            desc=desc.replace('</div><div class="separator" style="clear: both; text-align: left;">','').replace('<span class="Apple-style-span" style="background-color: white; color: #333333; font-family: Verdana, Arial, sans-serif; font-size: 13px; line-height: 18px;">','').replace('</div><div class="separator" style="clear: both; text-align: justify;">','').replace('</div><div class="separator" style="clear: both; text-align: center;">','').replace('</span>','').replace('<span>','').replace('</div><div class="separator" style="clear: both; text-align: justify;"><span class="Apple-style-span" style="background-color: white; color: #333333; font-family: Verdana, Arial, sans-serif; font-size: 13px; line-height: 18px;">','')
            desc=desc.replace('<br>','').replace('</br>','').replace('</div>','').replace('<div>','')
            main.addDirM(name,url,621,thumb,desc,thumb,'','','')

               

def LIST(mname,murl):
        main.GA("SominalTv","List")
        if mname=='Hindi':
                main.addDir('Hindi English Subtitled','http://www.sominaltvfilms.com/category/hindi-movies-english-subtitles',620,art+'/subtitled.png')
                main.addDir('Hindi BluRay','http://www.sominaltvfilms.com/category/hindi-blurays',620,art+'/bluray.png')
        elif mname=='Telugu':
                main.addDir('Telugu English Subtitled','http://www.sominaltvfilms.com/category/telugu-movies-english-subtitles',620,art+'/subtitled.png')
                main.addDir('Telugu BluRay','http://www.sominaltvfilms.com/category/telugu-blurays',620,art+'/bluray.png')
        elif mname=='Tamil':
                main.addDir('Tamil English Subtitled','http://www.sominaltvfilms.com/category/tamil-movies-english-subtitles',620,art+'/subtitled.png')
                main.addDir('Tamil BluRay','http://www.sominaltvfilms.com/category/tamil-blurays',620,art+'/bluray.png')
        elif mname=='Malayalam':
                main.addDir('Malayalam English Subtitled','http://www.sominaltvfilms.com/category/malayalam-movies-english-subtitles',620,art+'/subtitled.png')
        elif mname=='Punjabi':
                main.addDir('Punjabi English Subtitled','http://www.sominaltvfilms.com/category/punjabi-movies-english-subtitles',620,art+'/subtitled.png')
        elif mname=='All Hindi Dubbed Movies':
                main.addDir('Dubbed BluRay','http://www.sominaltvfilms.com/category/hindi-dubbed-blurays',620,art+'/bluray.png')
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile("""<div class='inner'><figure><a href="([^<]+)"><img src="(.+?)" alt="(.+?)"/>.+?<div class='description'><div class='date'>.+?<p>(.+?)</p>""").findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,desc in match:
                desc=desc.replace('  ','')
                name=main.unescapes(name)
                main.addDirM(name,url,621,thumb,desc,thumb,'','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                    return False   
        dialogWait.close()
        del dialogWait
        paginate = re.compile("""<a class="nextpostslink" href="(.+?)">.+?</a>""").findall(link)
        if len(paginate)>0:
            main.addDir('Next',paginate[0],620,art+'/next2.png')
        main.VIEWS()

def LINK(mname,murl,thumb,fan,desc):
        parts=[]
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match= re.compile('<a href="http://adf.ly/377117/(.+?)".+?target="_blank.+?>(.+?)</a>').findall(link)
        if len(match)==0:
                 match= re.compile('<a class="btn btn-custom btn-medium btn-red btn-red " target=".+?" href="http://adf.ly/377117/(.+?)"><span style=".+?"><strong>(.+?)</strong>').findall(link)
        b=1
        for url,name in match:
            name=name.replace('</b>','').replace('<b>','').replace('<span style="font-size: x-large;">','').replace('<span id="goog_1857978069"></span><span id="goog_1857978070"></span>','').replace('<span style="font-family: Verdana, sans-serif; font-size: x-large;">','').replace('<span style="font-family: Verdana, sans-serif; font-size: large;">','').replace('<span>','').replace('</span>','')
            http= re.compile('http://').findall(url)
            if len(http)==0:
                url='http://'+url
            if re.findall('part',name[0:4],re.I):
                    name=mname+' '+name
            main.addPlayc(name,url,622,thumb,desc,fan,'','','')
            parts.append(('Part '+str(b),url))
            b=b+1
        if parts and len(parts)>1:
            main.addPlayc(mname+' [COLOR blue]Play All[/COLOR]',str(parts),622,thumb,desc,fan,'','','')


def getvideo2(murl):
        link=main.OPENURL(murl)
        link2=dekode(link)
        stream_url2= re.compile('file: "(.+?)"').findall(link2)[0]
        return stream_url2
        
                
def LINK2(mname,murl,thumb,desc):
        SRT=os.path.join(datapath,'Sub.srt')
        if  os.path.exists(SRT):
                os.remove(SRT)
        ok=True
        infoLabels =main.GETMETAT(mname,'','',thumb)
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        main.GA("SominalTv","Watched")
        if murl:
                if "'," in murl:
                    print murl
                    mname=main.removeColoredText(mname)
                    pl=xbmc.PlayList(1);pl.clear()
                    playlist = sorted(list(set(eval(murl))), key=lambda playlist: playlist[0])
                    for xname,link in playlist:
                        pl.add(getvideo2(link),xbmcgui.ListItem(mname+' '+xname,thumbnailImage=img))
                    xbmc.Player().play(pl)
                    xbmc.Player().setSubtitles(SRT)
                    while xbmc.Player().isPlaying():
                        xbmc.sleep(2500)
                    if selfAddon.getSetting("whistory") == "true":
                        wh.add_item(mname+' '+'[COLOR green]SominalFilms[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
   
                else:
                        stream_url2=getvideo2(murl)
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,3000)")
                        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                        # play with bookmark
                        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url2, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                        player.setSubtitles(SRT)#inserts Srt file from profile folder
                        #WatchHistory
                        if selfAddon.getSetting("whistory") == "true":
                                wh.add_item(mname+' '+'[COLOR green]SominalFilms[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                        player.KeepAlive()
                                 

                        return ok
        else:
                        xbmc.executebuiltin("XBMC.Notification(Sorry!,Protected Link,5000)")




def _enk_dec_num(kode, enc):
    if re.search('fromCharCode', enc):
        x = ''
        for nbr in kode.split():
            x += chr(int(nbr) - 3)
        return x
    else:
        return None
    
def _enk_dec_swap(kode, enc):
    if re.search('charAt', enc):
        x = ''
        i = 0
        while i < (len(kode) - 1):
            x += (kode[i + 1] + kode[i])
            i += 2
        return (x + (kode[len(kode) - 1] if i < len(kode) else ''))
    else:
        return None
    
def _enk_dec_reverse(kode, enc):
    if re.search('reverse', enc):
        return kode[::-1]
    else:
        return None
    
ENK_DEC_FUNC = [_enk_dec_num, _enk_dec_swap, _enk_dec_reverse]


def dekode(html):
    kodeParts = re.compile('var kode\="kode\=\\\\"(.+?)\\\\";(.+?);"').findall(html)
    if len(kodeParts) == 0:
        return None
    kode = None
    while len(kodeParts) == 1:
        kode = kodeParts[0][0].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        enc = kodeParts[0][1].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        for dec_func in ENK_DEC_FUNC:
            x = dec_func(kode, enc)
            if x is not None:
                kode = x
        kodeParts = re.compile('kode\="(.+?)";(.*)').findall(kode.replace('\\"', 'BY_PASS_D').replace('\\\'', 'BY_PASS_S'))
    dekoded = kode.replace('\\"', '"').replace('\\\'', '\'').replace('\\\\', '\\')
    return dekoded            
