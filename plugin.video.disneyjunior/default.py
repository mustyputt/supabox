import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time


PLUGIN='plugin.video.disneyjunior'
ADDON = xbmcaddon.Addon(id=PLUGIN)


VIDEO='http://www.disney.co.uk:80/cms_res/disney-junior/video/'

def CATEGORIES():
            url='http://www.disney.co.uk/disney-junior/content/video.jsp?b=mch'
            link=OPEN_URL(url)
            match=re.compile('data-code="(.+?)" data-originpromo="(.+?)".+?\n.+?\n.+?\n.+?data-hover="(.+?)"').findall(link)
            for url,name,iconimage in match:
                url='http://www.disney.co.uk/disney-junior/content/video.jsp?b='+url
                name=str(name).replace('-',' ').upper()
                iconimage='http://www.disney.co.uk'+iconimage
                if 'dj.png' in iconimage:
                    iconimage='http://www.disney.co.uk/cms_res/disney-junior/images/video/brand_thumbs/active/120x120_active_dj.png'
                addDir(name,url,1,iconimage,'')
            setView('movies', 'default') 
       
       
                                                                      
def second_catergory(name,url):
    link=OPEN_URL(url).replace('\n','').replace('/cms_res/disney-junior/images/promo_support/promo_holders/video.png','').replace('/cms_res/disney-junior/images/promo_support/playlist_add_icon.png','')
    link=link.split('<div id="video_main_promos_inner">')[1]
    match=re.compile('<img src="/cms_res/disney-junior/images/(.+?)".+?div class="promo_title_3row"><p>.+?<br/>(.+?)</p>.+?data-itemName="(.+?)">').findall(link)
    for iconimage,name,passto in match:
        iconimage='http://www.disney.co.uk/cms_res/disney-junior/images/'+iconimage
        name=str(name).replace('%E2%80%99',"'").replace('U+2019',"'").replace('0x92',"'")
        print '============================ '+str(passto)
        addDir(name,url,2,iconimage,passto)
        setView('movies', 'default') 
    
    
def playvideo(name,url,iconimage,passto):
    r='"urlId":"%s".+?{"stream":{"program":"(.+?)"'%(passto)
    print r
    link=OPEN_URL(url).replace('\n','')
    match=re.compile(r).findall(link)
    print match
    url=match[0]
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(VIDEO+url.replace('/tv/disney_junior/','').replace('sofia-the-first/',''), liz)
    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    
    
    
    
def playall(name,url):
    dp = xbmcgui.DialogProgress()
    dp.create("Disney Junior",'Creating Your Playlist')
    dp.update(0)
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()

    response=OPEN_URL(url).replace('\n','')
    link = response.replace('/cms_res/disney-junior/images/promo_support/promo_holders/video.png','')#
    link = link.replace('/cms_res/disney-junior/images/promo_support/playlist_add_icon.png','')
    link = link.split('<div id="video_main_promos_inner">')[1]

    match = re.compile('<img src="/cms_res/disney-junior/images/(.+?)".+?div class="promo_title_3row"><p>.+?<br/>(.+?)</p>.+?data-itemName="(.+?)">').findall(link)

    playlist = []
    nItem    = len(match)

    try:
        for iconimage, name, passto in match:

            iconimage = 'http://www.disney.co.uk/cms_res/disney-junior/images/'+iconimage
            name      = str(name).replace('%E2%80%99',"'").replace('U+2019',"'").replace('0x92',"'")           

            liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name} )
            liz.setProperty("IsPlayable","true")

            r      = '"urlId":"%s".+?{"stream":{"program":"(.+?)"'%(passto)
            newURL = re.compile(r).findall(response)[0]
            newURL = newURL.replace('/tv/disney_junior/','').replace('sofia-the-first/','')
            playlist.append((VIDEO+newURL ,liz))
    
            progress = len(playlist) / float(nItem) * 100  
            dp.update(int(progress), 'Adding to Your Playlist',name)

            if dp.iscanceled():
                return

        dp.close()
    
        print 'THIS IS PLAYLIST====   '+str(playlist)
                
        for blob ,liz in playlist:
            try:
                if blob:
                    print blob
                    pl.add(blob,liz)
            except:
                pass

        if not xbmc.Player().isPlayingVideo():
	    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("Disney Junior", "Sorry Get All Valid Urls", "Why Not Try A Singular Video") 
        


         
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
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

def addDir(name,url,mode,iconimage,passto):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&passto="+urllib.quote_plus(passto)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        menu = []
        if not mode==2 and not mode==2000:
            forurl=urllib.quote(url)
            menu.append(('Play All Videos','XBMC.RunPlugin(%s?name=%s&mode=200&iconimage=None&passto=None&url=%s)'% (sys.argv[0],name,forurl)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
 
        
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
passto=None


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
        mode=int(params["mode"])
except:
        pass
try:        
        passto=urllib.unquote_plus(params["passto"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        second_catergory(name,url)
        
elif mode==2:
        playvideo(name,url,iconimage,passto)
        
elif mode==200:
        playall(name,url)
        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
