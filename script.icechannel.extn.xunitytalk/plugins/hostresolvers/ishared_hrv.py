'''
    Ishared Host resolver
    for Istream Only 
    23/01/2014

    Jas0npc, the-one

    version 0.1

    A thank you to all members of the Xunity team.

    (c)2014 Xunity.

    This resolver IS NOT OPEN SOURCE, It is to be used as
    part of Istream ONLY.
'''
from entertainment import jsunpack
from entertainment.plugnplay.interfaces import HostResolver
from entertainment.plugnplay import Plugin
from entertainment import common

import xbmcgui
import xbmc
import os
                    


class Ishared(HostResolver):
    implements = [HostResolver]
    name = "ishared"
    match_list = ['ishared.eu']
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

        net = Net(cached=False)
        common.addon.log( self.name.upper() + ' - Link: %s' % url )

        try:
            html = net.http_GET(url).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)
            
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)

            headers = {}
            headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                            'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'DNT': '1', 'Host': 'ishared.eu',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36'})

            try:
                movie = re.search(r'movie\s\:\s\"(.*?)\"\,', html, re.I).group(1)
                season = re.search(r'season\s\:\"?(\d+)\"\,', html, re.I).group(1)
                episod = re.search(r'episode\:\"?(\d+)\"', html, re.I).group(1)
                path = re.search(r'path\:\"(.*?)\"\,', html, re.I).group(1)
                played = re.search(r'played\s\:\s?(\d+)', html, re.I).group(1)
                host = re.search(r'//(.*?)/', path ).group(1)

                headers.update({'Host': str(host), 'Referer': str(url)})
            except Exception, e:
                raise Exception('Stream Not Found')

            html = net.http_GET(path, headers, auto_read_response=False).content

            postData = {}
            postData.update({'movie': str(movie), 'season': str(season),
                             'episode': str(episod), 'path': str(path),
                             'played': str(played)})

            del headers['Cache-Control']
            
            net.set_cookies(self.cookie_file)
            headers.update({'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                            'Host': 'ishared.eu', 'Origin': 'http://ishared.eu', 'X-Requested-With': 'XMLHttpRequest'})

            urlt = net.http_POST(url, postData, headers, auto_read_response=False).get_url()
            return path

            
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None 

            
        
