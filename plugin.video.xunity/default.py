import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import extract
import downloader


ADDON = xbmcaddon.Addon(id='plugin.video.xunity')
base_url='http://xunitytalk-repository.googlecode.com/svn/skins/'
icon = 'http://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.xunity/icon.png'
ifan = 'http://xunitytalk-repository.googlecode.com/svn/addons/plugin.video.xunity/fanart.jpg'

xbmcfolder = xbmc.translatePath(os.path.join('special://home',''))
splashimage = xbmc.translatePath(os.path.join('special://home/media','Splash.png'))

addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
xunitytalk=os.path.join(addonfolder,'repository.xunitytalk')

ISTREAM_PATH=os.path.join(addonfolder,'repository.istream')
packages = xbmc.translatePath(os.path.join('special://home/addons','packages'))
icechannel = xbmc.translatePath(os.path.join('special://home/addons','script.icechannel'))

icechannelzip='http://istream-xbmc-repo.googlecode.com/svn/repo/zips/script.icechannel/script.icechannel.zip'

ISTREAMREPO='http://xunitytalk-repository.googlecode.com/svn/addons/repository.istream/repository.istream-1.0.zip'

XUNITYTALK='http://xunitytalk-repository.googlecode.com/svn/addons/repository.xunitytalk/repository.xunitytalk-1.0.0.zip'

def CATEGORIES():
        addDir('[COLOR blue]R[/COLOR]emove [COLOR blue]S[/COLOR]plash [COLOR blue]I[/COLOR]mage','url',3,icon,ifan,'','')
        addDir('F[COLOR blue]i[/COLOR]x My [COLOR blue]i[/COLOR]Stream','url',2,icon,ifan,'','')
        link=OPEN_URL(base_url+'skins.txt')
        match=re.compile('name="(.+?)".+?skins="(.+?)".+?desc="(.+?)"',re.DOTALL).findall (link)
        for name ,zip_url ,description in match:
        
            url_dest    =   base_url+'%s/%s' %(name,zip_url)
            iconimage   =   base_url+'%s/icon.png' %name
            fanart      =   base_url+'%s/fanart.png' %name
            
            addDir(name,url_dest,1,iconimage,fanart,description,'')
            
        setView('movies', 'everything') 
       
       
                                                                      
def Install(name,url,common):
        profile = xbmc.getInfoLabel("System.ProfileName" )
        dp = xbmcgui.DialogProgress()
        dp.create("[COLOR blue]i[/COLOR]Stream","Downloading ",name, 'Please Wait')
        lib=os.path.join(packages,name+'.zip')
        commonzip=os.path.join(packages,common)
        splash=os.path.join(packages,'splash.zip')
        try:
           os.remove(lib)
        except:
           pass
        downloader.download(url, lib, dp)#download skin
        dp.update(0,name, "Extracting Zip Please Wait")
        extract.all(lib,addonfolder,dp)#extract skin
        
        Dependencies()
        
        if os.path.exists(icechannel)==True:
            GetFile(packages,'script.icechanne*')
            GetFile(addonfolder,'script.icechannel')
            
        downloader.download(icechannelzip, os.path.join(packages,'script.icechannel.zip'), dp)
        dp.update(0,name, "Extracting Zip Please Wait")
        extract.all(os.path.join(packages,'script.icechannel.zip'),addonfolder,dp)
        
        if os.path.exists(xunitytalk)==False:
            downloader.download(XUNITYTALK, os.path.join(packages,'XunityTalk_Repository.zip'), dp)
            dp.update(0,name, "Extracting Zip Please Wait")
            extract.all(os.path.join(packages,'XunityTalk_Repository.zip'),addonfolder,dp)
            
        if os.path.exists(ISTREAM_PATH)==False:
            downloader.download(ISTREAMREPO, os.path.join(packages,'iStream_Repository.zip'), dp)
            dp.update(0,name, "Extracting Zip Please Wait")
            extract.all(os.path.join(packages,'iStream_Repository.zip'),addonfolder,dp)            
            
        if os.path.exists(splashimage)==False:
            dp.update(0,"", "Downloading") #download splash 
            downloader.download(base_url+'splash.zip', splash, dp)        
            dp.update(0,"", "Extracting Zip Please Wait")
            extract.all(splash,xbmcfolder,dp)#extract splash
        
            
        xbmc.executebuiltin('UpdateLocalAddons') 
        xbmc.executebuiltin("UpdateAddonRepos")
        dialog = xbmcgui.Dialog()
        if dialog.yesno("[COLOR blue]i[/COLOR]Stream", "Would You Like To Change Skin Now", ""):
            dialog.ok("[COLOR blue]i[/COLOR]Stream", "The Window Will Change To Apperance Settings", "Please Choose From Skin Drop Down Menu", "And Select Your New Skin")
            xbmc.executebuiltin("XBMC.ActivateWindow(appearancesettings)")
            
def Dependencies():
    dependencies = ['script.module.watchhistory','script.favourites','script.module.urlresolver','script.module.universal','script.module.beautifulsoup','script.module.metahandler','script.module.elementtree','script.module.t0mm0.common']
    for scripts in dependencies:
        addon=xbmc.translatePath(os.path.join('special://home/addons',scripts))
        if os.path.exists(addon)==False:
            dp = xbmcgui.DialogProgress()
            dp.create("[COLOR blue]i[/COLOR]Stream","Downloading ",scripts, 'Please Wait')
            lib=os.path.join(packages,scripts+'.zip')
            downloader.download('http://xfinity.xunitytalk.com/Modules/%s.zip'%scripts, lib, dp)
            dp.update(0,name, "Extracting Zip Please Wait")
            extract.all(os.path.join(lib),addonfolder,dp)
            
                    
def iStreamFix():
        dialog = xbmcgui.Dialog()
        
        GetFile(packages,'script.icechanne*')
        GetFile(addonfolder,'script.icechannel')
        
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR blue]i[/COLOR]Stream", "", "Please Reboot For [B][COLOR blue]i[/COLOR]Stream[/B] [B]F[COLOR blue]i[/COLOR]x[/B] To Take Effect", "")
        
def GetFile(directory,name):
     import glob
     both=xbmc.translatePath(os.path.join(directory, name))
     for infile in glob.glob(both):
         removefolder(infile)
         try:
             os.remove(infile)
         except:
             pass
        
def removefolder(name):   
    
    if os.path.exists(str(name))==True: 
        for root, dirs, files in os.walk(name):
            for f in files:
                try:
                    os.unlink(os.path.join(root, f))
                except:
                    pass
    if os.path.exists(str(name))==True: 
        for root, dirs, files in os.walk(name):
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except:
                    pass
    try:
        os.rmdir(name)
    except:
        pass



    


            
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
        
        

def addDir(name,url,mode,iconimage,fanart,description,common):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&common="+urllib.quote_plus(common)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty("Fanart_Image", fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
        
        
 
        
#below tells plugin about the views                
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
fanart=None
description=None
common=None

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
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        common=urllib.unquote_plus(params["common"])
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
        Install(name,url,common)
        
elif mode==2:
        iStreamFix()

elif mode==3:
        os.remove(splashimage)      
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR blue]i[/COLOR]Stream", "", "Please Reboot To Take Effect", "")
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
