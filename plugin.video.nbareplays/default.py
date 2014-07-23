import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

ADDON = xbmcaddon.Addon(id='plugin.video.nbareplays')

BASE_URL='http://replay.nbaliveonline.tv'

icon = xbmc.translatePath(os.path.join('special://home/addons/nbareplays', 'icon.png'))


def CATEGORIES():
        addDir('Latest Games',BASE_URL,1,icon,'')
        addDir('Choose Your Team',BASE_URL,2,icon,'')
       
       
                      												  
def MAIN(url,description):

        static_url=url
        link=OPEN_URL(url)
        
        match=re.compile('<div class="poster"><a href="(.+?)" title="(.+?) Replay"><img src="(.+?)&w=.+?').findall(link)
        for url,name,iconimage in match:
            addDir(name,url,3,iconimage+'&w=254&h=170','')
            
        if not description=='':
              page=description
              if "class='nextpostslink'>" in link:
                    try:
	                    pagenum= int(page) + 1
	                    new_url = static_url.split('page')[0]+'page/'+str(pagenum)+'/'
	            
	                    addDir('Next Page >>',new_url,1,'',str(pagenum))
                    except:pass
                
def TEAM(url):
        link=OPEN_URL(url)
        link=link.split('>NBA Replay</a>')[1]
        
        link=link.split('</ul>')[0]
        match=re.compile('href="(.+?)">(.+?)</a>').findall(link)
        
        for url,name in match:
            addDir(name,url,1,icon,'1')
        
 
            
def GET_GAMES(name,url,iconimage):
        link=OPEN_URL(url)
        try:
            match=re.compile("<div id=\"tabs-1\"><iframe src='(.+?)'").findall(link)[0]
            addDir(name,match,200,iconimage,'')
        except:
            match=re.compile("class='videoheader'>(.+?)</h3><iframe src='(.+?)'").findall(link)
            for name,url in match:
                addDir(name,url,200,iconimage,'')
    
            
def GrabVK(url):
    link = OPEN_URL(url.replace('amp;',''))
    name=[]
    url=[]
    r      ='"url(.+?)":"(.+?)"'
    match = re.compile(r,re.DOTALL).findall(link)
    for quality,stream in match:
        name.append(quality+'p')
        url.append(stream.replace('\/','/'))
    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]            
            
    
    
def PLAY_STREAM(name,url,iconimage):

    stream_url = GrabVK(url)

    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(stream_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)            
            
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

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode == 200:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok        
        
        
def addLink(name,url,iconimage,description):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok 
 
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


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
        description=urllib.unquote_plus(params["description"])
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
        print ""+url
        MAIN(url,description)
        
elif mode==2:
        print ""+url
        TEAM(url)
        
elif mode==3:
        print ""+url
        GET_GAMES(name,url,iconimage)
       
        
elif mode==200:
        print ""+url
        PLAY_STREAM(name,url,iconimage)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
