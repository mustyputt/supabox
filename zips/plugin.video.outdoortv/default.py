import urllib,urllib2,re,os
import xbmcplugin,xbmcgui,xbmcaddon
try:
    import json
except:
    import simplejson as json
from BeautifulSoup import BeautifulStoneSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.outdoortv')
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
fanart = os.path.join( home, 'fanart.jpg' )


def Categories():
        BASE = 'http://feed.theplatform.com/f/MTQ3NTE2MjMwOA/'
        PARAM = '/?types=none&fileFields=bitrate,duration,format,url&params=Player%3Dmyoutdoortv.com'
        PARAM1 = '&range=1-50&form=json&fields=author,content,defaultThumbnailUrl,description,pubDate,title&byContent=byFormat%3DFLV%7CWM%7CMove%7CThreeGPP%7CThreeGPP2%7CAAC%7CMPEG4%7CQT%7CMP3&validFeed=false&count=true'
        addDir('Between the Banks',BASE+'pssHGpIVQIQi'+PARAM+'/Shows/Between%20the%20Banks'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/betweenbanks.jpg')
        addDir('Australian Fishing Championships',BASE+'ycI5sgZ6vraB'+PARAM+'/Shows/Australian%20Fishing%20Championships'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/ausfishchamp-2.jpg')
        addDir("Sportsman's Adventures",BASE+'N_fzoOymr0Ud'+PARAM+'/Shows/Sportsmans%20Adventures'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/sportsmans_adventures.jpg')
        addDir('The Carolina Outdoorsman Show',BASE+'sA2HrQEiQZZV'+PARAM+'/Shows/The%20Carolina%20Outdoorsman'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/carolinaoutdoorsman.jpg')
        addDir('Ultimate Catch',BASE+'N58gKpiZKsOY'+PARAM+'/Shows/Ultimate%20Catch'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/ultimatecatchtv.jpg')
        addDir('Shooting USA',BASE+'zzBvTR8eH5a3'+PARAM+'/Shows/Shooting%20USA'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/shooting_usa.jpg')
        addDir('Remington Country TV',BASE+'jTAbgblRwWHU'+PARAM+''+PARAM1,1,'')
        addDir("Cabela's Outfitter Journal",BASE+'lA19UVpNoKoc'+PARAM+'/Shows/Cabelas%20Outfitter%20Journal'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/cabelas_1-2.jpg')
        addDir("Cabela's Memories in the Field",BASE+'E4YINEMBEZQj'+PARAM+'/Shows/Cabelas%20Memories%20in%20the%20Field'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/cabelas_2-2.jpg')
        addDir("Cabela's Ultimate Adventures",BASE+'hSHZQg0y3uKU'+PARAM+'/Shows/Cabelas%20Ultimate%20Adventures'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/cabelas_3-2.gif')
        addDir('Scott Martin Challenge',BASE+'hnRmy8KPkZjL'+PARAM+'/Shows/Scott%20Martin%20Challenge'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/scott_martin.jpg')
        addDir('Jimmy Houston Outdoors',BASE+'Qd2SJ3VK9A4d'+PARAM+'/Shows/Jimmy%20Houston%20Outdoors'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/jimmy-houston.gif')
        addDir("Babe Winkelman's Good Fishing",BASE+'jXTpQeI9maTP'+PARAM+'/Shows/Babe%20Winkelmans%20Outdoor%20Secrets'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/babe_fishing.gif')
        addDir('National Wild Turkey Federation',BASE+'EZ1uFBJ51WY2'+PARAM+'/Shows/National%20Wild%20Turkey%20Federation'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/nwtfresized.jpg')
        addDir("Mike Avery's Outdoor Magazine",BASE+'kK_0Xhn6jvLX'+PARAM+''+PARAM1,1,'http://www.myoutdoortv.com/images/stories/outdoormag.jpg')
        addDir('Living on the Wildside',BASE+'QZ29eDqzDFIj'+PARAM+'/Shows/Living%20On%20The%20Wildside'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/wild_side.gif')
        addDir('Living Outdoors',BASE+'1mZrKxEl8mir'+PARAM+'/Shows/Living%20Outdoors'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/living_outdoors.jpg')
        addDir('Jeep Outdoors',BASE+'zTwvm4Z7FVB3'+PARAM+'/Shows/Jeep%20Outdoors'+PARAM1,1,'')
        addDir('Indiana Outdoor Adventures',BASE+'dNQ5xo5icQRh'+PARAM+'/Shows/Indiana%20Outdoor%20Adventures'+PARAM1,1,'http://www.myoutdoortv.com/images/show-logos/IndianaOutdoorAdventures-200x135.jpg')
        addDir('High Country TV',BASE+'I47FGARbPisB'+PARAM+''+PARAM1,1,'http://www.myoutdoortv.com/images/stories/high_country.jpg')
        addDir('Gator Trax Outdoors',BASE+'kwQx53U1g0hn'+PARAM+'/Shows/Gator%20Trax%20Outdoors'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/gator-trax-logo-2-2.jpg')
        addDir('Ducks, Dogs, and Decoys',BASE+'Cj6OKDHAxcY0'+PARAM+'/Shows/Ducks%20Dogs%20and%20Decoys'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/d3.jpg')
        addDir("Bob Redfern's Outdoor Magazine",BASE+'r98R5jFbMLLf'+PARAM+'/Shows/Bob%20Redfern%27s%20Outdoor%20Magazine'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/bob_redfern-2.gif')
        addDir('Backwoods Life',BASE+'pWbVbZjmjrtF'+PARAM+'/Shows/Backwoods%20Life'+PARAM1,1,'http://www.myoutdoortv.com/images/show-logos/BackwoodsLife-150x47')
        addDir('Adirondack Trails',BASE+'u4NgTD1BIE0x'+PARAM+'/Shows/Adirondack%20Trails'+PARAM1,1,'http://www.myoutdoortv.com/images/show-logos/adirondack-trails.jpg')
        addDir("A Dog's Life",BASE+'g3Or2UhUY9_m'+PARAM+'/Shows/A%20Dogs%20Life'+PARAM1,1,'http://www.myoutdoortv.com/images/show-logos/a-dogs-life.jpg')
        addDir('Arctic Cat Outdoors',BASE+'c4kV9xKQW1sh'+PARAM+'/Shows/Arctic%20Cat%20Outdoors'+PARAM1,1,'http://www.myoutdoortv.com/images/show-logos/arctic-cat-outdoors.jpg')
        addDir('Alaskan Wilderness Family',BASE+'VQLhXqAX3n1Z'+PARAM+'/Shows/Alaskan%20Wilderness%20Family'+PARAM1,1,'http://www.myoutdoortv.com/images/show-logos/alaska-wilderness-family.jpg')
        addDir("Jim Duckworth's Fishing Adventures",BASE+'hjG3sk3KSMum'+PARAM+'/Shows/Jim%20Duckworths%20Fishing%20Adventures'+PARAM1,1,'http://www.myoutdoortv.com/images/stories/jim_duckworth.gif')

def Index(url):
        req = urllib2.Request(url)
        req.addheaders = [('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        data = json.loads(link)
        items = data['entries']
        for i in items:
            title = i['title']
            thumb = i['plmedia$defaultThumbnailUrl']
            desc = i['description']
            url = i['media$content'][0]['plfile$url']
            duration = str(i['media$content'][0]['plfile$duration'])
            try:
                addLink(title,url,desc,duration.split('.')[0],thumb,2)
            except:
                title = title.encode('utf-8', 'ignore')
                addLink(title,url,desc,duration.split('.')[0],thumb,2)
            
            
def setUrl(url):
        req = urllib2.Request(url)
        req.addheaders = [('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulStoneSoup(link)
        url = soup.meta['base']+soup.video['src']
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


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

        
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
def addLink(name,url,description,duration,iconimage,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": duration })
        liz.setProperty( "Fanart_Image", fanart)
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


params=get_params()

url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
    print ""
    Categories()

elif mode==1:
    print ""
    Index(url)

elif mode==2:
    print ""
    setUrl(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))