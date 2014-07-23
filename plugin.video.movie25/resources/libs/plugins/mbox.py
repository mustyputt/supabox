# -*- coding: utf-8 -*-
import urllib,re,os,sys,json
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,time
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
smalllogo = art+'/smallicon.png'
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
profile = os.path.join(main.datapath,'MBox')
dataurl = 'http://mobapps.cc/data/data_en.zip'
prettyName = 'MBox'

def MAIN():
    lock_file_path = os.path.join(os.path.join(main.datapath,'Temp'), 'mbox.lock')
    lock_file = main.getFile(lock_file_path)
    if not lock_file:
        try: 
            lib=os.path.join(datapath, 'MBox.zip')
            if main.downloadFile(dataurl,lib,False):
                xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,profile))
        except: pass
        main.setFile(lock_file_path,'lock')
    main.addDir('Movies','movies',278,art+'/mbox.png')
    main.addDir('TV','tv',278,art+'/mbox.png')
    main.addDir('Music','music',278,art+'/mbox.png')
    main.GA("Plugin","MBox")

def DownloadAndList(type):
    try: 
        lib=os.path.join(datapath, 'MBox.zip')
        path=os.path.join(profile,type.lower()+'_lite.json')
        if not os.path.exists(lib) or (os.path.exists(path) and os.stat(path).st_mtime + 3600 < time.time()):
            if main.downloadFile(dataurl,lib,False):
                xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,profile))
                time.sleep(.2)
                LIST(type)
        elif os.path.exists(path): LIST(type)
    except: pass
    
def negtopos(num):
    if num == -1: return 99999
    return num
    
def LIST(type):
    path=os.path.join(profile,type+'_lite.json')
    f = open(path)
    field=json.loads(f.read())
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Content list is cached.')
    totalLinks = len(field)
    loadedLinks = 0
    remaining_display = 'Content Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    field = sorted(field,key=lambda x:x['poster'],reverse=True)
    try:
        updates = ''
        if 'movies'in type: path = os.path.join(profile,'news_movies.json')
        else: path = os.path.join(profile,'news_tv.json')
        updates = open(path).read()
        field = sorted(field,key=lambda word: negtopos(updates.find('"id":'+word['id']+',')))
    except: pass
    for data in field:
        #genre=str(data["genres"]).replace("u'",'').replace("'",'').replace("[",'').replace("]",'')
        if data['active'] == '1':
            thumb=str(data["poster"]).replace("\/'",'/')
            if 'movies'in type:
                main.addDown4(str(data["title"].encode('utf-8'))+' ('+str(data["year"])+')','http://mobapps.cc/api/serials/get_movie_data?id='+str(data["id"]),279,thumb,'','','','','')
            elif 'music' in type:
                main.addDirMs(str(data["title"].encode('utf-8')),'http://mobapps.cc/api/serials/get_artist_data/?id='+str(data["id"])+'&type=1',302,thumb,'','','','','')
            else:
                main.addDirT(str(data["title"].encode('utf-8')),data["id"]+'xoxe'+data["seasons"],280,thumb,'','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Content Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled():
            return False
    main.GA("Mbox","List")

def MUSICLIST(mname,murl):
    link=main.OPENURL(murl)
    fan=re.findall('"banner":"(.+?)",',link,re.DOTALL)[0]
    match=re.findall('{"id":".+?","link":"(.+?)","name":"(.+?)","year":"(.+?)","pic":"(.+?)"}',link,re.DOTALL)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Song list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Songs Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,name,year,thumb in match:
        main.addPlayMs(mname+' [COLOR red]'+name+' ('+year+')[/COLOR]',url,279,thumb.replace('\/','/'),'',fan.replace('\/','/'),'','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Songs Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled():
            return False
    main.GA("Mbox","Music")

def SEASONS(mname,murl):
    id = murl.split('xoxe')[0]
    season = murl.split('xoxe')[1]
    for s in reversed(range(int(season))):
        main.addDir(mname.strip()+' Season '+str(s+1),id,281,'')

def EPISODES(mname,murl):
    sea=re.findall('\sSeason\s(\d+)',mname,re.DOTALL)[0]
    getepi='http://mobapps.cc/api/serials/es/?id='+murl+'&season='+sea
    link=main.OPENURL(getepi)
    match=re.findall('"(\d+)":"([^"]+?)"',link,re.DOTALL)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Episodes list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Episodes Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for epinum,thumb in match:
        main.addDown4(mname+' Episode '+epinum,'http://mobapps.cc/api/serials/e/?h='+murl+'&u='+sea+'&y='+epinum,279,thumb.replace('\/','/'),'','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Episodes Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled():
            return False
 
def superSearch(encode,type):
    try:
        returnList=[]
        encode = encode.replace('%20',' ')
        try: 
            lib=os.path.join(datapath, 'MBox.zip')
            path=os.path.join(profile,type.lower()+'_lite.json')
            if not os.path.exists(lib) or (os.path.exists(path) and os.stat(path).st_mtime + 86400 < time.time()):
                if main.downloadFile(dataurl,lib,False):
                    xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,profile))
                    time.sleep(.2)
        except: pass
        f = open(path)
        field=json.loads(f.read())
        for data in field:
            if data['active'] == '1':
                thumb=str(data["poster"]).replace("\/'",'/')
                if type == 'Movies':
                    name = str(data["title"].encode('utf-8'))+' ('+str(data["year"])+')'
                    if re.search('(?i)'+encode,name):
                        returnList.append((name,prettyName,'http://mobapps.cc/api/serials/get_movie_data?id='+str(data["id"]),thumb,279,False))
                else:
                    name = str(data["title"].encode('utf-8'))
                    if re.search('(?i)'+encode,name):
                        returnList.append((name,prettyName,data["id"]+'xoxe'+data["seasons"],thumb,280,True))
        return returnList
    except: return []

def resolveMBLink(url):
    try:
        r = re.findall('h=(\d+?)&u=(\d+?)&y=(\d+)',url,re.I)
        if r: r = int(r[0][0]) + int(r[0][1]) + int(r[0][2])
        else: r = 537 + int(re.findall('id=(\d+)',url,re.I)[0])
        link=main.OPENURL(url,verbose=False)
        q = re.findall('"lang":"en","apple":(\d+?),"google":(\d+?),"microsoft":"([^"]+?)"',link,re.I)
        vklink = "https://vk.com/video_ext.php?oid="+str(r + int(q[0][0]))+"&id="+str(r + int(q[0][1]))+"&hash="+q[0][2]
    except:
        vklink=url
    vklink=vklink.replace("\/",'/')
    stream_url = main.resolve_url(vklink)
    return stream_url

def PLAY(mname,murl,thumb):
    main.GA("MBox","Watched") 
    stream_url = resolveMBLink(murl)
    r = re.findall('(.+?)\sSeason\s(\d+)\sEpisode\s(\d+)',mname,re.I)
    if r:
        infoLabels =main.GETMETAEpiT(mname,'','')
        video_type='episode'
        season=infoLabels['season']
        episode=infoLabels['episode']
    else:
        infoLabels =main.GETMETAT(mname,'','',thumb)
        video_type='movie'
        season=''
        episode=''
    img=infoLabels['cover_url']
    fanart =infoLabels['backdrop_url']
    imdb_id=infoLabels['imdb_id']
    infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
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
            wh.add_item(mname+' '+'[COLOR green]MBOX[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        player.KeepAlive()
        return True
    except Exception, e:
        if stream_url != False: main.ErrorReport(e)
        return False
