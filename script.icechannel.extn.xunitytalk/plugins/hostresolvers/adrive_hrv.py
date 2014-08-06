'''
    Adrive Host resolver
    for Istream
    05/01/2014

    version 0.1
'''

from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Adrive(HostResolver):
    implements = [HostResolver]
    name = "Adrive"
    match_list = ['adrive.com']
    profile_path = common.profile_path
    cookie_file = os.path.join(common.cookies_path, '%s.cookies') % name
    puzzle_img = os.path.join(common.captchas_path, '%s.jpg') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass
    

    def Resolve(self, url):
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        Referer = url

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                      'Resolving', 700, self.icon)

        try:
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            r = re.search(r'location\.href\s=\s\"(.*?)\"', html, re.I)
            if r:

                Host = re.search(r'//(.*?)/', r.group(1), re.I).group(1)
                headers = {}
                headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                                'Connection': 'keep-alive', 'Host': str(Host), 'Referer': str(Referer),
                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'})
            
                html = net.http_GET(r.group(1), headers).content
                return r.group(1)

            raise Exception ('Link Not Found.')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
