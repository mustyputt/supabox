'''
    Googledocs
    for Istream ONLY
    

    Coolwave

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.

    version 0.1
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class googledocs(HostResolver):
    implements = [HostResolver]
    name = "googledocs"
    match_list = ['docs.google.com']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(profile_path, 'captchas', '%s.png') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass

    
    def Resolve(self, url):

        from entertainment.net import Net
        import re
        import time

        net = Net()

        try:

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)
        
            headers={'Referer':str(url), 'Host':'docs.google.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0','Connection':'keep-alive','Accept-Encoding':'gzip, deflate','Accept-Language':'en-US,en;q=0.5','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            
            html = net.http_GET(url, headers=headers).content.encode("utf-8").rstrip()
            video_url=re.search('fmt_stream_map".+?(http.+?),', html).group(1)
            video_url=video_url.replace('|', '').replace('\u003d','=').replace('\u0026','&')
            
            return video_url

            

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None

        
