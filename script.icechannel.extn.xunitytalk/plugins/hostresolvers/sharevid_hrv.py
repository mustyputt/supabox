'''
    Sharevid Host resolver
    for Istream ONLY
    18/01/2014

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
                    


class Sharevid(HostResolver):
    implements = [HostResolver]
    name = "Sharevid"
    match_list = ['sharevid.org']
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '%s.cookies') % name
    puzzle_img = os.path.join(common.captchas_path, '%s.png') % name
    icon = common.notify_icon
    try:
        os.makedirs(os.path.dirname(cookie_file))
    except OSError:
        pass

    
    def Resolve(self, url):

        from entertainment.net import Net
        import re

        common.addon.log( self.name.upper() + ' - Link: %s' % url )
        
        net = Net(cached=False)
        referer = url
        postData = {}

        try:
            html = net.http_GET(url).content

            if re.search(r'\<b\>File Not Found\<\/b\>', html, re.I):
                raise Exception ('File Not Found')

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]',
                                          'Resolving', 700, self.icon)
            
            r = re.findall(r'hidden\"\sname=\"(.*?)\"\svalue=\"?(.*?)\"', html, re.I)
            for name, value in r:
                postData.update({str(name): str(value)})

            html = net.http_POST(url, postData).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)

            url = re.search(r'href=\"(.*?)(?=\"\>Download)', html, re.I)
            if url:
                return url.group(1).replace(' ', '%20')

            if not url:
                raise Exception ('File Not Found')
            
        except Exception, e:
            common.addon.log(self.name.upper() + ' - Exception occured: %s' % e)
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: [B][COLOR white]' + self.name.upper() + '[/B][/COLOR]', '[COLOR red]'+str(e)+'[/COLOR]', 700, self.icon)                
            return None
