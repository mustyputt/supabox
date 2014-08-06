'''
    Ice Channel    
'''

from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui

import re, xbmcgui



class VidBull(HostResolver):
    implements = [HostResolver]
    name = "vidbull"
    match_list = ['vidbull.com']    

    def Resolve(self, url):
        try:
            from entertainment.net import Net
            net = Net(cached=False)
    
            html = net.http_GET(url).content

            data = {}
            html = re.search('<Form(.+?)/Form', html, re.DOTALL).group(1)
            r = re.findall(r'type="hidden"\s*name="(.+?)"\s*value="(.+?)"', html)
            for name, value in r:
                data[name] = value
                
            common.addon.show_countdown(4, title='Vidbull', text='Loading Video...')
            html = net.http_POST(url, data).content

            sPattern =  '<script type=(?:"|\')text/javascript(?:"|\')>eval\(function\(p,a,c,k,e,[dr]\)(?!.+player_ads.+).+?</script>'
            r = re.search(sPattern, html, re.DOTALL + re.IGNORECASE)
            if r:
                sJavascript = r.group()
                sUnpacked = jsunpack.unpack(sJavascript)
                stream_url = re.compile('(file:|src=)"(.+?)"').findall (sUnpacked)[0][1]
                if stream_url:
                    return stream_url
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None

