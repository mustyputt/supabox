#-*- coding: utf-8 -*-
import urllib,re,string,urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
prettyName = 'Aflam1'
MAINURL='http://www.aflam1.com'

def MAINAFLAM():
    main.addDir('Search (بحث)','aflam',342,art+'/search.png')
    main.addDir('Programs (برامج)','http://www.aflam1.com/tvshow.htm',336,art+'/aflam1.png')
    main.addDir('Series (مسلسلات)','http://www.aflam1.com/arabic-series.htm',339,art+'/aflam1.png')
    main.addDir('Movies (أفلام)','http://www.aflam1.com/arabic-movies.htm',340,art+'/aflam1.png')
    main.GA("Plugin","Aflam1")

def SEARCHAFLAM():
        keyb = xbmc.Keyboard('', 'Search Movies & Shows')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            encode=urllib.quote(search)
            surl='http://www.aflam1.com/search.php?query='+encode+'&andor=AND&mids%5B%5D=2&mids%5B%5D=3&submit=Search&action=results&id_REQUEST=c47d515172b7e063c5852f3b72f5c8fc'
            link=main.OPENURL(surl)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','')
            match=re.compile("""><img src='([^<]+)' alt='.+?<a href='(.+?)'>(.+?)</a></strong>""",re.DOTALL).findall(link)
            for thumb,url,name in match:
                name=name+'  '
                url=MAINURL+'/'+url
                if '/movies/watch'in url:
                    main.addPlayM(name,url,338,thumb,'','','','','')
                else:
                    main.addDir(name,url,337,thumb)

def SERIESAFLAM(murl):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','')
    match=re.compile("""<a title="([^<]+)" href="(.+?)">.+?class="hint">(.+?)</div>""",re.DOTALL).findall(link)
    for name,url,count in match:
        name=name+'  '
        main.addDir('[COLOR red]'+count+'[/COLOR]  '+name,url,336,art+'/aflam1.png')

def MOVIESAFLAM(murl):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','')
    match=re.compile("""<a href="([^<]+)"><b>(.+?)</b></a>([^<]+)""",re.DOTALL).findall(link)
    for url,name,count in match:
        count=count.replace('  ','')
        name=name+'  '
        main.addDir('[COLOR red]'+count+'[/COLOR]'+name,url,341,art+'/aflam1.png')

def LISTMov(murl):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','')
    match=re.compile("""<td width=".+?" valign=".+?" style=".+?<a href="([^<]+)"><img src="(.+?)".+?title="(.+?)" alt=".+?".+?</ul>(.+?)</div>""",re.DOTALL).findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for url,thumb,name,desc in match:
        name=main.unescapes(name)
        main.addPlayM(name,url,338,thumb,desc,'','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False   
    dialogWait.close()
    del dialogWait
    paginate = re.compile('''<a class="xo-pagarrow" href="([^<]+)"><u></u>''').findall(link)
    if len(paginate)>0:
        main.addDir('Next',MAINURL+paginate[0],341,art+'/next2.png')
                
    main.GA("Aflam1","List")

def LISTProg(murl):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','')
    match=re.compile("""<a href="([^<]+)"><img style=".+?src="(.+?)" width=".+?<a href='.+?'>(.+?)</a>""",re.DOTALL).findall(link)
    for url,thumb,name in match:
        main.addDir(name,url,337,thumb)

    paginate = re.compile('''<a class="xo-pagarrow" href="([^<]+)"><u></u>''').findall(link)
    if len(paginate)>0:
        main.addDir('Next',MAINURL+paginate[0],336,art+'/next2.png')
                
    main.GA("Aflam1","List")


def LISTEPI(mname,murl,thumb):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&raquo;','')
    match=re.compile("""<h3><a class="play" href="([^<]+)" onClick="return popups.+?">(.+?)</a></h3>""",re.DOTALL).findall(link)
    for url,name in match:
        main.addPlayc(name,url,338,thumb,'','','','','')


def get_mailru(url):
    from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
    import cookielib
    link=main.OPENURL(url)
    match=re.compile('videoSrc = "(.+?)",',re.DOTALL).findall(link)
    cj = cookielib.CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
    req = Request(url)
    f = opener.open(req)
    html = f.read()
    for cookie in cj:
        cookie=str(cookie)

    rcookie=cookie.replace('<Cookie ','').replace(' for .video.mail.ru/>','')

    vlink=match[0]+'|Cookie='+rcookie
    return vlink
    

def LINKSAFLAM(mname,murl,thumb):
    main.GA("Aflam1","Watched")
    if '/movies/watch'in murl:
        link=main.OPENURL(murl)
        match=re.compile('<a class="btn default large text-right" href=(.+?)"',re.DOTALL).findall(link)
        if match:
            murl=match[0]
            murl=murl.replace(' ','')
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")
    link=main.OPENURL(murl)
    ok=True
    infoLabels =main.GETMETAT(mname,'','',thumb)
    video_type='movie'
    season=''
    episode=''
    img=infoLabels['cover_url']
    fanart =infoLabels['backdrop_url']
    imdb_id=infoLabels['imdb_id']
    infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        
    match=re.compile('<div id="Layer2".+?<iframe src="(.+?)"',re.DOTALL).findall(link)
    if match:
        stream_url = main.resolve_url(match[0])
    else:
        match2=re.compile('value="movieSrc=(.+?)&autoplay=0"',re.DOTALL).findall(link)
        url='http://api.video.mail.ru/videos/embed'+match2[0]+'.html'
        stream_url=get_mailru(url)
    try:
        if stream_url == False: return                                                            
        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre'], 'originaltitle': infoLabels['metaName']}
        # play with bookmark
        stream_url=stream_url.replace(' ','%20')
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from resources.universal import watchhistory
            wh = watchhistory.WatchHistory(addon_id)
            wh.add_item(mname+' '+'[COLOR green]Aflam1[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        player.KeepAlive()
        return True
    except Exception, e:
        if stream_url != False: main.ErrorReport(e)
        return False
