import urllib,re,os,sys
import xbmc,xbmcgui,xbmcaddon,xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art

def LISTSP3(murl):
    subpages = 5
    if murl == 'HD':
        page = 1
        max = 100
    else:
        try:
            pages = murl.split(',', 1 );
            page = int(pages[0])
            max = int(pages[1])
        except:
            page = 1
#         http://www.filestube.to/query.html?q=1080p+bluray+-esubs+-msubs+-subs&hosting=85&select=mkv&sizefrom=6000&sizeto=20000&sort=dd&page=1
    url='http://www.filestube.to/query.html?q=1080p+bluray+-esubs&hosting=85&select=mkv&sizefrom=6000&sizeto=20000&sort=dd'
    urls = []
    for n in range(subpages):
        urls.append(url+"&page="+str(page+n))
        if page+n == max: break
    page = page + subpages - 1
    link=main.batchOPENURL(urls)
#         print link
    next = len(re.compile('rel="nofollow next">Next</a>').findall(link)) == subpages
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#38;','&')
    match=re.compile('(?sim)<a href="([^"]+?)"[^>]*?class="resultsLink"[^>]*?>(.+?)</a>').findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for url, name in match:
        url = url.decode('utf-8').encode('ascii', 'ignore')
        url = 'http://www.filestube.to' + url
        name = name.replace('<b>','').replace('</b>','')
        name=main.unescapes(name)
        if not re.search('(?i)(\\bsubs\\b|\\msubs\\b|fetish)',name) and re.search('(?i)(20\d\d|19\d\d)',name):
            main.addPlayM(name,url,406,'','','','','','')
            loadedLinks = loadedLinks + 1
        else: totalLinks -= 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False
    if next:
        main.addDir('Page ' + str(page/subpages) + ' [COLOR blue]Next Page >>>[/COLOR]',str(page+1)+','+str(max),405,art+'/next2.png')
    dialogWait.close()
    del dialogWait
    main.GA("HD-TV","FilesTube")
    main.VIEWS()
        
def LINKSP3(mname,murl):
    main.GA("FilesTube","Watched")
    msg = xbmcgui.DialogProgress()
    msg.create('Please Wait!','')
    msg.update(0,'Collecting hosts')
    link=main.OPENURL(murl,mobile=True,timeout = 10)
    sources=[]
    titles=[]
    ok=True
    match=re.compile('(?sim)<pre id="copy_paste_links"[^<]+?</pre>').findall(link)
    if match:
        match = re.compile('(https?://[^<]+)').findall(match[0])
    hostsmax = len(match)
    h = 0
    from urlparse import urlparse
    for url in match:
        url = url.strip()
        h += 1
        percent = (h * 100)/hostsmax
        msg.update(percent,'Collecting hosts - ' + str(percent) + '%')
        if msg.iscanceled(): break
        vlink=re.compile('rar|part\d+?(\.html)?$|/folder/').findall(url)
        if len(vlink)==0:
            host = urlparse(url).hostname.replace('www.','').partition('.')[0]
            hostname = host
            host = host.upper()
            quality = mname
            match3=re.compile('(?i)(720p?|1080p?)').findall(quality)
            if match3 and not 'p' in match3[0]: match3[0] += 'p'
            match4=re.compile('mp4').findall(url)
            if len(match3)>0:
                host =host+' [COLOR red]'+match3[0]+'[/COLOR]'
            elif len(match4)>0:
                host =host+' [COLOR green]SD MP4[/COLOR]'
            else:
                host =host+' [COLOR blue]SD[/COLOR]'
            if main.supportedHost(hostname):
                titles.append(host)
                sources.append(url)
    msg.close()
    if (len(sources)==0):
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Could not find a playable link,3000)")
        return
    else:
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose your stream', titles)
        if index != -1: 
            source = sources[index]
        else: source = None
    try:
        if not source:
            main.CloseAllDialogs()
            return
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")
        stream_url = main.resolve_url(source)
        if(stream_url == False):
            return
        
        if re.findall('(.+?)\ss(\d+)e(\d+)\s',mname,re.I):
            mname=mname.split('&')[0]
            infoLabels =main.GETMETAEpiT(mname,'','')
            video_type='episode'
            season=infoLabels['season']
            episode=infoLabels['episode']
        else:
            infoLabels =main.GETMETAT(mname,'','','')
            video_type='movie'
            season=''
            episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        
        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre'], 'originaltitle': infoLabels['metaName']}
        if not video_type is 'episode': infoL['originalTitle']=main.removeColoredText(infoLabels['metaName'])
        # play with bookmark
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from resources.universal import watchhistory
            wh = watchhistory.WatchHistory('plugin.video.movie25')
            wh.add_item(mname+' '+'[COLOR green]DL4Free[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
            main.ErrorReport(e)
        return ok