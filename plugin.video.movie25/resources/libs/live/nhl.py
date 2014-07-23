import urllib,urllib2,re,cookielib,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,time
from resources.libs import main
#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art


def MAINNHL():
    source_media = {}
    from datetime import datetime
    date=datetime.now().strftime('%Y%m%d')
    xml='http://feeds.cdnak.neulion.com/fs/nhl/mobile/feeds/data/'+str(date)+'.xml'
    link=main.OPENURL(xml)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile('<eastern-start-time>(.+?)</eastern-start-time>.+?<away-team>.+?<team-abbreviation>(.+?)</team-abbreviation>.+?</away-team><home-team>.+?<team-abbreviation>(.+?)</team-abbreviation>.+?</home-team><video-clip/><streams>(.+?)</streams>',re.DOTALL).findall(link)
    for timed,ateam,hteam,streams in match:
        split= re.search('(.+?)\s(\d+:\d+):\d+',timed)
        split1=str(split.group(1))
        split2=str(split.group(2))
        timed = time.strftime("%I:%M %p", time.strptime(split2, "%H:%M"))
        main.addDir(ateam+' at '+hteam+' [COLOR red]('+timed+')[/COLOR] [COLOR blue]('+split1+')[/COLOR]',streams,395,art+'/nhl.png')

def LISTSTREAMS(mname,murl):
    mname=main.removeColoredText(mname)
    awayteam= mname.split(' at ')[0]
    hometeam= mname.split(' at ')[1]
    match=re.compile('<live bitrate="0">([^<]+ipad.m3u8)</live>',re.DOTALL).findall(murl)
    if len(match)==0:
        link=main.OPENURL('http://breadwinka.com/get_games.php?client=nhl&playerclient=hop')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
        match=re.compile('<home_team>'+hometeam.replace(' ','')+'</home_team><away_team>'+awayteam.replace(' ','')+'</away_team><assignments><assignment.+?name="away"><ipad_url>(.+?)</ipad_url></assignment><assignment.+?name="home"><ipad_url>(.+?)</ipad_url>',re.DOTALL).findall(link)
        for away,home in match:
            pass
        print home
        link=main.OPENURL(home)
        url1=home.split('_hd')[0]
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        home=re.compile('BANDWIDTH=\d+(.+?.mp4.m3u8)',re.DOTALL).findall(link)
        for i in home:
            f= i.split('_hd_')[1]
            bitrate=f.split('_ipad_')[0]
            final= url1+'_hd_'+f
            main.addPlayc(hometeam+' Home'+' '+bitrate+' Kbps',final,396,art+'/nhl.png','','','','','')
        link2=main.OPENURL(away)
        url2=away.split('_hd')[0]
        link2=link2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        away=re.compile('BANDWIDTH=\d+(.+?.mp4.m3u8)',re.DOTALL).findall(link2)
        for i in away:
            f= i.split('_hd_')[1]
            bitrate=f.split('_ipad_')[0]
            final= url2+'_hd_'+f
            main.addPlayc(awayteam+' Away'+' '+bitrate+' Kbps',final,396,art+'/nhl.png','','','','','')
    else:
        url1=match[0].split('_hd')[0]
        link=main.OPENURL(match[0])
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        home=re.compile('BANDWIDTH=\d+(.+?_ipad.m3u8)',re.DOTALL).findall(link)
        for i in home:
            f= i.split('_hd_')[1]
            bitrate=f.split('_ipad.m3u8')[0]
            final= url1+'_hd_'+f
            main.addPlayc(hometeam+' Home'+' '+bitrate+' Kbps',final,396,art+'/nhl.png','','','','','')
        url2=match[1].split('_hd')[0]
        link2=main.OPENURL(match[1])
        link2=link2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        away=re.compile('BANDWIDTH=\d+(.+?_ipad.m3u8)',re.DOTALL).findall(link2)
        for i in away:
            f= i.split('_hd_')[1]
            bitrate=f.split('_ipad.m3u8')[0]
            final= url2+'_hd_'+f
            main.addPlayc(awayteam+' Away'+' '+bitrate+' Kbps',final,396,art+'/nhl.png','','','','','')
    

def LINK(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        namelist=[]
        urllist=[]
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        stream_url = murl+'|User-Agent=Roku/DVP-5.0 (025.00E08043A)'
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        infoL={'Title': mname, 'Genre': 'Live'} 
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='movie', title=mname,season='', episode='', year='',img=thumb,infolabels=infoL, watchedCallbackwithParams='',imdb_id='')

        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from resources.universal import watchhistory
            wh = watchhistory.WatchHistory('plugin.video.movie25')
            wh.add_item(mname+' '+'[COLOR green]NHL[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok
