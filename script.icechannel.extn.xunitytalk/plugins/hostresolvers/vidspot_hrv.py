'''
    Vidspot Host resolver
    for Istream ONLY
    17/01/2014

    Jas0npc, the-one

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
                    


class Vidspot(HostResolver):
    implements = [HostResolver]
    name = "Vidspot"
    match_list = ['vidspot.net']
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
            headers = {}
            html = net.http_GET(url).content

            headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                            'Connection': 'keep-alive', 'DNT': '1', 'Host': 'vidspot.net', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'})
        
            headers.update({'Cache-Control': 'max-age=0', 'Content-Type': 'application/x-www-form-urlencoded',
                            'Origin': 'http://vidspot.net', 'Referer': url, 'Cookie': 'lang=english; over.umz.d0=1'})

            postData = {}

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)

            check = re.search('\<b\sclass=\"err\"\>(.*?)\<\/b\>', html, re.I)

            if check:
                raise Exception (check.group(1)) 
            
            r = re.findall(r'\"hidden\"\sname=\"(.+?)\"\svalue=\"(.+?)\"\>', html, re.I)
            if r:
                for name, value in r:
                    postData.update({str(name): str(value)})
                postData.update({'usr_login': '', 'referer': '', 'method_free': '1'})
                html = net.http_POST(url, postData, headers).content

                r = re.findall(r'\"file\"\s\:\s\"(.+?)\"\,', html, re.I)[0]
                if r:
                    return str(r)
                if not r:
                    raise Exception ('Link Not Found')
            if not r:
                    raise Exception ('Link Not Found')

        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
