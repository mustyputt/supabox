'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui

import re, xbmcgui



class Vodlocker(HostResolver):
    implements = [HostResolver]
    name = "vodlocker"
    
    match_list = ['vodlocker.com']    


    def Resolve(self, url):
        try:
            from entertainment.net import Net
            net = Net(cached=False)
    
            html = net.http_GET(url).content

            import time
            time.sleep(3)            
            
            data = {}
            r = re.findall(r'type="(?:hidden|submit)?" name="(.+?)" value=(.+?)"', html)
            for name, value in r:
                data[name] = value.replace('"','')
                
            html = net.http_POST(url,data,headers={'Host':'vodlocker.com','Referer':url}).content
            
            sPattern =  'file: "(.+?)"'
            r = re.compile(sPattern).findall(html)
            return r[0]

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None
            
