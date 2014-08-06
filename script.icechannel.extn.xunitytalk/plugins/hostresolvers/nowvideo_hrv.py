'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui

import re, xbmcgui


class Nowvideo(HostResolver):
    implements = [HostResolver]
    name = "nowvideo"
    match_list = ['nowvideo.ch','nowvideo.eu','nowvideo.sx','nowvideo.ws','nowvideo.at']

    def Resolve(self, url):
        try:
            
            from entertainment.net import Net
            net = Net(cached=False)
            
            html = net.http_GET(url).content

            key = re.compile('flashvars.filekey=(.+?);').findall(html)
            ip_key = key[0]
            pattern = 'var %s="(.+?)".+?flashvars.file="(.+?)"'% str(ip_key)
            r = re.search(pattern,html, re.DOTALL)
            if r:
                filekey, filename= r.groups()
            else:
                r = re.search('file no longer exists',html)
                if r:
                    raise Exception ('File Not Found or removed')
            
            #get stream url from api
            api = 'http://www.nowvideo.sx/api/player.api.php?key=%s&file=%s' % (filekey, filename)
            html = net.http_GET(api).content
            r = re.search('url=(.+?)&title', html)
            if r:
                import urllib
                stream_url = urllib.unquote(r.group(1))
            else:
                r = re.search('file no longer exists',html)
                if r:
                    raise Exception ('File Not Found or removed')
                raise Exception ('Failed to parse url')
                
            return stream_url
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None