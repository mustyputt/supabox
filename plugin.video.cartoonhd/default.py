import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json


ADDON = xbmcaddon.Addon(id='plugin.video.cartoonhd')

cartoon=os.path.join(ADDON.getAddonInfo('path'),'cartoon')

def CATEGORIES():
    addDir('[COLOR cyan].Top Movie[/COLOR]','picasa_topmovie',1,'https://lh4.googleusercontent.com/-xwlVx-Rv1qw/UrQN_iy5w0I/AAAAAAAABnY/l_wjhLjykuY/s630/marvel-rankings.jpg','')
    addDir('[COLOR cyan].Top Cartoon[/COLOR]','picasa_topcartoon',1,'https://lh5.googleusercontent.com/-l6lQqrU7BW0/UrQqqA4AlqI/AAAAAAAAIyE/LqwNMn_RBHo/s800/Disney-Pixar-Wallpaper-for-Desktop1.jpg','')
    addDir('[COLOR cyan].Top Disney Collection[/COLOR]','picasa_disneycollection',1,'https://lh6.googleusercontent.com/-srGy1JeuoxU/UmpVe7gEGBI/AAAAAAAABbA/m0LgdL3mAwQ/s640/WaltDisneyPicturesSpecialPoster.jpeg','')
    addDir('[COLOR cyan].Top IMDB[/COLOR]','picasa_imdb',1,'https://lh5.googleusercontent.com/-U-eB6iRwwns/UxxNvZrXHFI/AAAAAAAACmA/8HAwCVDzuSg/s800/imdb_top_250_bg.jpg','')
    xunity='https://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.cartoonhd/cats/cartoon'
    response=OPEN_URL(xunity)
    
    link=json.loads(response)

    data=link['Data']

    for field in data:
        name= field['Name'].encode("utf-8")
        iconimage= field['Image'].encode("utf-8")
        action=field['Action'].encode("utf-8")
        if not 'Top Movie' in name:
            if not 'Top Cartoon' in name:
                if not 'Top IMDB' in name:
                    if not 'Top Disney' in name:
                        addDir(name,action,1,iconimage,'')
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)            
    setView('movies', 'default') 
       
       
                                                                      
def GetContent(url):
    try:
        new_url='http://gappcenter.com/app/cartoon/mapi.php?action=getlistcontent&cate=%s&pageindex=0&pagesize=1000&os=newiosfull&version=2.1&deviceid=&token=&time=&device=iphone'%url
        response=OPEN_URL(new_url)
        link=json.loads(response)
        if 'invalid token' in response:
            print '#########################################'
            xunity='https://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.cartoonhd/cats/%s' % url
            link=json.loads(OPEN_URL(xunity))
        data=link['Data']
        for field in data:
            name= field['Name'].encode("utf-8")
            iconimage= field['Image'].encode("utf-8")
            url=field['Link'].encode("utf-8")
            addDir(name,url,200,iconimage,'')
        setView('movies', 'movies') 
    except:
        try:
            new_url='https://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.cartoonhd/cats/%s' % url
            response=OPEN_URL(new_url)
            link=json.loads(response)
            data=link['Data']
            for field in data:
                name= field['Name'].encode("utf-8")
                iconimage= field['Image'].encode("utf-8")
                url=field['Link'].encode("utf-8")
                addDir(name,url,200,iconimage,'')
            setView('movies', 'movies')
        except:    
            dialog = xbmcgui.Dialog()
            dialog.ok("Cartoon HD", "", "Sorry Cannot Resolve","")
    if ADDON.getSetting('sort')=='true':
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE) 
    
               
 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
    
def PLAY_STREAM(name,url,iconimage):
    if 'auengine.com' in url:
        html=OPEN_URL(url)
        url=re.compile("url: '(.+?)'").findall(html)[0]
        
    if 'animeonhand.com' in url:
        html=OPEN_URL(url)
        url=re.compile("'file': '(.+?)'").findall(html)[0]
        
        
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
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
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
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
        GetContent(url)
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
