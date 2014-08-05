import xbmcplugin,xbmcgui,xbmcaddon,xbmc

import re,sys,os,urllib

try:
    try:
        from t0mm0.common.addon import Addon
    except:
        raise Exception ('Addon.common Not Found')
    try:
        from t0mm0.common.net import Net
    except:
         raise Exception ('Addon.common Not Found')
except Exception, e:
    xbmc.log('ERROR TV Time Capsule: '+str(e))
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR red]Failed To Find Needed Modules[/COLOR]','[COLOR red][B]'+str(e)+'[/COLOR][/B]',
              'Please Goto [COLOR green][B]XBMCTALK.COM[/COLOR][/B] For Support')
    xbmcplugin.endOfDirectory(int(sys.argv[1]),succeeded=True)

addonID = 'plugin.video.ctvtc'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
sys.path.append(xbmc.translatePath(os.path.join( local.getAddonInfo('path'), 'resources', 'lib')))


art = xbmc.translatePath(os.path.join( local.getAddonInfo('path'), 'resources', 'art' ))
BaseUrl = 'http://www.solie.org/alibrary/'
net = Net()

import requests

def GenerateMenu(menu_items):
    addDir(150,BaseUrl,'',"[COLOR red]Extra's[/COLOR]",os.path.join(art,'extra.jpg'),0,True)    
    for (url,name,mode) in menu_items:
        addDir(mode,BaseUrl+url+'.html','',name,os.path.join(art,url+'.jpg'),0,True)
    
    
menu_items = [
    ('funnyguys','Funny Guys!',100),
    ('whackydames','Whacky Dames!',100),
    ('westernshows','Westerns',100),
    ('kidshows','Kid Shows',100),
    ('variety','Variety Shows',100),
    ('gameshows','Game Shows',100),
    ('historical','Historical Drama',100),
    ('family','Family Comedies and Dramas',100),
    ('weird','SciFi, Fantasy and Horror',100),
    ('detectives','Mystery & Crime Drama',100),
    ('tvdrama','Television Drama',100),
    ('musical','Musical Programs',100,),
    ('ActionAdventure','Action & Adventure',100),
    ('documentary','News/Documentary (Reality) Programs',100),
    ('featurefilms','Feature Films',100),
    ('silentfilms','Silent Films',100),
    ('shorts','Cartoons, Serials, Short Format Films & Unsold Pilots',100),
    ('Christmas','The Christmas Collection',100)
    ]

extra_items = [
    ('6zo9rEoEc2M%26list=PLk1mDkkzvx7RSMc5oN3pPxZCQZcacN-Vr','The Beverly Hillbillies','beverlyhillbillies.jpg'),
    ('NZUBiptZDLU%26list=PL4BAC7037010FBCF0','Disneyland - The Original 1950s Television Series','disneyland.jpg'),
    ('dPfRO1Zb2ZI%26list=PLF_EbdVJ6V2cc1ID-oEB_LDOOK52b0E_h','Mork and Mindy Season 1-2','mork.jpg'),
    ('RZzbrNUjQn0%26list=PLNGnyJ_9o6-Xnxvdz3ePb-xNK0D1HeSYG','Alfred Hitchcock Presents','hitch.jpg'),
    ('4wZOyjHDIZ0&list=PLYeJlWBZQQa_6zeH3t7ybpALa8DEJQpna','The Lone Ranger Season 1-2','lone.jpg'),
    ('isy2jWbs6N4&list=PLiSxBUjo1VCMuP2mmfrZicpsbaMLoa9CH','Popular Diffrent Strokes videos','strokes.jpg'),
    ('z55p72g1Wvw%26list=PLxNMT6vQ_PVEXjJEsPv7fTzgtoV3iY6kV','Popular Lassie videos','lassie.jpg'),
    ('_1JZpWweMQs%26list=PL0-31eWh3QplVWkOiOVmpKSxdZPqnQaal','Popular The Brady Bunch videos','brady.jpg'),
    ('kOXxvxjqWjU%26list=PLj44llpCwKIw0fqLy0jq3xRwHoVCwRB_G','Popular The Littlest Hobo videos','hobo.jpg'),
    ('3zQ_lZfMPwk%26list=PLE3gtwReXvMQiEfr9PomPlqO-TQmrGZUg','Popular One Day at a Time videos','oneday.jpg'),
    ('gX_s449BVeE%26list=PLjB1oGzn24fyd1xPbdHfOH5vlPdOaE-vQ','Popular The Munsters videos','munsters.jpg'),
    ('AcOf1_Nl8nQ%26list=PLWEVvZtBqsJ_fBp_Eok9r-Mm6UBOGq2zp','Popular The Magic School Bus videos','magicschool.jpg'),
    ('vC-BkADEnUM%26list=PL2F217D855BEA1AD6','Popular The Monkees - TV Show Episodes','monkies.jpg'),
    ('DqbXBT6rVXg%26list=PLZs0gQed9tMQ1GYjXWa8RgLafqpFf0oDr','Popular STARSKY & HUTCH Episodes[COLOR red]*NEW*[/COLOR]','shutch.jpg'),
    ('MgWb2uk8NS4%26list=PLQ41l_vNoPd8CZE3qiZZxOkHJklFxtsp9','Popular The Rockford Files Videos[COLOR red]*NEW*[/COLOR]','rock.jpg'),
    ('ln19GNiqXBo%26list=PL7YPN8JheNiJouD8ZeyeSEiJCa19ruBnB','Popular GUNSMOKE Season 1 thru 5[COLOR red]*NEW*[/COLOR]','gunsmoke.jpg'),
    ('pXsllHo5M1k%26list=PLtAUhMuKZ9db6i7FLNWv8o3nzDaglRDvR','Popular That\'s My Mama Videos[COLOR red]*NEW*[/COLOR]','mama.jpg'),
    ('T--K0md1E70%26list=PLPfexRHg55reg2TQoSRpTK9y66AWkitLT','Popular The Honeymooners Videos[COLOR red]*NEW*[/COLOR]','honey.jpg')
    ]

lucy_items = [
    ('kukhLITAD_w','Season 1 Episode 1 - The Girls Want To Go To A Nightclub','http://cdn4.static.ovimg.com/m/02r286c/?width=140'),
    ('fj37QNgaNWw','Season 1 Episode 2 - Be a pal', 'http://search.ovguide.com/?ci=85&q=I+Love+Lucy+%28%28Be+a+Pal%29+OR+%28Season+1+Episode+2%29%29'),
    ('5-gmEYt5iSs','Season 1 Episode 3 - The Diet','http://cdn4.static.ovimg.com/m/06z3mls/?width=140'),
    ('xPUyJ4ZFqco','Season 1 Episode 4 - Thinks Ricky Is Trying to Murder Her','http://cdn4.static.ovimg.com/m/0261tn2/?width=140'),
    ('cc7xyRDvgA0','Season 1 Episode 5 - The Quiz Show','http://cdn4.static.ovimg.com/m/06z3mm2/?width=140'),
    ('bTFrIyQs0S8','Season 1 Episode 6 - The Audition','http://cdn4.static.ovimg.com/m/06z3mmd/?width=140'),
    ('mCbw3ZfVswc','Season 1 Episode 7 - The Seance','http://search.ovguide.com/?ci=85&q=I+Love+Lucy+%28%28The+S%C3%A9ance%29+OR+%28Season+1+Episode+7%29%29'),
    ('o-e7WxPuAwY','Season 1 Episode 8 - Men Are Messy','http://cdn4.static.ovimg.com/m/06z3mn0/?width=140'),
    ('0AkQhSq2Jc4','Season 1 Episode 9 - The Fur Coat','http://cdn4.static.ovimg.com/m/06z3mnn/?width=140'),
    ('QJLTk0NoYr4','Season 1 Episode 10 - Lucy Is Jealous of Girl Singer','http://cdn4.static.ovimg.com/m/06z3mnz/?width=140'),
    ('nMUuWQA_FLw','Season 1 Episode 11 - Drafted','http://cdn4.static.ovimg.com/m/06z3mnb/?width=140'),
    ('Pakn-xFqlXg','Season 1 Episode 12 - The Adagio','http://cdn4.static.ovimg.com/m/06z3mp8/?width=140'),
    ('B7_16eUcbsM','Season 1 Episode 13 - The Benefit','http://cdn4.static.ovimg.com/m/06z3mpl/?width=140'),
    ('J6Z6DdTgQ0A','Season 1 Episode 14 - The Amateur Hour','http://cdn4.static.ovimg.com/m/06z3mpx/?width=140'),
    ('Dn99IFVo5T0','Season 1 Episode 15 - Lucy Plays Cupid','http://cdn4.static.ovimg.com/m/06z3mq6/?width=140'),
    ('ioOwnx7jZAY','Season 1 Episode 17 - Lucy Writes a Play','http://cdn4.static.ovimg.com/m/06z3mqv/?width=140'),
    ('bBOjaEv92DM','Season 1 Episode 18 - Breaking the Lease','http://cdn4.static.ovimg.com/m/06z3mr4/?width=140'),
    ('3gJe8TkYkFQ','Season 1 Episode 19 - The Ballet','http://cdn4.static.ovimg.com/m/06z3mrg/?width=140'),
    ('nORJKpwBQB8','Season 1 Episode 20 - The Young Fans','http://cdn4.static.ovimg.com/m/06z3mrs/?width=140'),
    ('JIQu064WWy0','Season 1 Episode 21 - New Neighbors','http://cdn4.static.ovimg.com/m/06z3ms2/?width=140'),
    ('oDUezpCHMgg','Season 1 Episode 22 - Fred and Ethel Fight','http://cdn4.static.ovimg.com/m/06z3msd/?width=140'),
    ('Dqo8BH9jJfw','Season 1 Episode 23 - The Moustache','http://cdn4.static.ovimg.com/m/06z3msq/?width=140'),
    ('2gslTmaow9U','Season 1 Episode 24 - The Gossip','http://cdn4.static.ovimg.com/m/06z3mt0/?width=140'),
    ('NrQjbpg2KjA','Season 1 Episode 25 - Pioneer Women','http://cdn4.static.ovimg.com/m/06z3mtb/?width=140')
    ]
    
    
    

def Main():
    GenerateMenu(menu_items)

def addedShows(url,name):
    BaseUrl = 'http://www.youtube.com/watch?v='
    for (url,name,img) in extra_items:
        addDir(100,BaseUrl+url.replace('&','%26'),'',name,os.path.join(art,img),0,True)
           


def findShows(url,name):
    if 'youtube.com' in url:
        youtubeShows(url,name)

    else:
        try:
            html = net.http_GET(url).content
        #    print html
        except:
            print html
        pattern = '\"top\"\>.+?\<a href=\"(.+?)\"\>.+?\<img src=\"(.+?)\".+?\<H3\>(.+?)\<\/H3\>'
        r = re.findall(r''+pattern+'', html, re.I|re.DOTALL)
        totalitems = len(r)
        for url, img, name in r:
            name = name.replace('<br>','').replace('\n','')
            addDir(200, BaseUrl+url, '', name, BaseUrl+img, totalitems, True)
    

def subIndex(url,spare):
    #if re.search('alibrary/ILoveLucy\.html', url, re.I):
    #    TBaseUrl = 'http://www.youtube.com/watch?v='
    #    for (url,name,img) in lucy_items:
    #        addDir(300,TBaseUrl+url.replace('&','%26'),'',name,img,0,True)
    #        return 

    #else:
        
    html = net.http_GET(url).content

    r = re.search(r'ign\=top\>.*?\<a\shref\=\"(.*?)\"\>(.*?)\<\/a\>', html, re.I|re.DOTALL)
    if r:
        addDir(300, BaseUrl+r.group(1), '', r.group(2), '', 0, False)
        
    
    r = re.findall(r'br\>\<a\shref=\"(.*?)\"\>(.*?)\<\/a\>', html, re.I)
    if r:
        for url, name in r:
            addDir(300, BaseUrl+url, '', name, '', 0, False)
        r = re.findall(r'frame\ssrc=\"(.*?)\"', html, re.I)
        if spare != 'NP':
            for url in r:
                name = re.split(r'embed/', url, re.I)[1]
                addDir(300,url, '', name, '', 0, False)
    if not r:
        r = re.findall(r'align=\"center\".*?\<a\shref=\"(.*?)\"\>.*?\<img\ssrc\=\"(.*?)\".*?\<H3\>(.*?)\<\/H3\>',
                       html.text, re.I|re.DOTALL)
        totalitems = len(r)
        for url, img, name in r:
            addDir(200, BaseUrl+url, '', name.replace('<br>',''), BaseUrl+img, totalitems, True)
        if not r:
            print 'not r:'
            print url
            
            r = re.search(r'\"\ssrc=\"(.*?)\"', html,re.I)
            #if r:
                #    ResolveStream(r.group(1), name)
                

    NP = re.search(r'\<P\>More\s+\<a\shref=\"(.*?)\"', html, re.I)
    if NP:
        addDir(200, BaseUrl+NP.group(1), 'NP','[COLOR yellow]Next Page>>>[/COLOR]', '', 0, True)
        

def ResolveStream(url,spare):
    xbmc.executebuiltin("XBMC.Notification(TV Time Capsule,Resolving Link,5000,"+os.path.join(art,'smallres.jpg')+")")

    html = net.http_GET(url).content
    if re.search(r'archive.org/embed', url, re.I):
        BaseUrl = 'http://www.archive.org'
        r = re.findall(r'source\ssrc=\"(.*?)\"', html,re.I)
        url = requests.get(BaseUrl+r[0],stream=True)
        PlayStream(url.url, name)

    elif re.search(r'\?list\=', url, re.I):
        youTubePlaylist(url)
        
    elif re.search(r'youtube.com/embed/', url, re.I):
        fid = re.split(r'embed/', url,re.I)[1]
        url   = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % fid
        PlayStream(url, name)

    elif re.search(r'com/watch\?v=', url, re.I):
        fid = re.split(r'watch\?v=', url,re.I)[1]
        url   = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % fid

        print url
        PlayStream(url, name)
        return youtubeShows('',name)
        
        

    elif re.search(r'hulu.com', url, re.I):
        dialog = xbmcgui.Dialog()
        dialog.ok('Stream Error','Media is Hosted at Hulu,',
                  'Streaming from Hulu Not working at the moment')
        return
        
    elif re.search(r'org/alibrary/', url,re.I):
        url = re.search(r'iframe\ssrc=\"(.*?)\"',html,re.I)
        if not url:
            url = re.search(r'src=\"(.*?)\"', html,re.I)
            if url:
                ResolveStream(url.group(1),'')
        ResolveStream(url.group(1),'')

    

def youTubePlaylist(url):
    if '&amp;hl=en_US' in url:
        url = re.split('&amp;', url, re.I)[0]
    html = requests.get(url)

    if re.search(r'div = id=\"player-unavailable\"', html, re.I):
        dialog = xbmcgui.Dialog()
        dialog.ok('[COLOR red]SORRY[/COLOR]','Video Not Available','')
        return
    
    if re.search(r'youtube\.com/embed\/.*?\?list\=', url, re.I):
        playListID = re.search(r'list\=(.*?):', url+':', re.I)
        if playListID:
            youTubeID = re.search(r'href\=\"http\:\/\/www.youtube\.com\/watch\?v\=(.*?)\"\>', html.text, re.I)
            try:
                url = 'https://www.youtube.com/watch?v=%s&list=%s'%(youTubeID.group(1), playListID.group(1))
            except:
                dialog = xbmcgui.Dialog()
                dialog.ok('[I][COLOR red]SORRY[/I][/COLOR]','Video Not Available','')
                return
            
        html = net.http_GET(url).content
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()  
        
        for fileID in re.finditer(r'data-video-title="(.+?)".+?data-video-id="(.+?)"', html.text, re.I):
            url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s'%fileID.group(2)
            liz = xbmcgui.ListItem(fileID.group(1))
            liz.setInfo( type="Video", infoLabels={"Title": fileID.group(1)})
            liz.setProperty("IsPlayable","true")
            pl.add(url, liz)

        if not xbmc.Player().isPlayingVideo():
             xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)


def youtubeShows(url,name):
    import HTMLParser


    html = net.http_GET(url).content
    html = html.encode('utf8','ignore')

    pattern = 'playlist-video-description\"\>.*?\<h4 class=\".*?\\"\>(.*?)\<\/h4\>'
    pattern +='.*?data-video-id=\"(.*?)\".*?data-thumb=\"(.*?)\"'

    if re.search(r''+pattern+'',html,re.I|re.DOTALL):
        for items in re.finditer(r''+pattern+'', html,re.I|re.DOTALL):
            showTitle = items.group(1)
            showID = items.group(2)
            showImg = items.group(3)
            url = 'http://www.youtube.com/watch?v='+showID
            if '[Deleted Video]' in showTitle:
                showTitle = '[COLOR red]%s[/COLOR]' % re.search(r'\[(.*?)\]',showTitle,re.I).group(1)
            try:
                showTitle = HTMLParser.HTMLParser().unescape(showTitle)
            except:
                pass
            addDir(300,url, '', showTitle, 'http:'+showImg, 0, True)

    else:
        pattern = 'related\"\sdata\-vid\=\"(.*?)\"\>\<img.*?src\=\"(.*?)\"'
        pattern += '.*?title\"\stitle\=\"(.*?)\"'
        for items in re.finditer(r''+pattern+'', html,re.I|re.DOTALL):
            showID = items.group(1)
            showImg = items.group(2)
            showTitle = items.group(3)
            url = 'http://www.youtube.com/watch?v='+showID
            if '[Deleted Video]' in showTitle:
                showTitle = '[COLOR red]%s[/COLOR]' % re.search(r'\[(.*?)\]',showTitle,re.I).group(1)
            showTitle = HTMLParser.HTMLParser().unescape(showTitle)
            addDir(300,url, '', showTitle, showImg, 0, True)

    
                    
        
def PlayStream(url, name):

    print 'playstream'
    print url
    
    try:
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='')
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
    
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        pl.add(url, liz)

        xbmc.Player().play(pl)
    except:
        pass
    

    
def addDir(mode,url,spare,name,icon,totalItems,folder):
    u = sys.argv[0]
    u += "?mode=" +str(mode)
    u += "&url=" +str(url)
    u += "&spare=" +spare
    u += "&name=" +str(name)
    u += "&icon=" +str(icon)
    u += "&totalItems=" +str(totalItems)
    u += "&folder=" +str(folder)

    name = re.sub('Popular\s','[COLOR yellow]*Popular* [/COLOR]',name, re.I)
    

    infoLabels = {'cover_url': icon, 'title': name}
    ok = True
    liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels=infoLabels)
    if folder == True:ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,
                                                     totalItems=int(totalItems))
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

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


params = get_params()
mode = None
url = None
spare = None
name = None
icon = None
totalItems = None
folder = None

try:
    mode = urllib.unquote_plus(params['mode'])
except:
    pass
try:
    url = urllib.unquote(params["url"])
except:
    pass
try:

    print params["spare"]
    spare = str(params["spare"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    icon = urllib.unquote_plus(params["icon"])
except:
    pass
try:
    totalItems = urllib.unquote_plus(params['totalItems'])
except:
    pass
try:
    folder = urllib.unquote_plus(params["folder"])
except:
    pass

print '================================='
print spare


xbmc.log('Mode: '+str(mode))
xbmc.log('Url: '+str(url))
#xbmc.log('Spare: '+spare)
xbmc.log('Name: '+str(name))
xbmc.log('Icon: '+str(icon))
xbmc.log('TotalItems: '+str(totalItems))
xbmc.log('Folder: '+str(folder))

if mode == None or url == None or len(url)<1:
    Main()
elif mode == '100':
    findShows(url,name)
elif mode == '150':
    addedShows(url,name)
elif mode == '200':
    subIndex(url,spare)
elif mode == '300':
    print '+++++'
    print spare
    ResolveStream(url,spare)
    


xbmcplugin.endOfDirectory(int(sys.argv[1]),succeeded=True)
