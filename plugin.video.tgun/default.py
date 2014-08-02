import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib2
import re, string
import os
from urlparse import urlparse
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net = Net()

try:
    import json
except:
    import simplejson as json


##### XBMC  ##########
addon = Addon('plugin.video.tgun', sys.argv)
xaddon = xbmcaddon.Addon(id='plugin.video.tgun')
datapath = addon.get_profile()


##### Paths ##########
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "cookiejar.lwp")
if os.path.exists(cookie_path) == False:
    os.makedirs(cookie_path)

##### Queries ##########
play = addon.queries.get('play', None)
mode = addon.queries['mode']
page_num = addon.queries.get('page_num', None)
url = addon.queries.get('url', None)

print 'Mode: ' + str(mode)
print 'Play: ' + str(play)
print 'URL: ' + str(url)
print 'Page: ' + str(page_num)

################### Global Constants #################################

main_url = 'http://www.tgun.tv/'
shows_url = main_url + 'shows/'
#showlist_url = 'http://www.tgun.tv/menus2/shows/chmenu%s.php'
showlist_url = 'http://www.tgun.tv/menus/shows/chmenu.php'
num_showpages = 4
classic_url = main_url + 'classic/'
classic_shows_url = 'http://www.tgun.tv/menus2/classic/chmenu%s.php'
livetv_url = main_url + 'usa/'
livetv_pages = 'http://www.tgun.tv/menus2/usa/chmenu%s.php'
addon_path = xaddon.getAddonInfo('path')
icon_path = addon_path + "/icons/"

######################################################################

def Notify(typeq, title, message, times, line2='', line3=''):
     #simplified way to call notifications. common notifications here.
     if title == '':
          title='TGUN Notification'
     if typeq == 'small':
          if times == '':
               times='5000'
          smallicon= icon_path + 'tgun.png'
          xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+smallicon+")")
     elif typeq == 'big':
          dialog = xbmcgui.Dialog()
          dialog.ok(' '+title+' ', ' '+message+' ', line2, line3)
     else:
          dialog = xbmcgui.Dialog()
          dialog.ok(' '+title+' ', ' '+message+' ')


def sys_exit():
    xbmc.executebuiltin("XBMC.Container.Update(addons://sources/video/plugin.video.tgun?mode=main,replace)")
    return


def getSwfUrl(channel_name):
        """Helper method to grab the swf url, resolving HTTP 301/302 along the way"""
        base_url = 'http://www.justin.tv/widgets/live_embed_player.swf?channel=%s' % channel_name
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                   'Referer' : 'http://www.justin.tv/'+channel_name}
        req = urllib2.Request(base_url, None, headers)
        response = urllib2.urlopen(req)
        return response.geturl()


def justintv(embedcode):

    channel = re.search('data="(.+?)"', embedcode, re.DOTALL).group(1)  
    channel_name = re.search('http://www.justin.tv/widgets/.+?\?channel=(.+)', channel).group(1)
    
    channel_name = par
    
    api_url = 'http://usher.justin.tv/find/%s.json?type=live' % channel_name
    print 'Retrieving: %s' % api_url
    html = net.http_GET(api_url).content
    
    data = json.loads(html)
    try:
        jtv_token = ' jtv='+data[0]['token'].replace('\\','\\5c').replace(' ','\\20').replace('"','\\22')
    except:
        Notify('small','Offline', 'Channel is currently offline','')
        return 'Offline'
    rtmp = data[0]['connect']+'/'+data[0]['play']
    swf = ' swfUrl=%s swfVfy=1' % getSwfUrl(channel_name)
    page_url = ' Pageurl=http://www.justin.tv/' + channel_name
    final_url = rtmp + jtv_token + swf + page_url
    return final_url


def sawlive(embedcode, ref_url):
    url = re.search("<script type='text/javascript'> swidth='[0-9%]+', sheight='[0-9%]+';</script><script type='text/javascript' src='(.+?)'></script>", embedcode, re.DOTALL).group(1)
    ref_data = {'Referer': ref_url}

    try:
        ## Current SawLive resolving technique - always try to fix first
        html = net.http_GET(url,ref_data).content
        link = re.search('src="(http://sawlive.tv/embed/watch/[A-Za-z0-9_/]+)">', html).group(1)
        print link

    except Exception, e:
        ## Use if first section does not work - last resort which returns compiled javascript
        print 'SawLive resolving failed, attempting jsunpack.jeek.org, msg: %s' % e
        Notify('small','SawLive', 'Resolve Failed. Using jsunpack','')
        
        jsunpackurl = 'http://jsunpack.jeek.org'
        data = {'urlin': url}
        html = net.http_POST(jsunpackurl, data).content
        link = re.search('src="(http://sawlive.tv/embed/watch/[A-Za-z0-9]+[/][A-Za-z0-9_]+)"',html).group(1)
        print link

    html = net.http_GET(link, ref_data).content
    
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    playPath = re.search('\'file\', \'(.+?)\'', html).group(1)
    streamer = re.search('\'streamer\', \'(.+?)\'', html).group(1)
    appUrl = re.search('rtmp[e]*://.+?/(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' app=', appUrl,
       ' pageURL=', url,
       ' swfUrl=', swfPlayer,
       ' live=true'])
    print rtmpUrl
    return rtmpUrl


def shidurlive(embedcode, ref_url):
    url = re.search("<script type='text/javascript'> swidth='100%', sheight='100%';</script><script type='text/javascript' src='(.+?)'></script>", embedcode, re.DOTALL).group(1)
    ref_data = {'Referer': ref_url}

    try:
        html = net.http_GET(url,ref_data).content
        url = re.search('src="(.+?)">', html).group(1)
    except Exception, e:
        addon.log_error('Cannot resolver shidurlive link')
        return None

    html = net.http_GET(url, ref_data).content
    
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    playPath = re.search('\'file\', \'(.+?)\'', html).group(1)
    streamer = re.search('\'streamer\', \'(.+?)\'', html).group(1)
    appUrl = re.search('rtmp[e]*://.+?/(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' app=', appUrl,
       ' pageURL=', url,
       ' swfUrl=', swfPlayer,
       ' live=true'])
    print rtmpUrl
    return rtmpUrl


def mediaplayer(embedcode):
    url = re.search('<embed type="application/x-mplayer2" .+? src="(.+?)"></embed>', embedcode).group(1)
    print 'Retrieving: %s' % url
    html = net.http_GET(url).content
    
    matches = re.findall('<Ref href = "(.+?)"/>', html)
    url = matches[1]
    
    print 'Retrieving: %s' % url
    html = net.http_GET(url).content
    print html
    
    return re.search('Ref1=(.+?.asf)', html).group(1)


def ilive(embedcode):
    
    #channel = re.search('<script type="text/javascript" src="http://www.ilive.to/embed/(.+?)&width=.+?"></script>', embedcode)
    channel = par
    print channel
    
    if channel:
        #url = 'http://www.ilive.to/embedplayer.php?channel=%s' % channel.group(1)
        url = 'http://www.ilive.to/embedplayer.php?channel=%s' % channel
        print 'Retrieving: %s' % url
        html = net.http_GET(url).content
        filename = re.search('file: "([^&]+).flv"', html).group(1)
        rtmp = re.search('streamer: "(.+?)",', html).group(1)
    else:
        filename = re.search('streamer=rtmp://live.ilive.to/edge&file=(.+?)&autostart=true&controlbar=bottom"', embedcode).group(1)
        url = 'http://www.ilive.to/embedplayer.php'

    swf = 'http://player.ilive.to/ilive-plugin.swf'
    return rtmp + ' playPath=' + filename + ' swfUrl=' + swf + ' swfVfy=true live=true pageUrl=' + url


def embedrtmp(embedcode, url):
    stream = re.search('<embed src="(.+?)" allowfullscreen="true" allowscriptaccess="always" flashvars="streamer=(rtmp://.+?)&amp;file=(.+?)&amp;type', embedcode)
    app = re.search('rtmp[e]*://.+?/(.+)', stream.group(2)).group(1)
    return stream.group(2) + ' app=' + app + ' playpath=' + stream.group(3) + ' swfUrl=' + stream.group(1) + ' pageUrl=' + url + ' live=true'


def castto(embedcode, url):
    data = {'Referer': url}
    
    parms = re.search('<script type="text/javascript"> fid="(.+?)"; v_width=.+; .+ src=".+castto.+"></script>', embedcode)
    
    link = 'http://static.castto.me/embed.php?channel=%s' % parms.group(1)
    html = net.http_GET(link, data).content
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    playPath = re.search('\'file\',\'(.+?)\'', html).group(1)
    streamer = re.search('\'streamer\',\'(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' pageURL=', 'http://static.castto.me',
       ' swfUrl=', swfPlayer,
       ' live=true',
       ' token=#ed%h0#w@1'])
    print rtmpUrl
    return rtmpUrl


def owncast(embedcode, url):
    data = {'Referer': url}
    
    parms = re.search('<script type="text/javascript"> fid="(.+?)"; v_width=(.+?); v_height=(.+?);</script><script type="text/javascript" src="(.+?)"></script>', embedcode)
    
    link = 'http://www.owncast.me/embed.php?channel=%s&vw=%s&vh=%s&domain=www.tgun.tv' % (parms.group(1), parms.group(2), parms.group(3))
    #html = net.http_GET(link, data).content
    referrer = url
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    req = urllib2.Request(link)
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Referer', referrer)
    response = urllib2.urlopen(req)
    html = response.read()
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    rtmpjson = re.search('getJSON\("(.+?)",', html).group(1)
    
    data = {'referer': link}
    rtmplink = net.http_GET(rtmpjson, data).content
    streamer = re.search('"rtmp":"(.+?)"', rtmplink).group(1)
    playPath = re.search('"streamname":"(.+?)"', rtmplink).group(1)
    
    
    if not re.search('http://www.owncast.me', swfPlayer):
        swfPlayer = 'http://www.owncast.me' + swfPlayer
    #playPath = re.search('\'file\',\'(.+?)\'', html).group(1)
    #streamer = re.search('\'streamer\',\'(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' pageURL=', link,
       ' swfUrl=', swfPlayer,
       ' live=true'])
    print rtmpUrl
    return rtmpUrl


def playerindex(embedcode):
    link = re.search('iframe src="(.+?)"', embedcode).group(1)
    link = urllib2.unquote(urllib2.unquote(link))
    print 'Retrieving: %s' % link 
    html = net.http_GET('http://www.tgun.tv/shows/' + link).content
    return html


def get_embed(html):
    #embedtext = "(<object type=\"application/x-shockwave-flash\"|<!--[0-9]* start embed [0-9]*-->|<!-- BEGIN PLAYER CODE.+?-->|<!-- Begin PLAYER CODE.+?-->|<!--[ ]*START PLAYER CODE [&ac=270 kayakcon11]*-->|)(.+?)<!-- END PLAYER CODE [A-Za-z0-9]*-->"
    embedtext = "</div>(.+?)<!-- start Ad Code 2 -->"
    #embedcode = re.search(embedtext, html, re.DOTALL).group(2)
    embedcode = re.search(embedtext, html, re.DOTALL).group(1)
    
    #Remove any commented out sources to we don't try to use them
    embedcode = re.sub('(?s)<!--.*?-->', '', embedcode).strip()
    return embedcode


def determine_stream(embedcode, url):
    if re.search('justin.tv', embedcode):
        print 'justin'
        stream_url = justintv(embedcode)
    elif re.search('castto', embedcode):
        print 'casto'
        stream_url = castto(embedcode, url)
    elif re.search('owncast', embedcode):
        print 'owncast'
        stream_url = owncast(embedcode, url)
    elif re.search('sawlive', embedcode):
        print 'sawlive'
        stream_url = sawlive(embedcode, url)
    elif re.search('shidurlive', embedcode):
        print 'shidurlive'
        stream_url = shidurlive(embedcode, url)       
    elif re.search('ilive.to', embedcode):
        print 'ilive'
        stream_url = ilive(embedcode)	
    elif re.search('MediaPlayer', embedcode):
        stream_url = mediaplayer(embedcode)
    elif re.search('rtmp', embedcode):
        stream_url = embedrtmp(embedcode, url)
    elif re.search('Ref1=(.+?asf)', embedcode):
        stream_url = re.search('Ref1=(.+?asf)', embedcode).group(1)
    else:
        stream_url = None
    return stream_url


if play:

    #Check for channel name at the end of url
    global par
    par = urlparse(url).query
    
    #Sometimes they pass in the url we want in a url query parm, check first
    r = re.search("((HTTP|http)://.+)", par)
    if r:
        url = r.group(1)

    html = net.http_GET(url).content
    #embedcode = get_embed(html)

    #Check for channels that have multiple stream sources
    stream_sources = re.compile('<a style="color: #000000; text-decoration: none;padding:10px; background: #38ACEC" href="#" onClick="Chat=window.open\(\'(.+?)\',\'player\',\'\'\); return false;"><b>(.+?)</b></a>').findall(html)
    
    if stream_sources:
        names = []
        links = []
        for link, name in stream_sources:
            names.append(name)
            links.append(link)
        
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose a video source', names)
        if index >= 0:
            url = links[index]
            html = net.http_GET(url).content
            par = urlparse(url).query
   
    #Remove any commented out sources to we don't try to use them
    embedcode = re.sub('(?s)<!--.*?-->', '', html).strip()
    #html = re.sub('(?s)<!--.*?-->', '', html).strip()

    if re.search('players/playerindex[0-9]*.php', html):
        #channel = urllib2.unquote(re.search('src="playerindex.php\?(.+?)"', embedcode).group(1))
        #html = playerindex(embedcode)
        embedcode = ''

    if re.search('http://tgun.tv/embed/', embedcode):
        link = re.search('src="(.+?)"', embedcode).group(1)
        embedcode = net.http_GET(link).content      
        embedcode = re.sub('(?s)<!--.*?-->', '', embedcode).strip()

    stream_url = determine_stream(embedcode, url)

    if not stream_url:
        #If can't find anything lets do a quick check for escaped html for hidden links
        if not embedcode or re.search('document.write\(unescape', html):
            escaped = re.search('document.write\(unescape\(\'(.+?)\'\)\);', html)
            escaped2 = re.search('<script type="text/javascript">var embed="";embed=embed\+\'<object width="640" height="466" id="dplayer"(.+?)</script>', html)
            if escaped or escaped2:
                if escaped:
                    embedcode = urllib2.unquote(urllib2.unquote(escaped.group(1)))
                else:
                    embedcode = urllib2.unquote(urllib2.unquote(escaped2.group(1)))
                embedcode = urllib2.unquote(urllib2.unquote(embedcode))
                print embedcode
                if re.search('streamer', embedcode):
                    stream = re.search('streamer=(.+?)&file=(.+?)&skin=.+?src="(.+?)"', embedcode)
                    if stream:
                        if '+' in stream.group(2):
                            playpath = par
                        else:
                            playpath = stream.group(2)
                        stream_url = stream.group(1) + ' playpath=' + playpath + ' swfUrl=http://www.tgun.tv' + stream.group(3) + ' pageUrl=' + url + ' live=true'                        
                    else:
                        swfPlayer = re.search('SWFObject\(\'(.+?)\'', embedcode).group(1)
                        streamer = re.search('\'streamer\',\'(.+?)\'', embedcode).group(1)
                        playPath = channel
                        stream_url = ''.join([streamer,
                                       ' playpath=', playPath,
                                       ' pageURL=', url,
                                       ' swfUrl=', 'http://www.tgun.tv' + swfPlayer,
                                       ' live=true'])
                    print stream_url
                elif re.search('http://tgun.tv/embed', embedcode):
                    link = re.search('src="(.+?)"', html)
                    if link:
                        html = net.http_GET(link.group(1)).content
                        html = re.sub('(?s)<!--.*?-->', '', html).strip()
                        stream_url = determine_stream(html, link.group(1))
                    else:
                        stream_url = None
        else:
            Notify('small','Undefined Stream', 'Channel is using an unknown stream type','')
            stream_url = None

    #Play the stream
    if stream_url and stream_url <> "Offline":
        addon.resolve_url(stream_url)


def tvchannels(turl = url, tpage = page_num):
    #turl = turl % tpage
    print 'Retrieving: %s' % turl
    html = net.http_GET(turl).content
    print html

    #tpage = int(tpage) 
    #if tpage > 1:
    #    addon.add_directory({'mode': 'mainexit'}, {'title': '[COLOR red]Back to Main Menu[/COLOR]'}, img=icon_path + 'back_arrow.png')

    #if tpage < num_showpages:
    #    tpage = tpage +  1
    #    addon.add_directory({'mode': 'tvchannels', 'url': showlist_url, 'page_num': tpage}, {'title': '[COLOR blue]Next Page[/COLOR]'}, img=icon_path + 'next_arrow.png')

    #Remove any commented out sources to we don't try to use them
    html = re.sub('(?s)<!--.*?-->', '', html).strip()
    
    #match = re.compile('<a Title="" href="#" onClick="Chat=window.open\(\'(.+?)\',\'img_m\',\'\'\); return false;"><img border="0" src="(.+?)" style="filter:alpha \(opacity=50\); -moz-opacity:0.5" onMouseover="lightup\(this, 100\)" onMouseout="lightup\(this, 30\)" width="110" height="80"></a>(.+?)</td>').findall(html)
    match = re.compile('<a Title="(.+?)" href="#" onClick="Chat=window.open\(\'(.+?)\',\'vid_z\',\'\'\); return false;"><img src="(.+?)" border="1" width=120 height=90 /></a>').findall(html)
    if not match:
        match = re.compile('<a Title=".*" href="(.+?)" target="img_m"><img border="0" src="(.+?)" style="filter:alpha[ \(opacity=50\)]*; -moz-opacity:0.5" onMouseover="lightup\(this, 100\)" onMouseout="lightup\(this, 30\)" width="110" height="80"></a>(.+?)</td>').findall(html)
    #for link, thumb, name in match:
    for name, link, thumb in match:
        if not re.search('http://', thumb):
            thumb = main_url + thumb
        if re.search('http://www.tgun.tv/menus/players/playerindex[0-9]*.php', link):
            name = name + '[COLOR blue]*[/COLOR]'
        addon.add_video_item({'mode': 'channel', 'url': link}, {'title': name}, img=thumb)

    
def mainmenu():
    #tvchannels(showlist_url, 1)
    whatismyip = "http://icanhazip.com/"
    print urllib2.urlopen(whatismyip).readlines()[0]
    addon.add_directory({'mode': 'tvchannels', 'url': showlist_url, 'page_num': 1}, {'title': 'Live TV Shows & Movies'}, img=icon_path + 'newtv.png')
    addon.add_directory({'mode': 'classics', 'url': classic_shows_url % 1, 'page_num': 1}, {'title': 'Classic TV Shows'}, img=icon_path + 'retrotv.png')
    addon.add_directory({'mode': 'livetv', 'url': livetv_pages % 1, 'page_num': 1}, {'title': 'Live TV Channels'}, img=icon_path + 'livetv.png')


if mode == 'main':
    mainmenu()


elif mode == 'mainexit':
    sys_exit()
    mainmenu()


elif mode == 'tvchannels':
    tvchannels()


elif mode == 'classics':
    print 'Retrieving: %s' % url
    html = net.http_GET(url).content

    page = int(page_num)    
    if page > 1:
        addon.add_directory({'mode': 'mainexit'}, {'title': '[COLOR red]Back to Main Menu[/COLOR]'}, img=icon_path + 'back_arrow.png')

    if page < 4:
        page = page +  1
        addon.add_directory({'mode': 'classics', 'url': classic_shows_url % page, 'page_num': page}, {'title': '[COLOR blue]Next Page[/COLOR]'}, img=icon_path + 'next_arrow.png')

    match = re.compile('<a Title="" href="(.+?)" target="img_m"><img border="0" src="(.+?)" style="filter:alpha\(opacity=50\); -moz-opacity:0.5" onMouseover="lightup\(this, 100\)" onMouseout="lightup\(this, 30\)" width="110" height="80"></a>(.+?)</td>').findall(html)
    for link, thumb, name in match:
        if not re.search('http://', thumb):
            thumb = main_url + thumb
        addon.add_video_item({'mode': 'channel', 'url': link}, {'title': name}, img=thumb)


elif mode == 'livetv':
    print 'Retrieving: %s' % url
    html = net.http_GET(url).content

    page = int(page_num)    
    if page > 1:
        addon.add_directory({'mode': 'mainexit'}, {'title': '[COLOR red]Back to Main Menu[/COLOR]'}, img=icon_path + 'back_arrow.png')

    if page < 4:
        page = page +  1
        addon.add_directory({'mode': 'livetv', 'url': livetv_pages % page, 'page_num': page}, {'title': '[COLOR blue]Next Page[/COLOR]'}, img=icon_path + 'next_arrow.png')

    match = re.compile('<td width="100%" .+? href="(.+?)" target="img_m"><img border="0" src="(.+?)" style=.+?></a>(.+?)</td>').findall(html)
    for link, thumb, name in match:
        if not re.search('http://', thumb):
            thumb = main_url + thumb
        addon.add_video_item({'mode': 'channel', 'url': link}, {'title': name}, img=thumb)

    
elif mode == 'exit':
    sys_exit()


if not play:
    addon.end_of_directory()