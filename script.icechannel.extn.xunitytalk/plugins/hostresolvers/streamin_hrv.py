'''
    Ice Channel    
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmcgui
import re



class Streamin(HostResolver):
    implements = [HostResolver]
    name = "streamin"
    
    match_list = ['streamin.to']    


    def Resolve(self, url):
        try:
            from entertainment.net import Net
            net = Net(cached=False)
    
            html = net.http_GET(url).content

            import time
            time.sleep(5)            
            
            data = {}
            r = re.findall(r'type="(?:hidden|submit)?" name="(.+?)" value=(.+?)"', html)
            print r
            for name, value in r:
                data[name] = value.replace('"','')
                
            html = net.http_POST(url,data,headers={'Host':'streamin.to','Referer':url}).content
            print html
            r = re.compile('file: "(.+?)"').findall(html)
            s=re.compile('streamer: "(.+?)"').findall(html)

            return s[0]+' playpath='+r[0] + ' pageUrl=' + url + ' swfUrl=http://streamin.to/player/player.swf live=false'

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR white]' + self.name.upper() + '[/COLOR][/B]', '[COLOR red]Exception occured, check logs.[/COLOR]')                
            return None
            
