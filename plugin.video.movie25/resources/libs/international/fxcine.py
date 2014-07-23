
import urllib,urllib2,re,cookielib,urlresolver,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from resources.universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = main.art
wh = watchhistory.WatchHistory(addon_id)


def LISTFX():
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,10000)")
        urllist=main.OPENURL('http://www.fxcine.com/la/peliculas/page/1/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/2/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/3/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/4/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/5/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/6/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/7/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/8/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/9/')+main.OPENURL('http://www.fxcine.com/la/peliculas/page/10/')
        if urllist:
                urllist=urllist.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('class="load-local" href="(.+?)" rel=".+?div class="peli_img_img.+?img src="(.+?)" alt=".+?".+?<p class="sinopsis">(.+?)</p>.+?<div class="divcen">(.+?)<div class="sep-w">.+?alt="(.+?) on IMDb"',re.DOTALL).findall(urllist)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Movie list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                for url,thumb,desc,lang,name in match:
                        name=name.decode('latin-1')
                        name=name.encode('utf-8')
                        desc=desc.decode('latin-1')
                        desc=desc.encode('utf-8')
                        if 'eng1 d_inlineb' in lang:
                            name= name+' [COLOR red]ENG[/COLOR]'
                        if 'sub1 d_inlineb' in lang:
                            name= name+' [COLOR green]SUB[/COLOR]'
                        if 'lat1 d_inlineb' in lang:
                            name= name+' [COLOR yellow]LAT[/COLOR]'
                        if 'cas1 d_inlineb' in lang:
                            name= name+' [COLOR blue]CAS[/COLOR]'
                        main.addDirM(name,url,309,thumb,desc,'','','','')
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                            return False   
        dialogWait.close()
        del dialogWait
        main.GA("INT","FXCine")

def LANGFX(mname,murl,thumb):
    dialog = xbmcgui.Dialog()
    langList=[]
    idList=[]
    link=main.OPENURL(murl).replace('>Descargas</a></li>','')
    match=re.compile('<li><a href="#(.+?)">(.+?)</a></li>',re.DOTALL).findall(link)
    for id,lang in match:
        idList.append(id)
        langList.append(lang)
    ret = dialog.select('[COLOR=FF67cc33][B]Select Language[/COLOR][/B]',langList)
    if ret == -1:
        return
    else:
        vidlink=re.compile('<div id="'+idList[ret]+'" class=".+?<div class=".+?src="(.+?)" fr',re.DOTALL).findall(link)[0]
        LINKLIST(mname,vidlink)

def LINKLIST(mname,url):
    link=main.OPENURL(url)
    link=main.unescapes(link)
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    match=re.compile("""><img alt="([^<]+)" src="[^<]+" onClick="cargar.?'#player','(.+?)'""",re.DOTALL).findall(link)
    for host,url in match:
        host=host.replace(' Java','').replace('ShockShare','SockShare').replace('.to','')
        print host
        if main.supportedHost(host):
            mname=main.removeColoredText(mname)
            main.addDown2(mname+' [COLOR blue]'+host.upper()+'[/COLOR]','http://www.fxcine.com/player/'+url,310,art+'/hosts/'+host.lower()+".png",art+'/hosts/'+host.lower()+".png")

def getlink(murl):
    link=main.OPENURL(murl)
    try:
        match=re.compile('src="(.+?)"',re.I).findall(link)[0]
        if 'fxcine' in match:
                link2=main.OPENURL(match)
                match=re.compile('link=(.+?)&captions',re.DOTALL).findall(link2)[0]  
        return match
    except:
        return 'nolink'

def LINKFX(name,murl):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        main.GA("FXCine","Watched")
        stream_url = False
        ok=True
        infoLabels =main.GETMETAT(name,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }  
        url=getlink(murl)
        stream_url = main.resolve_url(url)
        try:
                    listitem = xbmcgui.ListItem(thumbnailImage='')
                    listitem.setInfo('video', {'Title': name, 'Year': ''} )         
                
                    infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                    # play with bookmark
                    player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=infoLabels['title'],season=season, episode=episode, year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                    #WatchHistory
                    if selfAddon.getSetting("whistory") == "true":
                        wh.add_item(name+' '+'[COLOR green]FXCine[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img='', fanart='', is_folder=False)
                    player.KeepAlive()
                    return ok
        except Exception, e:
                    if stream_url != False:
                        main.ErrorReport(e)
                    return ok
